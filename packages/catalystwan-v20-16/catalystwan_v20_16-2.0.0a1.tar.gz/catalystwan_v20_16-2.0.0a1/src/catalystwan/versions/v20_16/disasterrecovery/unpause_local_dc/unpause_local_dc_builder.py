# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class UnpauseLocalDcBuilder:
    """
    Builds and executes requests for operations under /disasterrecovery/unpauseLocalDC
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, **kw) -> Any:
        """
        Unpause DR for Local datacenter
        POST /dataservice/disasterrecovery/unpauseLocalDC

        :returns: Any
        """
        return self._request_adapter.request(
            "POST", "/dataservice/disasterrecovery/unpauseLocalDC", **kw
        )
