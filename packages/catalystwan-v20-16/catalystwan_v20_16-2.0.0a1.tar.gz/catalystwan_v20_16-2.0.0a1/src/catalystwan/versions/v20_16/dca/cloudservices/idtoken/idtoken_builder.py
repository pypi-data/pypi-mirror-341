# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class IdtokenBuilder:
    """
    Builds and executes requests for operations under /dca/cloudservices/idtoken
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Get DCA Id token
        GET /dataservice/dca/cloudservices/idtoken

        :returns: Any
        """
        return self._request_adapter.request("GET", "/dataservice/dca/cloudservices/idtoken", **kw)

    def post(self, payload: Any, **kw):
        """
        Set DCA Id token
        POST /dataservice/dca/cloudservices/idtoken

        :param payload: DCA Id token
        :returns: None
        """
        return self._request_adapter.request(
            "POST", "/dataservice/dca/cloudservices/idtoken", payload=payload, **kw
        )
