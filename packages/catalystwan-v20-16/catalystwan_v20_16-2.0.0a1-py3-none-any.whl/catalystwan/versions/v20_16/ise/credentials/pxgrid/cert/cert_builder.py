# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class CertBuilder:
    """
    Builds and executes requests for operations under /ise/credentials/pxgrid/cert
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> str:
        """
        Retrieves Pxgrid Certificate
        GET /dataservice/ise/credentials/pxgrid/cert

        :returns: str
        """
        return self._request_adapter.request(
            "GET", "/dataservice/ise/credentials/pxgrid/cert", return_type=str, **kw
        )
