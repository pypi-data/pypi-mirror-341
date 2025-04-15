from abc import ABC, abstractmethod
from typing import Tuple, Union
from uuid import UUID

from openhydroponics.base.endpoint import Endpoint


class NodeBase(ABC):
    def __init__(self, uuid: UUID):
        self._endpoints = {}
        self._uuid = uuid
        self._number_of_endpoints = -1

    @property
    def endpoints(self):
        return self._endpoints

    def get_endpoint(self, endpoint_id: int) -> Union[Endpoint, None]:
        return self._endpoints.get(endpoint_id)

    def get_endpoint_value(self, endpoint_id: int) -> Tuple[float, int]:
        endpoint = self._endpoints.get(endpoint_id)
        if not endpoint:
            return (None, None)
        return endpoint.value, endpoint.scale

    @property
    def number_of_endpoints(self) -> int:
        return self._number_of_endpoints

    @number_of_endpoints.setter
    def number_of_endpoints(self, value: int):
        self._number_of_endpoints = value

    @property
    def uuid(self) -> UUID:
        return self._uuid

    def __iter__(self):
        return iter(self._endpoints.values())
