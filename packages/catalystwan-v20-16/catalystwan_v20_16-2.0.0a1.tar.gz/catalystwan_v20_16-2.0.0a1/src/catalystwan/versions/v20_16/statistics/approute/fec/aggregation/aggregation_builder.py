# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import AppRouteFecAggRespInner


class AggregationBuilder:
    """
    Builds and executes requests for operations under /statistics/approute/fec/aggregation
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, payload: Any, site_id: Optional[str] = None, **kw
    ) -> List[AppRouteFecAggRespInner]:
        """
        Get aggregation data and fec recovery rate
        POST /dataservice/statistics/approute/fec/aggregation

        :param site_id: Site id
        :param payload: Query filter
        :returns: List[AppRouteFecAggRespInner]
        """
        params = {
            "site-id": site_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/statistics/approute/fec/aggregation",
            return_type=List[AppRouteFecAggRespInner],
            params=params,
            payload=payload,
            **kw,
        )
