# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class DetailsBuilder:
    """
    Builds and executes requests for operations under /certificate/device/details
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> str:
        """
        Get device detail view
        GET /dataservice/certificate/device/details

        :returns: str
        """
        return self._request_adapter.request(
            "GET", "/dataservice/certificate/device/details", return_type=str, **kw
        )
