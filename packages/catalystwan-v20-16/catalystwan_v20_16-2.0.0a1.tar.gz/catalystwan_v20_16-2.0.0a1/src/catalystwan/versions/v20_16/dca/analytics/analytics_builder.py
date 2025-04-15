# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .all.all_builder import AllBuilder


class AnalyticsBuilder:
    """
    Builds and executes requests for operations under /dca/analytics
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def put(self, payload: Any, **kw):
        """
        Update collection time of DCARest stat for vAnalytics
        PUT /dataservice/dca/analytics

        :param payload: Stats query
        :returns: None
        """
        return self._request_adapter.request(
            "PUT", "/dataservice/dca/analytics", payload=payload, **kw
        )

    @property
    def all(self) -> AllBuilder:
        """
        The all property
        """
        from .all.all_builder import AllBuilder

        return AllBuilder(self._request_adapter)
