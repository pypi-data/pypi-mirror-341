# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class FlowMonitorBuilder:
    """
    Builds and executes requests for operations under /device/cflowd/fnf/flow-monitor
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_id: str, **kw) -> Any:
        """
        Get FnF from device
        GET /dataservice/device/cflowd/fnf/flow-monitor

        :param device_id: Device IP
        :returns: Any
        """
        params = {
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/cflowd/fnf/flow-monitor", params=params, **kw
        )
