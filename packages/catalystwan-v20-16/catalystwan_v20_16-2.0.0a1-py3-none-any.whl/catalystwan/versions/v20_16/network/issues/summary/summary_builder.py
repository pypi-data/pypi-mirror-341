# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class SummaryBuilder:
    """
    Builds and executes requests for operations under /network/issues/summary
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Retrieve network issues summary
        GET /dataservice/network/issues/summary

        :returns: Any
        """
        return self._request_adapter.request("GET", "/dataservice/network/issues/summary", **kw)
