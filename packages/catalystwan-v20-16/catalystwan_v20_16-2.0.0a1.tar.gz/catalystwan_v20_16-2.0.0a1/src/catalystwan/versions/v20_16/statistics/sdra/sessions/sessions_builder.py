# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import SdraSessionSummary


class SessionsBuilder:
    """
    Builds and executes requests for operations under /statistics/sdra/sessions
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, site: Optional[int] = None, **kw) -> SdraSessionSummary:
        """
        Get SD-WAN Remote Access session summary
        GET /dataservice/statistics/sdra/sessions

        :param site: Site
        :returns: SdraSessionSummary
        """
        params = {
            "site": site,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/statistics/sdra/sessions",
            return_type=SdraSessionSummary,
            params=params,
            **kw,
        )
