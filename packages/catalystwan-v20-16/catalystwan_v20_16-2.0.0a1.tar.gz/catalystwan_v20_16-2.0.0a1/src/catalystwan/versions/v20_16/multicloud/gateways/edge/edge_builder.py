# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any

from catalystwan.abc import RequestAdapterInterface


class EdgeBuilder:
    """
    Builds and executes requests for operations under /multicloud/gateways/edge
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, edge_type: str, **kw) -> Any:
        """
        Get sites with connectivity to the interconnect gateways by edge type
        GET /dataservice/multicloud/gateways/edge/{edgeType}

        :param edge_type: Edge type
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "getEdgeGateways")
        params = {
            "edgeType": edge_type,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/multicloud/gateways/edge/{edgeType}", params=params, **kw
        )
