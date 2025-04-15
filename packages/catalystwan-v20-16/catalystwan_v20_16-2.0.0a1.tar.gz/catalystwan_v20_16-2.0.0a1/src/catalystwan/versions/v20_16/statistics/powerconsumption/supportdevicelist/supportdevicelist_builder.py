# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import SupportedDeviceList


class SupportdevicelistBuilder:
    """
    Builds and executes requests for operations under /statistics/powerconsumption/supportdevicelist
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, last_n_hours: Optional[int] = 24, **kw) -> SupportedDeviceList:
        """
        Get power consumption collection supported device list
        GET /dataservice/statistics/powerconsumption/supportdevicelist

        :param last_n_hours: Last n hours
        :returns: SupportedDeviceList
        """
        params = {
            "last_n_hours": last_n_hours,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/statistics/powerconsumption/supportdevicelist",
            return_type=SupportedDeviceList,
            params=params,
            **kw,
        )
