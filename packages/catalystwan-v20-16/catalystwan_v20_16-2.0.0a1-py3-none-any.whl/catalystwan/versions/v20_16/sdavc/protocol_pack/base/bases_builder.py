# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class BasesBuilder:
    """
    Builds and executes requests for operations under /sdavc/protocol-pack/base
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Get all base protocol pack details
        GET /dataservice/sdavc/protocol-pack/base

        :returns: Any
        """
        return self._request_adapter.request("GET", "/dataservice/sdavc/protocol-pack/base", **kw)
