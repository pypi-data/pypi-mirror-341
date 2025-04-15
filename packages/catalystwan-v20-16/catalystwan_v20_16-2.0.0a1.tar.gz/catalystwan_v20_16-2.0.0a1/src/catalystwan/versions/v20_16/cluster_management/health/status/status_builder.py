# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class StatusBuilder:
    """
    Builds and executes requests for operations under /clusterManagement/health/status
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Get cluster health check details


        Note: In a multitenant vManage system, this API is only available in the Provider view.
        GET /dataservice/clusterManagement/health/status

        :returns: Any
        """
        return self._request_adapter.request(
            "GET", "/dataservice/clusterManagement/health/status", **kw
        )
