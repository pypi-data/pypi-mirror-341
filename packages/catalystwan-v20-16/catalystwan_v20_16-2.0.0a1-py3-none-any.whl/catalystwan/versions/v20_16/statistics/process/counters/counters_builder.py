# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class CountersBuilder:
    """
    Builds and executes requests for operations under /statistics/process/counters
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[Any]:
        """
        Get statistics processing counters
        GET /dataservice/statistics/process/counters

        :returns: List[Any]
        """
        return self._request_adapter.request(
            "GET", "/dataservice/statistics/process/counters", return_type=List[Any], **kw
        )
