# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional

from catalystwan.abc import RequestAdapterInterface


class DetailBuilder:
    """
    Builds and executes requests for operations under /certificate/stats/detail
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self, status: Optional[str] = None, include_tenantv_smart: Optional[bool] = None, **kw
    ) -> List[str]:
        """
        Get certificate details
        GET /dataservice/certificate/stats/detail

        :param status: Certificate Status
        :param include_tenantv_smart: include tenant vSmart
        :returns: List[str]
        """
        params = {
            "status": status,
            "includeTenantvSmart": include_tenantv_smart,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/certificate/stats/detail",
            return_type=List[str],
            params=params,
            **kw,
        )
