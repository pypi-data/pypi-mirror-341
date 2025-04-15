# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class TelemetryBuilder:
    """
    Builds and executes requests for operations under /dca/cloudservices/telemetry
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Get DCA telemetry settings
        GET /dataservice/dca/cloudservices/telemetry

        :returns: Any
        """
        return self._request_adapter.request(
            "GET", "/dataservice/dca/cloudservices/telemetry", **kw
        )
