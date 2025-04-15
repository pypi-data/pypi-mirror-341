# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any

from catalystwan.abc import RequestAdapterInterface


class SettingBuilder:
    """
    Builds and executes requests for operations under /multicloud/gateway/edge/setting
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, edge_gateway_name: str, **kw) -> Any:
        """
        Get Interconnect Gateway custom setting by Interconnect Gateway name
        GET /dataservice/multicloud/gateway/edge/setting/{edgeGatewayName}

        :param edge_gateway_name: Edge gateway name
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "getIcgwCustomSettingDetails")
        params = {
            "edgeGatewayName": edge_gateway_name,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/gateway/edge/setting/{edgeGatewayName}",
            params=params,
            **kw,
        )
