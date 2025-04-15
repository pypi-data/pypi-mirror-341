# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DeviceAppResponse


class ApplicationsBuilder:
    """
    Builds and executes requests for operations under /statistics/dpi/device/applications
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, query: str, limit: Optional[int] = None, **kw) -> DeviceAppResponse:
        """
        Get DPI application flows device aggregation data
        GET /dataservice/statistics/dpi/device/applications

        :param query: Query
        :param limit: Limit
        :returns: DeviceAppResponse
        """
        params = {
            "query": query,
            "limit": limit,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/statistics/dpi/device/applications",
            return_type=DeviceAppResponse,
            params=params,
            **kw,
        )
