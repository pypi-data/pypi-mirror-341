# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import GetSitesResponse


class SiteBuilder:
    """
    Builds and executes requests for operations under /multicloud/site
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        color: Optional[str] = None,
        attached: Optional[str] = None,
        solution: Optional[str] = None,
        **kw,
    ) -> GetSitesResponse:
        """
        Get available sites
        GET /dataservice/multicloud/site

        :param color: color
        :param attached: Get attached Sites
        :param solution: Solution of branch device
        :returns: GetSitesResponse
        """
        params = {
            "color": color,
            "attached": attached,
            "solution": solution,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/multicloud/site", return_type=GetSitesResponse, params=params, **kw
        )
