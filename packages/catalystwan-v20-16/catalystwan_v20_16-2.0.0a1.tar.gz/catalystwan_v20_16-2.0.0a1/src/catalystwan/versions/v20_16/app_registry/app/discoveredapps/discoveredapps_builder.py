# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class DiscoveredappsBuilder:
    """
    Builds and executes requests for operations under /app-registry/app/discoveredapps
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[Any]:
        """
        Get All network discovered apps
        GET /dataservice/app-registry/app/discoveredapps

        :returns: List[Any]
        """
        return self._request_adapter.request(
            "GET", "/dataservice/app-registry/app/discoveredapps", return_type=List[Any], **kw
        )
