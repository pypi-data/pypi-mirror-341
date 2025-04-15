# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import SdraHeadendSummary


class HeadendsBuilder:
    """
    Builds and executes requests for operations under /statistics/sdra/headends
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, site: Optional[int] = None, **kw) -> SdraHeadendSummary:
        """
        Get SD-WAN Remote Access Head-end summary
        GET /dataservice/statistics/sdra/headends

        :param site: Site
        :returns: SdraHeadendSummary
        """
        params = {
            "site": site,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/statistics/sdra/headends",
            return_type=SdraHeadendSummary,
            params=params,
            **kw,
        )
