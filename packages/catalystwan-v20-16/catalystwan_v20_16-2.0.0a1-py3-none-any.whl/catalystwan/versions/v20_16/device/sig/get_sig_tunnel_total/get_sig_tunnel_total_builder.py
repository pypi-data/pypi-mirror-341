# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class GetSigTunnelTotalBuilder:
    """
    Builds and executes requests for operations under /device/sig/getSigTunnelTotal
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        get Sig Tunnel Total coount
        GET /dataservice/device/sig/getSigTunnelTotal

        :returns: Any
        """
        return self._request_adapter.request(
            "GET", "/dataservice/device/sig/getSigTunnelTotal", **kw
        )
