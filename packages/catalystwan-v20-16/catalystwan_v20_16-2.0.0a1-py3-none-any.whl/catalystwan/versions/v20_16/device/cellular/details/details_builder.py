# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import CellularDetail, LastNHoursParam


class DetailsBuilder:
    """
    Builds and executes requests for operations under /device/cellular/details
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, last_n_hours: Optional[LastNHoursParam] = None, **kw) -> List[CellularDetail]:
        """
        Cellular count dashlet details
        GET /dataservice/device/cellular/details

        :param last_n_hours: last N hours
        :returns: List[CellularDetail]
        """
        params = {
            "lastNHours": last_n_hours,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/device/cellular/details",
            return_type=List[CellularDetail],
            params=params,
            **kw,
        )
