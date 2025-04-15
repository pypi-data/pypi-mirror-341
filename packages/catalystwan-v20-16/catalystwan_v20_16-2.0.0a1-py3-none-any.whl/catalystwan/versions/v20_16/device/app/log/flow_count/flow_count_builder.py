# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class FlowCountBuilder:
    """
    Builds and executes requests for operations under /device/app/log/flow-count
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_id: str, **kw) -> Any:
        """
        Get App log flows count from device (Real Time)
        GET /dataservice/device/app/log/flow-count

        :param device_id: Device IP
        :returns: Any
        """
        params = {
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/app/log/flow-count", params=params, **kw
        )
