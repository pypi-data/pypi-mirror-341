# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import GetAuditLogData


class PageBuilder:
    """
    Builds and executes requests for operations under /auditlog/page
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, query: str, count: int, scroll_id: Optional[str] = None, **kw) -> GetAuditLogData:
        """
        Get raw property data in bulk
        GET /dataservice/auditlog/page

        :param query: Query
        :param scroll_id: Scroll id
        :param count: Count
        :returns: GetAuditLogData
        """
        params = {
            "query": query,
            "scrollId": scroll_id,
            "count": count,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/auditlog/page", return_type=GetAuditLogData, params=params, **kw
        )

    def post(
        self, count: int, payload: Any, scroll_id: Optional[str] = None, **kw
    ) -> GetAuditLogData:
        """
        Get raw property data in bulk with post action
        POST /dataservice/auditlog/page

        :param scroll_id: Scroll id
        :param count: Count
        :param payload: Stats query string
        :returns: GetAuditLogData
        """
        params = {
            "scrollId": scroll_id,
            "count": count,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/auditlog/page",
            return_type=GetAuditLogData,
            params=params,
            payload=payload,
            **kw,
        )
