# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class DetailsBuilder:
    """
    Builds and executes requests for operations under /device/crashlog/details
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Get device crash logs for all device
        GET /dataservice/device/crashlog/details

        :returns: Any
        """
        return self._request_adapter.request("GET", "/dataservice/device/crashlog/details", **kw)
