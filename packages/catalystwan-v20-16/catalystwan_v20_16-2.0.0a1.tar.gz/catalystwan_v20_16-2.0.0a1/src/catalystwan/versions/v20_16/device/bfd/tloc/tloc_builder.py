# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .detail.detail_builder import DetailBuilder


class TlocBuilder:
    """
    Builds and executes requests for operations under /device/bfd/tloc
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_id: str, **kw) -> Any:
        """
        Get TLOC summary from device (Real Time)
        GET /dataservice/device/bfd/tloc

        :param device_id: deviceId - Device IP
        :returns: Any
        """
        params = {
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/bfd/tloc", params=params, **kw
        )

    @property
    def detail(self) -> DetailBuilder:
        """
        The detail property
        """
        from .detail.detail_builder import DetailBuilder

        return DetailBuilder(self._request_adapter)
