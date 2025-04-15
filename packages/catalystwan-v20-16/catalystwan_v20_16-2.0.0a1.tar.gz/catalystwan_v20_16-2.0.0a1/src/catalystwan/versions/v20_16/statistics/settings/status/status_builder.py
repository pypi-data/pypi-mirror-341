# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .device.device_builder import DeviceBuilder


class StatusBuilder:
    """
    Builds and executes requests for operations under /statistics/settings/status
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Get statistics settings
        GET /dataservice/statistics/settings/status

        :returns: Any
        """
        return self._request_adapter.request("GET", "/dataservice/statistics/settings/status", **kw)

    def put(self, payload: Any, **kw):
        """
        Update statistics settings
        PUT /dataservice/statistics/settings/status

        :param payload: Stats setting
        :returns: None
        """
        return self._request_adapter.request(
            "PUT", "/dataservice/statistics/settings/status", payload=payload, **kw
        )

    @property
    def device(self) -> DeviceBuilder:
        """
        The device property
        """
        from .device.device_builder import DeviceBuilder

        return DeviceBuilder(self._request_adapter)
