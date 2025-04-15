# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class CsrBuilder:
    """
    Builds and executes requests for operations under /sslproxy/generate/vmanage/csr
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw) -> Any:
        """
        Generate CSR
        POST /dataservice/sslproxy/generate/vmanage/csr

        :param payload: CSR request
        :returns: Any
        """
        return self._request_adapter.request(
            "POST", "/dataservice/sslproxy/generate/vmanage/csr", payload=payload, **kw
        )
