# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class DetailsBuilder:
    """
    Builds and executes requests for operations under /dca/device/crashlog/details
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw) -> Any:
        """
        Get crash log
        POST /dataservice/dca/device/crashlog/details

        :param payload: Query string
        :returns: Any
        """
        return self._request_adapter.request(
            "POST", "/dataservice/dca/device/crashlog/details", payload=payload, **kw
        )
