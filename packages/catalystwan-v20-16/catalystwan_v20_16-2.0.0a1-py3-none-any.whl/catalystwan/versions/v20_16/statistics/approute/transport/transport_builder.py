# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import AppRouteTransportResp

if TYPE_CHECKING:
    from .summary.summary_builder import SummaryBuilder


class TransportBuilder:
    """
    Builds and executes requests for operations under /statistics/approute/transport
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self, type_: str, limit: int, query: Optional[str] = None, **kw
    ) -> AppRouteTransportResp:
        """
        Get application-aware routing statistics from device
        GET /dataservice/statistics/approute/transport/{type}

        :param type_: Type
        :param query: Query filter
        :param limit: Limit
        :returns: AppRouteTransportResp
        """
        params = {
            "type": type_,
            "query": query,
            "limit": limit,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/statistics/approute/transport/{type}",
            return_type=AppRouteTransportResp,
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
