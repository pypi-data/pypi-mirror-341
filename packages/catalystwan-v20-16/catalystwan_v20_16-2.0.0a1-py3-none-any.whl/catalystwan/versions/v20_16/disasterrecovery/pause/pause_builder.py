# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class PauseBuilder:
    """
    Builds and executes requests for operations under /disasterrecovery/pause
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, **kw) -> Any:
        """
        Pause DR
        POST /dataservice/disasterrecovery/pause

        :returns: Any
        """
        return self._request_adapter.request("POST", "/dataservice/disasterrecovery/pause", **kw)
