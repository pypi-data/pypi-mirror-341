# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import PowerConsumptionDeviceResp


class DeviceBuilder:
    """
    Builds and executes requests for operations under /statistics/powerconsumption/device
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw) -> PowerConsumptionDeviceResp:
        """
        Get Power Consumption Per Device stats
        POST /dataservice/statistics/powerconsumption/device

        :param payload: Stats query string
        :returns: PowerConsumptionDeviceResp
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/statistics/powerconsumption/device",
            return_type=PowerConsumptionDeviceResp,
            payload=payload,
            **kw,
        )
