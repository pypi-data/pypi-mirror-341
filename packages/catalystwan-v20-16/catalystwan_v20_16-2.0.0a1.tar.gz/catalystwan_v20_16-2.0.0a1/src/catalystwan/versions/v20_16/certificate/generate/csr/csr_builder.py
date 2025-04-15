# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class CsrBuilder:
    """
    Builds and executes requests for operations under /certificate/generate/csr
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw) -> str:
        """
        get certificaate details
        POST /dataservice/certificate/generate/csr

        :param payload: Device IP
        :returns: str
        """
        return self._request_adapter.request(
            "POST", "/dataservice/certificate/generate/csr", return_type=str, payload=payload, **kw
        )
