# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class AccesstokenBuilder:
    """
    Builds and executes requests for operations under /dca/cloudservices/accesstoken
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Get DCA access token
        GET /dataservice/dca/cloudservices/accesstoken

        :returns: Any
        """
        return self._request_adapter.request(
            "GET", "/dataservice/dca/cloudservices/accesstoken", **kw
        )

    def post(self, payload: Any, **kw):
        """
        Set DCA access token
        POST /dataservice/dca/cloudservices/accesstoken

        :param payload: DCA access token
        :returns: None
        """
        return self._request_adapter.request(
            "POST", "/dataservice/dca/cloudservices/accesstoken", payload=payload, **kw
        )
