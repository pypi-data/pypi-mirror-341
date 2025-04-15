# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import ApplicationSiteChartItem


class AggregationBuilder:
    """
    Builds and executes requests for operations under /statistics/perfmon/aggregation
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: str, **kw) -> List[ApplicationSiteChartItem]:
        """
        Get one application one site line chart data
        POST /dataservice/statistics/perfmon/aggregation

        :param payload: Stats query string
        :returns: List[ApplicationSiteChartItem]
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/statistics/perfmon/aggregation",
            return_type=List[ApplicationSiteChartItem],
            payload=payload,
            **kw,
        )
