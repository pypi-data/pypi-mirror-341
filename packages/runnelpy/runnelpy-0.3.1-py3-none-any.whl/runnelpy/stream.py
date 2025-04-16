from dataclasses import dataclass, replace
from functools import lru_cache
from typing import TYPE_CHECKING, Any, Callable, Iterable, Type, Union

import structlog

from runnelpy.exceptions import Misconfigured
from runnelpy.interfaces import Serializer
from runnelpy.record import Record

if TYPE_CHECKING:
    from runnelpy.app import App

logger = structlog.get_logger(__name__)


@dataclass(frozen=True)
class Stream:
    """
    A set of partitioned Redis streams, together representing a single logical event
    stream.

    Not intended to be used directly. Use :attr:`runnel.App.stream` instead.
    """
    app: "App"
    name: str
    record: Type[Record]
    partition_by: Union[str, Callable]
    serializer: Serializer  # Not applicable for records with primitive=True.
    hasher: Callable[[Any], int]
    partition_count: int
    partition_size: int

    def __post_init__(self):
        if self.record._primitive and self.serializer:
            raise Misconfigured("Cannot serialize primitive records")

        by = self.partition_by
        if isinstance(by, str) and not by in self.record.__fields__:
            raise Misconfigured("Stream.partition_by must specify a record field")

    def __hash__(self):
        return hash(self.id)

    def clone(self, **kwargs):
        return replace(self, **kwargs)

    @property
    def id(self):
        return f"{self.app.name}.{self.name}"

    @lru_cache(maxsize=None)
    def partition_key(self, i):
        return f"__strm:{self.id}.{i}"

    @lru_cache()
    def all_partition_keys(self):
        return [self.partition_key(i) for i in range(0, self.partition_count)]

    def route(self, key):
        return self.partition_key(self.hash(key))

    def hash(self, key):
        return self.hasher(key) % self.partition_count

    async def send(self, *records: Iterable[Record], stream_ids=None):
        """
        Send records to partitions of the stream, according to their partition keys.

        Parameters
        ----------
        records : Iterable[Record]
            The records to send.
        stream_ids : Optional[Iterable[str]]
            A list of stream_ids corresponding to the records. Must be the same length
            as records. If ``None``, then ``"*"`` will be used for all records. See
            `<https://redis.io/commands/xadd>`_ for more details.
        """
        if not stream_ids:
            stream_ids = ["*" for _ in range(len(records))]
        assert len(stream_ids) == len(records)

        async with self.app.redis.pipeline(transaction=True) as pipe:
            for record, stream_id in zip(records, stream_ids):
                # Use fields instead of entry, id instead of stream_id
                pipe.xadd(
                    name=self.route(self._compute_key(record)),
                    fields=self.serialize(record),
                    maxlen=self.partition_size,
                    approximate=True,
                    id=stream_id
                )
            await pipe.execute()

    async def read(self, group, consumer, prefetch, timeout, **keys):
        # redis-py async xreadgroup uses 'streams' dict
        return await self.app.redis.xreadgroup(  # yapf: disable
            groupname=group,
            consumername=consumer,
            streams=keys,
            count=prefetch,
            block=timeout,
        )

    async def ack(self, *events):
        if not events:
            return

        if len(events) == 1:
            e = events[0]
            # redis-py async xack takes ids as *args
            await self.app.redis.xack(e.partition.key, e.group, e.xid)
        else:
            keys = {}

            # Group events by key and group for efficient pipelining
            for e in events:
                key_group_tuple = (e.partition.key, e.group)
                if key_group_tuple not in keys:
                    keys[key_group_tuple] = []
                keys[key_group_tuple].append(e.xid)

            async with self.app.redis.pipeline(transaction=True) as pipe:
                for (key, group), xids in keys.items():
                    # Use specific redis-py async method pipe.xack
                    pipe.xack(key, group, *xids)
                await pipe.execute()
        logger.debug("acked", events=[e.data for e in events])

    def _compute_key(self, record):
        if isinstance(self.partition_by, str):
            return getattr(record, self.partition_by)
        elif isinstance(self.partition_by, Callable):
            return self.partition_by(record)

    def serialize(self, record):
        if self.record._primitive:
            return {k.encode("utf-8"): v for k, v in record.dict().items()}

        value = self.serializer.dumps(record.dict())
        if self.serializer.compressor:
            value = self.serializer.compressor.compress(value)
        return {b"data": value}

    def deserialize(self, value):
        if self.record._primitive:
            value = {k.decode("utf-8"): v for k, v in value.items()}
        else:
            value = value[b"data"]
            if self.serializer and self.serializer.compressor:
                value = self.serializer.compressor.decompress(value)
            value = self.serializer.loads(value)

        return self.record(**value)