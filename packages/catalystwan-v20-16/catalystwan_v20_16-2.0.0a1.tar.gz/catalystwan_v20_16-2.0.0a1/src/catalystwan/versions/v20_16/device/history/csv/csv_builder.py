# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional

from catalystwan.abc import RequestAdapterInterface


class CsvBuilder:
    """
    Builds and executes requests for operations under /device/history/csv
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, query: Optional[str] = None, **kw) -> str:
        """
        Get raw data with optional query as CSV
        GET /dataservice/device/history/csv

        :param query: Query string
        :returns: str
        """
        params = {
            "query": query,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/history/csv", return_type=str, params=params, **kw
        )
