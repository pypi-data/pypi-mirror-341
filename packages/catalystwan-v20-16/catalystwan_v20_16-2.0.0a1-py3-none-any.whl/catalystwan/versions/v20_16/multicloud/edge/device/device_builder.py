# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import EdgeTypeParam


class DeviceBuilder:
    """
    Builds and executes requests for operations under /multicloud/edge/{edgeType}/device
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, edge_type: EdgeTypeParam, **kw) -> Any:
        """
        Get available WAN edge devices
        GET /dataservice/multicloud/edge/{edgeType}/device

        :param edge_type: Edge Type
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "getEdgeWanDevices")
        params = {
            "edgeType": edge_type,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/multicloud/edge/{edgeType}/device", params=params, **kw
        )
