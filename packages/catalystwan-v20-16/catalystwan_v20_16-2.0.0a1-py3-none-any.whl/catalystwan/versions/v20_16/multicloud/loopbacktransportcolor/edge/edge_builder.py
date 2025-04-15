# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any

from catalystwan.abc import RequestAdapterInterface


class EdgeBuilder:
    """
    Builds and executes requests for operations under /multicloud/loopbacktransportcolor/edge
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Get Edge Loopback Tunnel supported colors
        GET /dataservice/multicloud/loopbacktransportcolor/edge

        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "getSupportedLoopbackTransportColors")
        return self._request_adapter.request(
            "GET", "/dataservice/multicloud/loopbacktransportcolor/edge", **kw
        )
