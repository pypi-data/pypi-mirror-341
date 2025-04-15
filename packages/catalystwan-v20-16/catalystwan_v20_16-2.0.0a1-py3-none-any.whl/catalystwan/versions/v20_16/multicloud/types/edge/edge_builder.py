# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any

from catalystwan.abc import RequestAdapterInterface


class EdgeBuilder:
    """
    Builds and executes requests for operations under /multicloud/types/edge
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Get edge types
        GET /dataservice/multicloud/types/edge

        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "getEdgeTypes")
        return self._request_adapter.request("GET", "/dataservice/multicloud/types/edge", **kw)
