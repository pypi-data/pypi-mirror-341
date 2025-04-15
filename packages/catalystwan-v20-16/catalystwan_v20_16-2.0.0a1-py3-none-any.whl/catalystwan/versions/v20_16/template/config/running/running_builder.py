# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class RunningBuilder:
    """
    Builds and executes requests for operations under /template/config/running
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_id: str, **kw) -> Any:
        """
        Get device running config
        GET /dataservice/template/config/running/{deviceId}

        :param device_id: Device Model ID
        :returns: Any
        """
        params = {
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/template/config/running/{deviceId}", params=params, **kw
        )
