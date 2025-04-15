# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class RootCertBuilder:
    """
    Builds and executes requests for operations under /certificate/forcesync/rootCert
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, **kw) -> str:
        """
        force Sync RootCert to all devices
        POST /dataservice/certificate/forcesync/rootCert

        :returns: str
        """
        return self._request_adapter.request(
            "POST", "/dataservice/certificate/forcesync/rootCert", return_type=str, **kw
        )
