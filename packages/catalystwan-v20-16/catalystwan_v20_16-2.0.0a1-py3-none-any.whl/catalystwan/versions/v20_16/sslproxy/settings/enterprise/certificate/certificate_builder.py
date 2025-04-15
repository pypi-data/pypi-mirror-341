# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class CertificateBuilder:
    """
    Builds and executes requests for operations under /sslproxy/settings/enterprise/certificate
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Get enterprise certificate
        GET /dataservice/sslproxy/settings/enterprise/certificate

        :returns: Any
        """
        return self._request_adapter.request(
            "GET", "/dataservice/sslproxy/settings/enterprise/certificate", **kw
        )

    def post(self, payload: Any, **kw) -> Any:
        """
        Configure enterprise certificate
        POST /dataservice/sslproxy/settings/enterprise/certificate

        :param payload: Config enterprise certificate request
        :returns: Any
        """
        return self._request_adapter.request(
            "POST", "/dataservice/sslproxy/settings/enterprise/certificate", payload=payload, **kw
        )
