# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class TunnelDashboardBuilder:
    """
    Builds and executes requests for operations under /device/sig/tunnelDashboard
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Get SIG Zscaler tunnels from device
        GET /dataservice/device/sig/tunnelDashboard

        :returns: Any
        """
        return self._request_adapter.request("GET", "/dataservice/device/sig/tunnelDashboard", **kw)
