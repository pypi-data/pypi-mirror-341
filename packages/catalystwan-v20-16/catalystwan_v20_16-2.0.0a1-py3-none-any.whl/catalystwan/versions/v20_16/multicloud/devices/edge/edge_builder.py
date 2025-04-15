# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface


class EdgeBuilder:
    """
    Builds and executes requests for operations under /multicloud/devices/edge
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, edge_type: str, edge_gateway_name: Optional[str] = None, **kw) -> Any:
        """
        Get cloud devices by cloud type
        GET /dataservice/multicloud/devices/edge/{edgeType}

        :param edge_type: Edge type
        :param edge_gateway_name: Edge Gateway Name
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "getCloudDevices_1")
        params = {
            "edgeType": edge_type,
            "edgeGatewayName": edge_gateway_name,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/multicloud/devices/edge/{edgeType}", params=params, **kw
        )
