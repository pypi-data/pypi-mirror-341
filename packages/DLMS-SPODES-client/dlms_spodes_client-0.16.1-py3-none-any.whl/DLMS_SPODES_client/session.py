from typing_extensions import deprecated
from time import time
import queue
from itertools import count
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Optional, Collection, Iterator, TypeAlias, Self
from threading import Thread
import threading
from functools import cached_property
import asyncio
from StructResult import result
from DLMSCommunicationProfile.osi import OSI
from DLMS_SPODES.config_parser import get_values
from DLMS_SPODES import exceptions as exc
from StructResult.result import T
from .logger import LogLevel as logL
from .client import Client
from . import task

_settings = {
    "storage": {
        "persistent_depth": 1000,
        "volatile_depth": 100
    },
    "worker": {
        "run": False,
        "time_checking": 1.0
    }
}
if toml_val := get_values("DLMSClient", "session"):
    _settings.update(toml_val)


@dataclass(eq=False)
class Session:
    c: Client
    tsk: task.Base
    acquire_timeout: float = 10.0
    complete: bool = False
    res: result.Result = field(init=False)

    async def run(self):
        try:
            await asyncio.wait_for(self.c.lock.acquire(), timeout=self.acquire_timeout)
            self.c.log(logL.INFO, "Acquire")
            self.res = await self.tsk.run(self.c)
            self.c.lock.release()
            await asyncio.sleep(0)  # switch to other session
            # try media close
            if not self.c.lock.locked():
                await asyncio.wait_for(self.c.lock.acquire(), timeout=1)  # keep anywhere
                if self.c.media.is_open():
                    self.c.log(logL.DEB, F"close communication channel: {self.c.media}")
                    await self.c.media.close()
                else:
                    self.c.log(logL.WARN, F"communication channel: {self.c.media} already closed")
                self.c.lock.release()
                self.c.level = OSI.NONE
            else:
                self.c.log(logL.INFO, "opened media use in other session")
        except TimeoutError as e:
            self.res = result.Error(exc.DLMSException("server is buzy"))
        finally:
            self.complete = True
            if storage is not None:
                await storage.add(self)

    def __hash__(self):
        return hash(self.c)


@dataclass(frozen=True)
class DistributedTask:
    """The task for distributed execution on several customers."""
    tsk: task.Base
    clients: Collection[Client]

    def __str__(self) -> str:
        return f"{self.tsk.msg}[{len(self.clients)}])"


if _settings["storage"].get("persistent_depth") > 0:
    from collections import deque


    @dataclass(eq=False)
    class Result:
        c: Client
        msg: str
        tsk: task.Base
        value: Optional[T]
        time: float
        err: Optional[ExceptionGroup]

        def __hash__(self):
            return hash(self.c)


    class UniversalLock:
        def __init__(self):
            self._thread_lock = threading.Lock()
            self._async_lock = asyncio.Lock()

        def __enter__(self):
            self._thread_lock.acquire()
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            self._thread_lock.release()

        async def __aenter__(self):
            await self._async_lock.acquire()
            return self

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            self._async_lock.release()


    class Storage:
        def __init__(self, persistent_depth: int, volatile_depth: int):
            self._persistent = deque(maxlen=persistent_depth)
            self._volatile = deque(maxlen=volatile_depth)
            self._lock = UniversalLock()

        async def add(self, sess: Session):
            s_res = Result(
                c=sess.c,
                msg=sess.res.msg,
                tsk=sess.tsk,
                value=sess.res.value,
                time=time(),
                err=sess.res.err
            )
            async with self._lock:
                self._persistent.append(s_res)
                self._volatile.append(s_res)

        def get_persistent(self) -> list[Result]:
            with self._lock:
                return list(self._persistent)

        def get_volatile(self) -> set[Result]:
            with self._lock:
                old = self._volatile
                self._volatile = deque(maxlen=self._volatile.maxlen)
            return set(old)

        def client2sres(self, c: Client) -> list[Result]:
            with self._lock:
                tmp = list(self._persistent)
            return [res for res in tmp if res.c == c]


    storage: Storage = Storage(
        persistent_depth=_settings["storage"]["persistent_depth"],
        volatile_depth=_settings["storage"]["volatile_depth"]
    )
    """exchange results archive"""

else:
    storage: None = None


