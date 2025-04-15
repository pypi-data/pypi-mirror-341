# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class UpdateDrConfigOnArbitratorBuilder:
    """
    Builds and executes requests for operations under /disasterrecovery/updateDRConfigOnArbitrator
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, **kw) -> Any:
        """
        Update arbitrator with primary and secondary states cluster
        POST /dataservice/disasterrecovery/updateDRConfigOnArbitrator

        :returns: Any
        """
        return self._request_adapter.request(
            "POST", "/dataservice/disasterrecovery/updateDRConfigOnArbitrator", **kw
        )
