# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import EdgeTypeParam


class EdgeBuilder:
    """
    Builds and executes requests for operations under /multicloud/billingaccounts/edge
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self, edge_type: EdgeTypeParam, edge_account_id: str, region: Optional[str] = None, **kw
    ) -> Any:
        """
        Get Edge Billing Accounts
        GET /dataservice/multicloud/billingaccounts/edge/{edgeType}/{edgeAccountId}

        :param edge_type: Interconnect Provider
        :param edge_account_id: Interconnect Provider Account ID
        :param region: Region
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "getEdgeBillingAccounts")
        params = {
            "edgeType": edge_type,
            "edgeAccountId": edge_account_id,
            "region": region,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/billingaccounts/edge/{edgeType}/{edgeAccountId}",
            params=params,
            **kw,
        )
