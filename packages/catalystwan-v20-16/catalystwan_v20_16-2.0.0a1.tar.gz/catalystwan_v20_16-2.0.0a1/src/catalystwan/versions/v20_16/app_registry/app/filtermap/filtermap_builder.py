# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class FiltermapBuilder:
    """
    Builds and executes requests for operations under /app-registry/app/filtermap
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[Any]:
        """
        Get all available filters for applist
        GET /dataservice/app-registry/app/filtermap

        :returns: List[Any]
        """
        return self._request_adapter.request(
            "GET", "/dataservice/app-registry/app/filtermap", return_type=List[Any], **kw
        )
