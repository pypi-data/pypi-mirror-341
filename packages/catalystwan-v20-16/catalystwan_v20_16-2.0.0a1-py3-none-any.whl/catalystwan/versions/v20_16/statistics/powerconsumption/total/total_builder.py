# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import PowerConsumptionTotalResp


class TotalBuilder:
    """
    Builds and executes requests for operations under /statistics/powerconsumption/total
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw) -> PowerConsumptionTotalResp:
        """
        Get Power Consumption Total stats
        POST /dataservice/statistics/powerconsumption/total

        :param payload: Stats query string
        :returns: PowerConsumptionTotalResp
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/statistics/powerconsumption/total",
            return_type=PowerConsumptionTotalResp,
            payload=payload,
            **kw,
        )
