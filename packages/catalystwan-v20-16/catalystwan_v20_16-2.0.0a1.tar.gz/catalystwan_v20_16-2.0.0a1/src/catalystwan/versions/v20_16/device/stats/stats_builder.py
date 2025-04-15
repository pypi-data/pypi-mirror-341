# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class StatsBuilder:
    """
    Builds and executes requests for operations under /device/stats
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Get stats queue information
        GET /dataservice/device/stats

        :returns: Any
        """
        return self._request_adapter.request("GET", "/dataservice/device/stats", **kw)
