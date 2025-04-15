import asyncio
import logging
import time
from typing import Any
from uuid import UUID
from pypostcard.types import List, u8
from pypostcard.serde import to_postcard

from openhydroponics.base import NodeManagerBase, NodeBase


from .phyinterface import CanPhyIface
import openhydroponics.net.msg as Msg
from openhydroponics.net.msg import ArbitrationId
from openhydroponics.net.endpoint import get_endpoint_class

_LOG = logging.getLogger(__name__)


class Node(NodeBase):
    def __init__(
        self, node_id: int, uuid: UUID, manager: NodeManagerBase, phy_iface: CanPhyIface
    ):
        super().__init__(uuid)
        self._manager = manager
        self._node_id = node_id
        self._phy_iface = phy_iface
        self._last_heartbeat = time.time()

    async def interview(self):
        if self.number_of_endpoints == -1:
            self.send_rtr(Msg.NodeInfo)
            resp = await self.wait_for(Msg.NodeInfo)
            if not resp:
                return
            self.number_of_endpoints = resp.number_of_endpoints
        for endpoint in range(self.number_of_endpoints):
            endpoint_info = await self.send_and_wait(
                Msg.EndpointInfoRequest(endpoint_id=u8(endpoint))
            )
            if not endpoint_info:
                continue
            EndpointClass = get_endpoint_class(
                endpoint_info.endpoint_class, endpoint_info.endpoint_sub_class
            )
            self._endpoints[endpoint] = EndpointClass(self, endpoint)
            await self._endpoints[endpoint].interview()

    @property
    def interviewed(self) -> bool:
        return self.number_of_endpoints == len(self.endpoints)

    def handle_sensor_reading(self, msg: Msg.SensorReading):
        endpoint = self.get_endpoint(msg.endpoint_id)
        if not endpoint:
            return
        endpoint.handle_sensor_reading(msg)

    @property
    def node_id(self) -> int:
        return self._node_id

    async def send_and_wait(self, request: Any):
        assert request.MSG_TYPE == Msg.MsgType.Request
        response = Msg.Msg.get_msg_cls(request.MSG_ID, Msg.MsgType.Response)
        assert response
        self.send_msg(request)
        return await self.wait_for(response)

    def send_msg(self, msg: Any):
        arb = ArbitrationId(
            prio=False,
            dst=self._node_id,
            master=True,  # We are the master
            src=self._manager.node_id,
            multiframe=False,
            msg_type=msg.MSG_TYPE,
            msg_id=msg.MSG_ID,
        )
        data = Msg.Msg.encode(msg)
        self._phy_iface.send_message(arb.encode(), data)

    def send_rtr(self, msg: Any):
        arb = ArbitrationId(
            prio=False,
            dst=self._node_id,
            master=True,  # We are the master
            src=self._manager.node_id,
            multiframe=False,
            msg_type=Msg.MsgType.Request,
            msg_id=msg.MSG_ID,
        )
        self._phy_iface.send_message(arb.encode(), b"", is_remote=True)

    async def set_config(self, config_no: int, config):
        cfg = to_postcard(config)
        cfg = cfg + bytes([0] * (32 - len(cfg)))
        msg = Msg.EndpointConfigRequest(
            endpoint_id=u8(self.node_id),
            config_no=u8(config_no),
            config=List(list(cfg)),
        )
        self.send_msg(msg)

    async def wait_for(self, msg: Any):
        arb = ArbitrationId(
            prio=False,
            dst=self._manager.node_id,
            master=False,
            src=self._node_id,
            multiframe=False,
            msg_type=msg.MSG_TYPE,
            msg_id=msg.MSG_ID,
        )
        try:
            frame = await self._phy_iface.wait_for(arb.encode())
            return Msg.Msg.decode(arb, frame.data)
        except asyncio.TimeoutError:
            _LOG.error("Timeout waiting for frame. Arb: %s", arb)
        return None
