# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import InterconnectDashboard


class DashboardBuilder:
    """
    Builds and executes requests for operations under /multicloud/interconnect/dashboard
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[InterconnectDashboard]:
        """
        API to retrieve Multicloud Interconnect dashboard view.
        GET /dataservice/multicloud/interconnect/dashboard

        :returns: List[InterconnectDashboard]
        """
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/interconnect/dashboard",
            return_type=List[InterconnectDashboard],
            **kw,
        )
