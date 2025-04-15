# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class StatusBuilder:
    """
    Builds and executes requests for operations under /dca/statistics/settings/status
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw) -> Any:
        """
        Get statistics setting status
        POST /dataservice/dca/statistics/settings/status

        :param payload: Stats setting
        :returns: Any
        """
        return self._request_adapter.request(
            "POST", "/dataservice/dca/statistics/settings/status", payload=payload, **kw
        )