class Work:
    __non_complete: set[Session]
    __complete: set[Session]

    def __init__(self, *sessions: Session):
        self.__non_complete = set(sessions)
        self.__complete = set()

    def __str__(self):
        return f"Worker[{len(self.__non_complete)}/{len(self.all)}]: {"complete" if self.is_complete() else "in work"}[{len(self.ok_results)}/{len(self.__complete)}]"

    @classmethod
    def from_distributed_task(cls, *dis_tasks: DistributedTask) -> Self:
        sessions: list[Session] = list()
        client_tasks: dict[Client, list[task.Base]] = defaultdict(list)
        for dis_tsk in dis_tasks:
            for client in dis_tsk.clients:
                client_tasks[client].append(dis_tsk.tsk)
        for client, tasks in client_tasks.items():
            if len(tasks) == 1:
                sessions.append(Session(client, tsk=tasks[0]))
            else:
                sessions.append(Session(client, tsk=task.Sequence(*tasks)))
        return cls(*sessions)

    @cached_property
    def all(self) -> set[Session]:
        return self.__non_complete | self.__complete

    def __iter__(self) -> Iterator[Session]:
        for sess in self.__non_complete:
            yield sess

    def __getitem__(self, item) -> Session:
        return tuple(self.all)[item]

    @cached_property
    def clients(self) -> set[Client]:
        return {sess.c for sess in self.all}

    @property
    def ok_results(self) -> set[Session]:
        """without errors exchange clients"""
        return {sess for sess in self.__complete if sess.res.err is None}

    @cached_property
    def nok_results(self) -> set[Session]:
        """ With errors exchange clients """
        return self.all.difference(self.ok_results)

    def pop(self) -> set[Session]:
        """get and move complete session"""
        to_move = {sres for sres in self.__non_complete if sres.complete}
        self.__complete |= to_move
        self.__non_complete -= to_move
        return to_move

    def is_complete(self) -> bool:
        """check all complete sessions. call <pop> before"""
        return len(self.__non_complete) == 0


@dataclass
class Worker:
    time_checking: float = 1.0
    __t: Optional[threading.Thread] = field(init=False, default=None)
    __stop: threading.Event = field(init=False, default_factory=threading.Event)
    __works: queue.Queue[Work] = field(init=False, default_factory=queue.Queue)
    __has_work: asyncio.Event = field(init=False, default_factory=asyncio.Event)

    def start(self, abort_timeout: int = 5) -> None:
        if self.__t is not None and self.__t.is_alive():
            raise RuntimeError("Thread is already running")
        self.__t = threading.Thread(
            target=self._run_async_loop,
            args=(abort_timeout,),
            daemon=True
        )
        self.__t.start()

    def add_task(self, *task: DistributedTask) -> Work:
        self.__works.put(worker := Work.from_distributed_task(*task))
        self.__has_work.set()
        return worker

    def add_sessions(self, *sess: Session) -> Work:
        self.__works.put(worker := Work(*sess))
        self.__has_work.set()
        return worker

    def stop(self) -> None:
        self.__stop.set()
        self.__has_work.set()

    def join(self, timeout: Optional[float] = None) -> None:
        if self.__t is not None:
            self.__t.join(timeout)

    def _run_async_loop(self, abort_timeout: int) -> None:
        try:
            asyncio.run(self._coro_loop(abort_timeout))
        except Exception as e:
            print(f"Transaction thread error: {e}")

    async def _coro_loop(self, abort_timeout: int) -> None:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(self._monitor(tg), name="main_monitor")

    async def _monitor(self, tg: asyncio.TaskGroup) -> None:
        while not self.__stop.is_set():
            try:
                await asyncio.wait_for(self.__has_work.wait(), timeout=1.0)
                while not self.__stop.is_set():
                    try:
                        worker = self.__works.get_nowait()
                        for sess in worker:
                            tg.create_task(sess.run())
                        self.__works.task_done()
                    except queue.Empty:
                        self.__has_work.clear()
                        break
                    await asyncio.sleep(0)
            except asyncio.TimeoutError:
                continue  # Периодическая проверка stop_event
        if self.__stop.is_set():
            raise asyncio.CancelledError("Stop requested")


worker: Optional[Worker]
if _settings["worker"]["run"]:
    worker = Worker(_settings["worker"]["time_checking"])
else:
    worker = None
