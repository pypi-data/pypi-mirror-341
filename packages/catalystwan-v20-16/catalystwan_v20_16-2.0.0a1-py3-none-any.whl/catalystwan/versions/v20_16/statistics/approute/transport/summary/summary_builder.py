# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import AppRouteFecAggRespInner


class SummaryBuilder:
    """
    Builds and executes requests for operations under /statistics/approute/transport/summary
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        type_: str,
        limit: Optional[int] = 5,
        query: Optional[str] = None,
        site_id: Optional[str] = None,
        **kw,
    ) -> List[AppRouteFecAggRespInner]:
        """
        Get application-aware routing statistics summary from device
        GET /dataservice/statistics/approute/transport/summary/{type}

        :param type_: Type
        :param limit: Limit
        :param query: Query
        :param site_id: Site id
        :returns: List[AppRouteFecAggRespInner]
        """
        params = {
            "type": type_,
            "limit": limit,
            "query": query,
            "site-id": site_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/statistics/approute/transport/summary/{type}",
            return_type=List[AppRouteFecAggRespInner],
            params=params,
            **kw,
        )
