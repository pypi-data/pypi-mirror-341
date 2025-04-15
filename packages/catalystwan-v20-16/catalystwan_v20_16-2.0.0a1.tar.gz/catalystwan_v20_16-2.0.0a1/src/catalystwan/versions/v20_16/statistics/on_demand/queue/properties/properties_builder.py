# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class PropertiesBuilder:
    """
    Builds and executes requests for operations under /statistics/on-demand/queue/properties
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        gets current size of on-demand queue
        GET /dataservice/statistics/on-demand/queue/properties

        :returns: Any
        """
        return self._request_adapter.request(
            "GET", "/dataservice/statistics/on-demand/queue/properties", **kw
        )
