# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, List

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .html.html_builder import HtmlBuilder


class ConfigBuilder:
    """
    Builds and executes requests for operations under /device/config
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_id: List[str], **kw) -> str:
        """
        Get device running configuration
        GET /dataservice/device/config

        :param device_id: Device Id list
        :returns: str
        """
        params = {
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/config", return_type=str, params=params, **kw
        )

    @property
    def html(self) -> HtmlBuilder:
        """
        The html property
        """
        from .html.html_builder import HtmlBuilder

        return HtmlBuilder(self._request_adapter)
