# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class GetcertificateBuilder:
    """
    Builds and executes requests for operations under /setting/configuration/webserver/certificate/getcertificate
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> str:
        """
        Get certificate for alias server
        GET /dataservice/setting/configuration/webserver/certificate/getcertificate

        :returns: str
        """
        return self._request_adapter.request(
            "GET",
            "/dataservice/setting/configuration/webserver/certificate/getcertificate",
            return_type=str,
            **kw,
        )
