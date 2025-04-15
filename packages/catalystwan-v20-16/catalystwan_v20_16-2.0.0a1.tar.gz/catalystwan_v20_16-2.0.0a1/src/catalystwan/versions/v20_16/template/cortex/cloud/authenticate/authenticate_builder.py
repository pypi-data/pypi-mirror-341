# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class AuthenticateBuilder:
    """
    Builds and executes requests for operations under /template/cortex/cloud/authenticate
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw):
        """
        Authenticate Cloud Account Credentials
        POST /dataservice/template/cortex/cloud/authenticate

        :param payload: Credential
        :returns: None
        """
        return self._request_adapter.request(
            "POST", "/dataservice/template/cortex/cloud/authenticate", payload=payload, **kw
        )
