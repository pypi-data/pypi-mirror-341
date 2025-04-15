# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .list.list_builder import ListBuilder


class UsersBuilder:
    """
    Builds and executes requests for operations under /device/users
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_id: str, **kw) -> List[Any]:
        """
        Get users from device (Real Time)
        GET /dataservice/device/users

        :param device_id: Device IP
        :returns: List[Any]
        """
        params = {
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/users", return_type=List[Any], params=params, **kw
        )

    @property
    def list(self) -> ListBuilder:
        """
        The list property
        """
        from .list.list_builder import ListBuilder

        return ListBuilder(self._request_adapter)
