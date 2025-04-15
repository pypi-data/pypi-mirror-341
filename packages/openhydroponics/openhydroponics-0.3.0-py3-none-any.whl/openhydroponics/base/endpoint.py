from enum import IntEnum
import logging
from typing import Any

_LOG = logging.getLogger(__name__)


class EndpointClass(IntEnum):
    NotSupported = 0
    Input = 1
    Output = 2


class EndpointInputClass(IntEnum):
    NotSupported = 0
    Temperature = 1
    Humidity = 2
    EC = 3


class EndpointOutputClass(IntEnum):
    NotSupported = 0
    Variable = 1
    Binary = 2


class Endpoint:
    ENDPOINT_CLASS = EndpointClass.NotSupported

    def __init__(self, node, endpoint_id):
        self._node = node
        self._endpoint_id = endpoint_id

    async def interview(self):
        pass

    @property
    def node(self):
        return self._node

    @property
    def endpoint_id(self):
        return self._endpoint_id

    async def set_config(self, config: dict[str, Any]):
        pass


class InputEndpoint(Endpoint):
    ENDPOINT_CLASS = EndpointClass.Input
    INPUT_CLASS = EndpointInputClass.NotSupported

    def __init__(self, node, endpoint_id):
        super().__init__(node, endpoint_id)
        self._value = None
        self._scale = None

    def handle_sensor_reading(self, msg):
        self._value = msg.value
        self._scale = msg.scale

    @property
    def value(self):
        return self._value

    @property
    def scale(self):
        return self._scale


class TemperatureEndpoint(InputEndpoint):
    INPUT_CLASS = EndpointInputClass.Temperature


class HumidityEndpoint(InputEndpoint):
    INPUT_CLASS = EndpointInputClass.Humidity


class OutputEndpoint(Endpoint):
    ENDPOINT_CLASS = EndpointClass.Output
    OUTPUT_CLASS = EndpointOutputClass.NotSupported


class VariableOutputEndpoint(OutputEndpoint):
    OUTPUT_CLASS = EndpointOutputClass.Variable


class ECConfigType(IntEnum):
    LOW = 0
    HIGH = 1
    GAIN = 2


class ECEndpoint(InputEndpoint):
    INPUT_CLASS = EndpointInputClass.EC
