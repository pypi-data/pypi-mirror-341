# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import EdgeTypeParam, ProductTypeParam


class EdgeBuilder:
    """
    Builds and executes requests for operations under /multicloud/license/edge
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        edge_type: Optional[EdgeTypeParam] = None,
        account_id: Optional[str] = None,
        product_type: Optional[ProductTypeParam] = None,
        refresh: Optional[str] = None,
        **kw,
    ) -> Any:
        """
        Get License Info for Edge Gateways/Connections
        GET /dataservice/multicloud/license/edge

        :param edge_type: Edge type
        :param account_id: Edge Account Id
        :param product_type: product Type
        :param refresh: Refresh License Cache from Megaport
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "getLicenses")
        params = {
            "edgeType": edge_type,
            "accountId": account_id,
            "productType": product_type,
            "refresh": refresh,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/multicloud/license/edge", params=params, **kw
        )
