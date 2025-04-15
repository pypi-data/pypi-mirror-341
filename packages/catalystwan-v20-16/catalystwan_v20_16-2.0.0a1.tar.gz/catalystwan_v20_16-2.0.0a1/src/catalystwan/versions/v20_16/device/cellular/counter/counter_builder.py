# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import CellularCount, LastNHoursParam, TypeParam


class CounterBuilder:
    """
    Builds and executes requests for operations under /device/cellular/counter
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        type_: Optional[TypeParam] = None,
        last_n_hours: Optional[LastNHoursParam] = None,
        **kw,
    ) -> List[CellularCount]:
        """
        Cellular count dashlet
        GET /dataservice/device/cellular/counter

        :param type_: type
        :param last_n_hours: last N Hours
        :returns: List[CellularCount]
        """
        params = {
            "type": type_,
            "lastNHours": last_n_hours,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/device/cellular/counter",
            return_type=List[CellularCount],
            params=params,
            **kw,
        )
