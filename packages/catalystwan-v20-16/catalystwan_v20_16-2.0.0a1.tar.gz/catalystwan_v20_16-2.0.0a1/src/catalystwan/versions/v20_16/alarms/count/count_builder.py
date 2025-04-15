# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import AlarmCountPost


class CountBuilder:
    """
    Builds and executes requests for operations under /alarms/count
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, include_tenants: Optional[bool] = None, **kw) -> Any:
        """
        Get the count of alarms which are active and not acknowledged by user.
        GET /dataservice/alarms/count

        :param include_tenants: include tenants
        :returns: Any
        """
        params = {
            "includeTenants": include_tenants,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/alarms/count", params=params, **kw
        )

    def post(
        self,
        payload: Any,
        site_id: Optional[str] = None,
        include_tenants: Optional[bool] = None,
        **kw,
    ) -> List[AlarmCountPost]:
        """
        Get the count of alarms as per the query passed.
        POST /dataservice/alarms/count

        :param site_id: Specify the site-id to filter the alarms
        :param include_tenants: Specify whether the tenant alarms need to be visible or not from provider view.
        :param payload: Query
        :returns: List[AlarmCountPost]
        """
        params = {
            "site-id": site_id,
            "includeTenants": include_tenants,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/alarms/count",
            return_type=List[AlarmCountPost],
            params=params,
            payload=payload,
            **kw,
        )
