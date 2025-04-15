# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import ApplicationSiteItem, HealthParam


class HealthBuilder:
    """
    Builds and executes requests for operations under /statistics/perfmon/application/site/health
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, payload: Any, health: Optional[HealthParam] = None, **kw
    ) -> List[ApplicationSiteItem]:
        """
        Get one application health for one site
        POST /dataservice/statistics/perfmon/application/site/health

        :param health: Health
        :param payload: Stats query string
        :returns: List[ApplicationSiteItem]
        """
        params = {
            "health": health,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/statistics/perfmon/application/site/health",
            return_type=List[ApplicationSiteItem],
            params=params,
            payload=payload,
            **kw,
        )
