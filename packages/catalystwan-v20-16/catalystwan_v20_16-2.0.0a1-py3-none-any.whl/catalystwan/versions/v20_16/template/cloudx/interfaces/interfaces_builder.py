# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class InterfacesBuilder:
    """
    Builds and executes requests for operations under /template/cloudx/interfaces
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw):
        """
        Enable cloudx gateway
        POST /dataservice/template/cloudx/interfaces

        :param payload: Cloudx
        :returns: None
        """
        return self._request_adapter.request(
            "POST", "/dataservice/template/cloudx/interfaces", payload=payload, **kw
        )
