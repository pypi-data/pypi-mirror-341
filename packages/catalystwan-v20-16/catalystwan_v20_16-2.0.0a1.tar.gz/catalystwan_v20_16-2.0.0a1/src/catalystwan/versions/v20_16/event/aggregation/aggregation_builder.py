# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import AlarmAggregationResponse


class AggregationBuilder:
    """
    Builds and executes requests for operations under /event/aggregation
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        query: str,
        site_id: Optional[str] = None,
        include_tenants: Optional[bool] = None,
        **kw,
    ) -> AlarmAggregationResponse:
        """
        Get aggregated count of events based on given query.
        GET /dataservice/event/aggregation

        :param query: Query
        :param site_id: Specify the site-id to filter the events
        :param include_tenants: Include tenants
        :returns: AlarmAggregationResponse
        """
        params = {
            "query": query,
            "site-id": site_id,
            "includeTenants": include_tenants,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/event/aggregation",
            return_type=AlarmAggregationResponse,
            params=params,
            **kw,
        )

    def post(
        self,
        payload: Any,
        site_id: Optional[str] = None,
        include_tenants: Optional[bool] = None,
        **kw,
    ) -> AlarmAggregationResponse:
        """
        Get aggregated count of events based on given query.
        POST /dataservice/event/aggregation

        :param site_id: Specify the site-id to filter the events
        :param include_tenants: Include tenants
        :param payload: Query
        :returns: AlarmAggregationResponse
        """
        params = {
            "site-id": site_id,
            "includeTenants": include_tenants,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/event/aggregation",
            return_type=AlarmAggregationResponse,
            params=params,
            payload=payload,
            **kw,
        )
