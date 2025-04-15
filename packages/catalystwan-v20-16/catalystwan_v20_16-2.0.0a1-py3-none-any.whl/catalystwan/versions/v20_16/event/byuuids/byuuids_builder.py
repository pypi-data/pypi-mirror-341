# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List, Optional

from catalystwan.abc import RequestAdapterInterface


class ByuuidsBuilder:
    """
    Builds and executes requests for operations under /event/byuuids
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: List[None], time_filter: Optional[str] = None, **kw) -> Any:
        """
        Get Events for given uuids
        POST /dataservice/event/byuuids

        :param time_filter: Query
        :param payload: List of event uuids
        :returns: Any
        """
        params = {
            "timeFilter": time_filter,
        }
        return self._request_adapter.request(
            "POST", "/dataservice/event/byuuids", params=params, payload=payload, **kw
        )
