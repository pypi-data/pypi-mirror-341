# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class CredentialsBuilder:
    """
    Builds and executes requests for operations under /cloudservices/credentials
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Get cloud service credentials
        GET /dataservice/cloudservices/credentials

        :returns: Any
        """
        return self._request_adapter.request("GET", "/dataservice/cloudservices/credentials", **kw)

    def post(self, payload: Any, **kw):
        """
        Add cloud service credentials
        POST /dataservice/cloudservices/credentials

        :param payload: Cloud service credentials
        :returns: None
        """
        return self._request_adapter.request(
            "POST", "/dataservice/cloudservices/credentials", payload=payload, **kw
        )
