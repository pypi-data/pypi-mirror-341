# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List, Optional

from catalystwan.abc import RequestAdapterInterface


class SummaryBuilder:
    """
    Builds and executes requests for operations under /event/severity/summary
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self, device_id: List[str], query: Optional[str] = None, site_id: Optional[str] = None, **kw
    ) -> Any:
        """
        Get event severity histogram
        GET /dataservice/event/severity/summary

        :param device_id: Device system ip
        :param query: Query
        :param site_id: Specify the site-id to filter the events
        :returns: Any
        """
        params = {
            "deviceId": device_id,
            "query": query,
            "site-id": site_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/event/severity/summary", params=params, **kw
        )
