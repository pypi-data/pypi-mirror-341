# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import AppRouteTunnenSummarResp


class HealthBuilder:
    """
    Builds and executes requests for operations under /statistics/approute/tunnels/health
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        type_: str,
        limit: Optional[int] = 10,
        last_n_hours: Optional[int] = 3,
        last_n_minutes: Optional[int] = None,
        device_ip: Optional[str] = None,
        site_id: Optional[str] = None,
        region_name: Optional[str] = None,
        **kw,
    ) -> List[AppRouteTunnenSummarResp]:
        """
        Get tunnel health
        GET /dataservice/statistics/approute/tunnels/health/{type}

        :param type_: Type
        :param limit: Limit
        :param last_n_hours: Last n hours
        :param last_n_minutes: Last n minutes
        :param device_ip: Device ip
        :param site_id: Site id
        :param region_name: Region name
        :returns: List[AppRouteTunnenSummarResp]
        """
        params = {
            "type": type_,
            "limit": limit,
            "last_n_hours": last_n_hours,
            "last_n_minutes": last_n_minutes,
            "deviceIP": device_ip,
            "site-id": site_id,
            "regionName": region_name,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/statistics/approute/tunnels/health/{type}",
            return_type=List[AppRouteTunnenSummarResp],
            params=params,
            **kw,
        )
