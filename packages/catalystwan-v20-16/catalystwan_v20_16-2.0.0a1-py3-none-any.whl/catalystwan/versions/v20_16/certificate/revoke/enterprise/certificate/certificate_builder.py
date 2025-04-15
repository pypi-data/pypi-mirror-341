# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class CertificateBuilder:
    """
    Builds and executes requests for operations under /certificate/revoke/enterprise/certificate
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: str, **kw) -> str:
        """
        Revoking enterprise CSR for hardware vEdge
        POST /dataservice/certificate/revoke/enterprise/certificate

        :param payload: JSON parameter with Device UUID
        :returns: str
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/certificate/revoke/enterprise/certificate",
            return_type=str,
            payload=payload,
            **kw,
        )
