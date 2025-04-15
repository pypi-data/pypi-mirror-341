# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class VanalyticsBuilder:
    """
    Builds and executes requests for operations under /dca/cloudservices/vanalytics
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: str, **kw) -> Any:
        """
        Get session from DCS for vAnalytics
        POST /dataservice/dca/cloudservices/vanalytics

        :param payload: Payload
        :returns: Any
        """
        return self._request_adapter.request(
            "POST", "/dataservice/dca/cloudservices/vanalytics", payload=payload, **kw
        )
