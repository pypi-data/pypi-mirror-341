import logging
from dbus_next.aio import MessageBus
from dbus_next.service import ServiceInterface, dbus_property
from dbus_next.constants import PropertyAccess

import asyncio

from openhydroponics.base.endpoint import Endpoint
from openhydroponics.net import Node, NodeManager
from openhydroponics.service.endpoint import wrap_endpoint


class NodeInterface(ServiceInterface):
    def __init__(self, bus: MessageBus, node: Node):
        super().__init__("com.openhydroponics.NodeInterface")
        self._bus = bus
        self._node = node
        self._endpoints = []
        for endpoint in node:
            endpoint_interface = EndpointInterface(self, endpoint)
            self._endpoints.append(endpoint_interface)
            self._bus.export(endpoint_interface.object_path, endpoint_interface)
            self._bus.export(
                endpoint_interface.object_path, endpoint_interface.wrapped_endpoint
            )

    @dbus_property(access=PropertyAccess.READ)
    def Interviewed(self) -> "b":
        return self._node.interviewed

    @property
    def object_path(self):
        return f"/com/openhydroponics/nodes/{str(self._node.uuid).replace('-', '_')}"

    @dbus_property(access=PropertyAccess.READ)
    def UUID(self) -> "s":
        return str(self._node.uuid)


class EndpointInterface(ServiceInterface):
    def __init__(self, node: NodeInterface, endpoint: Endpoint):
        super().__init__("com.openhydroponics.EndpointMetaDataInterface")
        self._node = node
        self._endpoint = endpoint
        self._wrapped_endoint = wrap_endpoint(endpoint)

    @property
    def wrapped_endpoint(self):
        return self._wrapped_endoint

    @dbus_property(access=PropertyAccess.READ)
    def EndpointClass(self) -> "u":
        return self._endpoint.ENDPOINT_CLASS

    @dbus_property(access=PropertyAccess.READ)
    def EndpointId(self) -> "u":
        return self._endpoint.endpoint_id

    @dbus_property(access=PropertyAccess.READ)
    def EndpointInterface(self) -> "s":
        return self._wrapped_endoint.DBUS_INTERFACE

    @property
    def object_path(self):
        return f"{self._node.object_path}/{self._endpoint.endpoint_id}"


class NodeManagerInterface(ServiceInterface):
    def __init__(self, bus):
        super().__init__("com.openhydroponics.NodeManager")
        self._bus: MessageBus = bus
        self._nm: NodeManager = NodeManager()
        self._nodes = []

    async def init(self):
        await self._nm.init()
        async for node in self._nm.nodes():
            node_interface = NodeInterface(self._bus, node)
            self._nodes.append(node_interface)
            self._bus.export(node_interface.object_path, node_interface)


async def main():
    logging.basicConfig(
        format="%(asctime)s %(name)-20s %(levelname)-7s: %(message)s",
        level=logging.DEBUG,
        datefmt="%H:%M:%S",
    )
    bus = await MessageBus().connect()

    interface = NodeManagerInterface(bus)
    await interface.init()

    bus.export("/com/openhydroponics/nodes", interface)
    await bus.request_name("com.openhydroponics")

    await bus.wait_for_disconnect()


def daemon():
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exiting...")


if __name__ == "__main__":
    daemon()
