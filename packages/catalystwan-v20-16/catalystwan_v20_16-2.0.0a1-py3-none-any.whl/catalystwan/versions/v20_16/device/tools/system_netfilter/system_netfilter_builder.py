# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class SystemNetfilterBuilder:
    """
    Builds and executes requests for operations under /device/tools/system-netfilter
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_id: str, **kw) -> Any:
        """
        Get system netfilter info from device
        GET /dataservice/device/tools/system-netfilter

        :param device_id: Device Id
        :returns: Any
        """
        params = {
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/tools/system-netfilter", params=params, **kw
        )
