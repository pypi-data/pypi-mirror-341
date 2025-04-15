# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class CertstatusBuilder:
    """
    Builds and executes requests for operations under /certificate/controller/certstatus
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> str:
        """
        invalidate the device
        GET /dataservice/certificate/controller/certstatus

        :returns: str
        """
        return self._request_adapter.request(
            "GET", "/dataservice/certificate/controller/certstatus", return_type=str, **kw
        )
