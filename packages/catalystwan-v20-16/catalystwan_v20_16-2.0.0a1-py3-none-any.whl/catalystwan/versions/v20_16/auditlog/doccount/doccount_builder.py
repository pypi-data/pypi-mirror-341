# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import GetAuditLogDoccount


class DoccountBuilder:
    """
    Builds and executes requests for operations under /auditlog/doccount
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, query: str, **kw) -> GetAuditLogDoccount:
        """
        Get response count of a query
        GET /dataservice/auditlog/doccount

        :param query: Query
        :returns: GetAuditLogDoccount
        """
        params = {
            "query": query,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/auditlog/doccount",
            return_type=GetAuditLogDoccount,
            params=params,
            **kw,
        )

    def post(self, payload: Any, **kw) -> GetAuditLogDoccount:
        """
        Get response count of a query
        POST /dataservice/auditlog/doccount

        :param payload: Stats query string
        :returns: GetAuditLogDoccount
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/auditlog/doccount",
            return_type=GetAuditLogDoccount,
            payload=payload,
            **kw,
        )
