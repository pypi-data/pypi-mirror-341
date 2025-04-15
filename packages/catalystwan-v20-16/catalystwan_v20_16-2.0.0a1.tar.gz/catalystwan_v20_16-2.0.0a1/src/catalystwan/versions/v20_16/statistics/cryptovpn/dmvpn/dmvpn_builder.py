# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class DmvpnBuilder:
    """
    Builds and executes requests for operations under /statistics/cryptovpn/dmvpn
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw) -> List[Any]:
        """
        Get crypto vpn dmvpn data
        POST /dataservice/statistics/cryptovpn/dmvpn

        :param payload: Stats query string
        :returns: List[Any]
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/statistics/cryptovpn/dmvpn",
            return_type=List[Any],
            payload=payload,
            **kw,
        )
