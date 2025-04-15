# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import PowerConsumptionEnergyMixResp


class EnergymixBuilder:
    """
    Builds and executes requests for operations under /statistics/powerconsumption/energymix
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw) -> PowerConsumptionEnergyMixResp:
        """
        Get Power Consumption Energy Mix
        POST /dataservice/statistics/powerconsumption/energymix

        :param payload: Stats query string
        :returns: PowerConsumptionEnergyMixResp
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/statistics/powerconsumption/energymix",
            return_type=PowerConsumptionEnergyMixResp,
            payload=payload,
            **kw,
        )
