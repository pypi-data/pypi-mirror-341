# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import ApplicationsSitesItem, HealthParam, LastNHoursParam


class HealthBuilder:
    """
    Builds and executes requests for operations under /statistics/perfmon/applications/sites/health
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        is_heat_map: Optional[bool] = None,
        last_n_hours: Optional[LastNHoursParam] = None,
        health: Optional[HealthParam] = None,
        include_usage: Optional[bool] = False,
        use_cache: Optional[bool] = True,
        **kw,
    ) -> List[ApplicationsSitesItem]:
        """
        Get applications health for all sites
        GET /dataservice/statistics/perfmon/applications/sites/health

        :param is_heat_map: Is heat map
        :param last_n_hours: Last n hours
        :param health: Health
        :param include_usage: Include usage
        :param use_cache: Use cache data
        :returns: List[ApplicationsSitesItem]
        """
        params = {
            "isHeatMap": is_heat_map,
            "last_n_hours": last_n_hours,
            "health": health,
            "includeUsage": include_usage,
            "useCache": use_cache,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/statistics/perfmon/applications/sites/health",
            return_type=List[ApplicationsSitesItem],
            params=params,
            **kw,
        )
