# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class CustomApplicationBuilder:
    """
    Builds and executes requests for operations under /sdavc/protocol-pack/compliance/custom-application
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Get All Custom Applications
        GET /dataservice/sdavc/protocol-pack/compliance/custom-application

        :returns: Any
        """
        return self._request_adapter.request(
            "GET", "/dataservice/sdavc/protocol-pack/compliance/custom-application", **kw
        )
