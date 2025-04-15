# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class IpaddressBuilder:
    """
    Builds and executes requests for operations under /monitor/sdavccloudconnector/ipaddress
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Get SD AVC App Rules based on IP Address for O365
        GET /dataservice/monitor/sdavccloudconnector/ipaddress

        :returns: Any
        """
        return self._request_adapter.request(
            "GET", "/dataservice/monitor/sdavccloudconnector/ipaddress", **kw
        )
