# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class CommonBuilder:
    """
    Builds and executes requests for operations under /statistics/cryptovpn/common
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw) -> List[Any]:
        """
        Get crypto vpn common data
        POST /dataservice/statistics/cryptovpn/common

        :param payload: Stats query string
        :returns: List[Any]
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/statistics/cryptovpn/common",
            return_type=List[Any],
            payload=payload,
            **kw,
        )
