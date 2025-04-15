# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class ValidvsmartsBuilder:
    """
    Builds and executes requests for operations under /device/control/validvsmarts
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_id: str, **kw) -> List[Any]:
        """
        Get valid vSmart list from device (Real Time)
        GET /dataservice/device/control/validvsmarts

        :param device_id: deviceId - Device IP
        :returns: List[Any]
        """
        params = {
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/device/control/validvsmarts",
            return_type=List[Any],
            params=params,
            **kw,
        )
