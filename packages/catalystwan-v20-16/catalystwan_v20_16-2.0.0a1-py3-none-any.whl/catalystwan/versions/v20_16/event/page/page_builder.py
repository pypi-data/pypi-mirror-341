# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import AlarmResponse


class PageBuilder:
    """
    Builds and executes requests for operations under /event/page
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        query: Optional[str] = None,
        scroll_id: Optional[str] = None,
        count: Optional[int] = None,
        site_id: Optional[str] = None,
        **kw,
    ) -> AlarmResponse:
        """
        Get paginated events
        GET /dataservice/event/page

        :param query: Query
        :param scroll_id: Scroll ID
        :param count: Number of alarms per page
        :param site_id: Specify the site-id to filter the events
        :returns: AlarmResponse
        """
        params = {
            "query": query,
            "scrollId": scroll_id,
            "count": count,
            "site-id": site_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/event/page", return_type=AlarmResponse, params=params, **kw
        )

    def post(
        self,
        payload: Any,
        scroll_id: Optional[str] = None,
        count: Optional[int] = None,
        site_id: Optional[str] = None,
        **kw,
    ) -> AlarmResponse:
        """
        Get paginated events
        POST /dataservice/event/page

        :param scroll_id: Scroll ID
        :param count: Number of alarms per page
        :param site_id: Specify the site-id to filter the events
        :param payload: Event query string
        :returns: AlarmResponse
        """
        params = {
            "scrollId": scroll_id,
            "count": count,
            "site-id": site_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/event/page",
            return_type=AlarmResponse,
            params=params,
            payload=payload,
            **kw,
        )
