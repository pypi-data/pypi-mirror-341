# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import CellularDataUsage, LastNHoursParam


class DataUsageBuilder:
    """
    Builds and executes requests for operations under /device/cellular/dataUsage
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        last_n_hours: Optional[LastNHoursParam] = None,
        drill_down: Optional[bool] = None,
        **kw,
    ) -> List[CellularDataUsage]:
        """
        Cellular DataUsage Dashlet
        GET /dataservice/device/cellular/dataUsage

        :param last_n_hours: last N hours
        :param drill_down: drill down
        :returns: List[CellularDataUsage]
        """
        params = {
            "lastNHours": last_n_hours,
            "drillDown": drill_down,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/device/cellular/dataUsage",
            return_type=List[CellularDataUsage],
            params=params,
            **kw,
        )
