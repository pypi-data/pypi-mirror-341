from uuid import UUID

from dbus_next.aio import MessageBus

from openhydroponics.base import NodeManagerBase
from openhydroponics.dbus import Node

BUS_NAME = "com.openhydroponics"


class NodeManager(NodeManagerBase):
    def __init__(self):
        super().__init__()
        self._bus = None

    async def init(self):
        self._bus = await MessageBus().connect()

        introspection = await self._bus.introspect(
            BUS_NAME, "/com/openhydroponics/nodes"
        )

        proxy_object = self._bus.get_proxy_object(
            BUS_NAME, "/com/openhydroponics/nodes", introspection
        )

        self._interface = proxy_object.get_interface("com.openhydroponics.NodeManager")
        for child in introspection.nodes:
            path = f"{introspection.name}/{child.name}"
            introspection = await self._bus.introspect(BUS_NAME, path)
            proxy_object = self._bus.get_proxy_object(BUS_NAME, path, introspection)

            interface = proxy_object.get_interface("com.openhydroponics.NodeInterface")
            uuid = UUID(await interface.get_uuid())
            node = Node(uuid, proxy_object)
            await node.init(self._bus, introspection)
            self.add_node(uuid, node)
