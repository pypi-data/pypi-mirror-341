# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import EdgeTypeParam


class TypesBuilder:
    """
    Builds and executes requests for operations under /multicloud/gateway/edge/types
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, edge_type: Optional[EdgeTypeParam] = None, **kw) -> Any:
        """
        Get Interconnect Gateway type for specified Edge Provider
        GET /dataservice/multicloud/gateway/edge/types

        :param edge_type: Edge type
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "getIcgwTypes")
        params = {
            "edgeType": edge_type,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/multicloud/gateway/edge/types", params=params, **kw
        )
