# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class AvailableappsBuilder:
    """
    Builds and executes requests for operations under /template/cloudx/availableapps
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[Any]:
        """
        Get CloudX available apps list
        GET /dataservice/template/cloudx/availableapps

        :returns: List[Any]
        """
        return self._request_adapter.request(
            "GET", "/dataservice/template/cloudx/availableapps", return_type=List[Any], **kw
        )
