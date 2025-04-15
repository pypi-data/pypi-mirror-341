# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class StatusBuilder:
    """
    Builds and executes requests for operations under /device/cellular/status
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_id: str, **kw) -> List[Any]:
        """
        Get cellular status list from device
        GET /dataservice/device/cellular/status

        :param device_id: Device IP
        :returns: List[Any]
        """
        params = {
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/cellular/status", return_type=List[Any], params=params, **kw
        )
