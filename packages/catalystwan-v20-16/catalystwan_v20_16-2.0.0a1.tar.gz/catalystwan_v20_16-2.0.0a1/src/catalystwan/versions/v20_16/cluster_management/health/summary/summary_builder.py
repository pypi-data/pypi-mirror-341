# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface


class SummaryBuilder:
    """
    Builds and executes requests for operations under /clusterManagement/health/summary
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, is_cached: Optional[bool] = False, site_id: Optional[str] = None, **kw) -> Any:
        """
        Get cluster health check summary


        Note: In a multitenant vManage system, this API is only available in the Provider view.
        GET /dataservice/clusterManagement/health/summary

        :param is_cached: Flag to enable cached result
        :param site_id: Optional site ID  to filter devices
        :returns: Any
        """
        params = {
            "isCached": is_cached,
            "site-id": site_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/clusterManagement/health/summary", params=params, **kw
        )
