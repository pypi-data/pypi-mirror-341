# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class DashboardlistBuilder:
    """
    Builds and executes requests for operations under /cloudservices/vanalytics/dashboardlist
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Get vAnalytics Dashboard List
        GET /dataservice/cloudservices/vanalytics/dashboardlist

        :returns: Any
        """
        return self._request_adapter.request(
            "GET", "/dataservice/cloudservices/vanalytics/dashboardlist", **kw
        )
