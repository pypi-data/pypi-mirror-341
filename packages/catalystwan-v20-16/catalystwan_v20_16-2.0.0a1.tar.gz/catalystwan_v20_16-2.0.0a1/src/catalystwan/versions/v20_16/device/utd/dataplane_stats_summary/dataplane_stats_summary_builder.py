# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class DataplaneStatsSummaryBuilder:
    """
    Builds and executes requests for operations under /device/utd/dataplane-stats-summary
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_id: str, **kw) -> Any:
        """
        Get data plane stats summary
        GET /dataservice/device/utd/dataplane-stats-summary

        :param device_id: deviceId - Device IP
        :returns: Any
        """
        params = {
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/utd/dataplane-stats-summary", params=params, **kw
        )
