# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class CertificateBuilder:
    """
    Builds and executes requests for operations under /sslproxy/settings/certificate
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Get certificate state
        GET /dataservice/sslproxy/settings/certificate

        :returns: Any
        """
        return self._request_adapter.request(
            "GET", "/dataservice/sslproxy/settings/certificate", **kw
        )
