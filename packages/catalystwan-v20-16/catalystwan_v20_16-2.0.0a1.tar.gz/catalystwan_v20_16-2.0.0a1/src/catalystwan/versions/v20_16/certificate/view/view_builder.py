# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class ViewBuilder:
    """
    Builds and executes requests for operations under /certificate/view
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> str:
        """
        Get certificate UI view
        GET /dataservice/certificate/view

        :returns: str
        """
        return self._request_adapter.request(
            "GET", "/dataservice/certificate/view", return_type=str, **kw
        )
