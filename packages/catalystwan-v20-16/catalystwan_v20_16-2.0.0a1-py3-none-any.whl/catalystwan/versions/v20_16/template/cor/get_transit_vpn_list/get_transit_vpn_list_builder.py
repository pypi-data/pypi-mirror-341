# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class GetTransitVpnListBuilder:
    """
    Builds and executes requests for operations under /template/cor/getTransitVpnList
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, account_id: str, **kw) -> List[Any]:
        """
        Get transit VPN list
        GET /dataservice/template/cor/getTransitVpnList

        :param account_id: Account Id
        :returns: List[Any]
        """
        logging.warning("Operation: %s is deprecated", "getTransitVpcVpnList")
        params = {
            "accountId": account_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/template/cor/getTransitVpnList",
            return_type=List[Any],
            params=params,
            **kw,
        )
