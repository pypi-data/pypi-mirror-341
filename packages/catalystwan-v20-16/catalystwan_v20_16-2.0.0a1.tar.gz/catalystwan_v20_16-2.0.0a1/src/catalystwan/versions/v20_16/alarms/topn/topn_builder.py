# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface


class TopnBuilder:
    """
    Builds and executes requests for operations under /alarms/topn
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        payload: Any,
        site_id: Optional[str] = None,
        include_tenants: Optional[bool] = None,
        **kw,
    ) -> Any:
        """
        Returns top-n alarm count based on given query
        POST /dataservice/alarms/topn

        :param site_id: Specify the site-id to filter the alarms
        :param include_tenants: Specify whether the tenant alarms need to be visible or not from provider view.
        :param payload: Input query
        :returns: Any
        """
        params = {
            "site-id": site_id,
            "includeTenants": include_tenants,
        }
        return self._request_adapter.request(
            "POST", "/dataservice/alarms/topn", params=params, payload=payload, **kw
        )
