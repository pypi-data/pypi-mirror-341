# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import ApplicationHeatMapDetail, LastNHoursParam


class DetailBuilder:
    """
    Builds and executes requests for operations under /statistics/perfmon/application/heatmap/detail
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        application: str,
        start_time: int,
        heatmap_time: int,
        siteid: Optional[str] = None,
        last_n_hours: Optional[LastNHoursParam] = "12",
        **kw,
    ) -> List[ApplicationHeatMapDetail]:
        """
        Get single applicaiton site health detail in a time range
        GET /dataservice/statistics/perfmon/application/heatmap/detail

        :param application: Application
        :param siteid: Siteid
        :param start_time: Heatmap single box entry_time
        :param heatmap_time: Heatmap generation time
        :param last_n_hours: Last n hours
        :returns: List[ApplicationHeatMapDetail]
        """
        params = {
            "application": application,
            "siteid": siteid,
            "start_time": start_time,
            "heatmap_time": heatmap_time,
            "last_n_hours": last_n_hours,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/statistics/perfmon/application/heatmap/detail",
            return_type=List[ApplicationHeatMapDetail],
            params=params,
            **kw,
        )
