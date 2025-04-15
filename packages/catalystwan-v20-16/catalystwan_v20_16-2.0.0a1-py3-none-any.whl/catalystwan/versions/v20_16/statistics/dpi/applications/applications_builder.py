# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DpiAppResponse

if TYPE_CHECKING:
    from .summary.summary_builder import SummaryBuilder


class ApplicationsBuilder:
    """
    Builds and executes requests for operations under /statistics/dpi/applications
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, query: str, limit: Optional[int] = None, **kw) -> DpiAppResponse:
        """
        Get detailed DPI application flows list in a grid table
        GET /dataservice/statistics/dpi/applications

        :param query: Query
        :param limit: Limit
        :returns: DpiAppResponse
        """
        params = {
            "query": query,
            "limit": limit,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/statistics/dpi/applications",
            return_type=DpiAppResponse,
            params=params,
            **kw,
        )

    @property
    def summary(self) -> SummaryBuilder:
        """
        The summary property
        """
        from .summary.summary_builder import SummaryBuilder

        return SummaryBuilder(self._request_adapter)
