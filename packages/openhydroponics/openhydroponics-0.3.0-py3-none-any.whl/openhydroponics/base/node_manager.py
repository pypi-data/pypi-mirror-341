from abc import ABC, abstractmethod
import asyncio
import time
from typing import AsyncGenerator, TypeVar, Union
from uuid import UUID

NodeType = TypeVar("Node")


class NodeManagerBase(ABC):
    def __init__(self):
        self._node_id = 1
        self._nodes = {}

    def add_node(self, src: int, node: NodeType):
        if src in self._nodes:
            raise ValueError(f"Node with ID {src} already exists")
        self._nodes[src] = node

    def get_node(self, uuid: Union[str, UUID]) -> Union[NodeType, None]:
        if isinstance(uuid, str):
            uuid = UUID(uuid)
        for node in self._nodes.values():
            if node.uuid == uuid:
                return node
        return None

    def get_node_by_src(self, node_id: int) -> Union[NodeType, None]:
        return self._nodes.get(node_id, None)

    @abstractmethod
    async def init(self):
        pass

    async def request_node(
        self, uuid: Union[str, UUID], timeout_s: float = 2.0
    ) -> Union[NodeType, None]:
        timeout = time.time() + timeout_s
        while time.time() < timeout:
            node = self.get_node(uuid)
            if node:
                return node
            await asyncio.sleep(0.1)
        return None

    def __iter__(self):
        return iter(self._nodes.values())

    def __aiter__(self):
        return aiter(self.nodes())

    @property
    def node_id(self) -> int:
        return self._node_id

    async def nodes(self) -> AsyncGenerator[NodeType, None]:
        if not self._nodes:
            # No nodes found. Sleep to wait for heartbeats
            await asyncio.sleep(1)
        for node in self._nodes.values():
            yield node
