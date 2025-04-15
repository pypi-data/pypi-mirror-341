# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import CellularHealth, LastNHoursParam, TypeParam


class HealthBuilder:
    """
    Builds and executes requests for operations under /device/cellular/health
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        type_: Optional[TypeParam] = None,
        last_n_hours: Optional[LastNHoursParam] = None,
        **kw,
    ) -> List[CellularHealth]:
        """
        Cellular Health Dashlet
        GET /dataservice/device/cellular/health

        :param type_: type
        :param last_n_hours: last N hours
        :returns: List[CellularHealth]
        """
        params = {
            "type": type_,
            "lastNHours": last_n_hours,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/device/cellular/health",
            return_type=List[CellularHealth],
            params=params,
            **kw,
        )
