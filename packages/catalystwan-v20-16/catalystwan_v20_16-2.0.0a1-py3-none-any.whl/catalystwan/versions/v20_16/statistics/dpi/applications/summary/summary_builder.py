# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DpiAppResponse


class SummaryBuilder:
    """
    Builds and executes requests for operations under /statistics/dpi/applications/summary
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self, query: str, limit: Optional[int] = None, site_id: Optional[str] = None, **kw
    ) -> DpiAppResponse:
        """
        Get detailed DPI application flows summary
        GET /dataservice/statistics/dpi/applications/summary

        :param query: Query
        :param limit: Limit
        :param site_id: Site id
        :returns: DpiAppResponse
        """
        params = {
            "query": query,
            "limit": limit,
            "site-id": site_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/statistics/dpi/applications/summary",
            return_type=DpiAppResponse,
            params=params,
            **kw,
        )
