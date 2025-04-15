# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DeviceHealthHistoryItem


class HistoryBuilder:
    """
    Builds and executes requests for operations under /statistics/devicehealth/history
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        last_n_hours: Optional[int] = 12,
        site: Optional[str] = None,
        limit: Optional[int] = 30,
        **kw,
    ) -> List[DeviceHealthHistoryItem]:
        """
        Get all device health history
        GET /dataservice/statistics/devicehealth/history

        :param last_n_hours: Last n hours
        :param site: Site
        :param limit: Limit
        :returns: List[DeviceHealthHistoryItem]
        """
        params = {
            "last_n_hours": last_n_hours,
            "site": site,
            "limit": limit,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/statistics/devicehealth/history",
            return_type=List[DeviceHealthHistoryItem],
            params=params,
            **kw,
        )
