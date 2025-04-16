import signal
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Set

import anyio
import structlog

from runnelpy import context
from runnelpy.discovery import autodiscover
from runnelpy.exceptions import Misconfigured
from runnelpy.executor import Executor
from runnelpy.utils import base64uuid

if TYPE_CHECKING:
    from runnelpy.app import App

logger = structlog.get_logger(__name__)


@dataclass
class Worker:
    """
    Runs processors for a given app. By default, will concurrently spawn an Executor
    task for every Processor known to the app. (The Executor in turn will spawn n tasks
    to actually process events -- one for every partition of the stream it owns.)
    """
    app: "App"
    id: str = field(default_factory=base64uuid)
    executors: Set[Executor] = field(default_factory=set)
    started: bool = False
    is_leader: bool = False

    def __hash__(self):
        return object.__hash__(self)

    @property
    def leader_key(self):
        return f"__lead:{self.app.name}"

    def start(self, processors="all"):
        """
        The main entrypoint.

        Parameters
        ----------
        processors : Union[str, List[str]]
            If "all", then run all processors known to the app. Otherwise only run those
            named in the processors list.

        Notes
        -----
        For every processor, the first worker to start will create a consumer group for
        in Redis if it does not already exist. It will set the starting ID to "0", which
        means "process the entire stream history". If you want to select a specific
        consumer group starting ID, see :func:`runnel.Processor.reset`.

        Examples
        --------
        >>> from runnelpy import Worker
        >>> from mymodule import myapp
        ...
        >>> # Run all processors.
        >>> Worker(myapp).start()
        ...
        >>> # Run specific processors.
        >>> Worker(myapp).start(["myproc1", "myproc2"])

        $ # Run named processor starting at specific ID from the shell
        $ runnel processor reset mymodule:myproc --start=12345-0
        $ runnel worker mymodule:myapp --processors=myproc
        """
        anyio.run(self._start, processors, backend="asyncio")

    async def _start(self, processors="all"):
        context.worker_id.set(self.id)
        assert processors == "all" or isinstance(processors, list)

        if self.started:
            raise Misconfigured("Worker already running")
        logger.info("starting-worker", processors=processors)

        # Import all modules likely to contain Runnel objects (e.g. processors, tasks)
        # that must be registered with the app.
        autodiscover(self.app)

        # Load lua scripts.
        for script_path in (Path(__file__).parent / "lua").glob("*.lua"):
            # redis-py async register_script returns a Script object
            script_obj = self.app.redis.register_script(script_path.read_text())
            self.app.scripts[script_path.stem] = script_obj

        # Create executors for all chosen processors.
        for proc in self.app.processors.values():
            if processors == "all" or proc.name in processors:
                await proc.prepare()
                self.executors.add(Executor(id=base64uuid(), processor=proc))

        # First leadership election attempt.
        await self._elect_leader()

        self.app.workers.add(self)
        try:
            async with anyio.open_signal_receiver(signal.SIGINT, signal.SIGTERM) as signals:
                async with anyio.create_task_group() as tg:
                    # The main executor tasks.
                    for e in self.executors:
                        await tg.spawn(e.start)

                    # Background tasks, e.g. timers, crontabs etc.
                    for t in self.app.tasks:
                        await tg.spawn(t, self)

                    # Leadership polling.
                    await tg.spawn(self.elect_leader)
                    self.started = True

                    # Allow for graceful shutdown.
                    async for signum in signals:
                        logger.critical("signal-received", signum=signum)
                        await tg.cancel_scope.cancel()
                        return
        finally:
            self.app.workers.remove(self)
            if not self.app.workers:
                # Use close() and wait_closed() for redis-py async
                await self.app.redis.close()
                await self.app.redis.wait_closed()
            logger.critical("worker-exit", executor_ids=[e.id for e in self.executors])

    async def elect_leader(self):
        # Poll a key in Redis and elect ourselves the leader if one does not exist. Not
        # very democratic, but all workers must poll frequently, so there can be no
        # disagreement. The lead worker is used to run tasks once across all workers
        # (e.g. timers, crontabs, etc).
        while True:
            logger.debug("leadership-check")
            await self._elect_leader()
            await anyio.sleep(self.app.settings.leadership_poll_interval / 1000)

    async def _elect_leader(self):
        # The leader key is essentially a lock, so we reuse the lock extension Lua
        # script.
        script_obj = self.app.scripts["lock_extend"]
        px = self.app.settings.leadership_poll_interval * 4
        # Use await script_obj(...) for redis-py async script execution
        leader = await script_obj(keys=[self.leader_key], args=[self.id, px])

        if leader:
            if not self.is_leader:
                logger.info("new-leader")
                self.is_leader = True
        else:
            self.is_leader = False