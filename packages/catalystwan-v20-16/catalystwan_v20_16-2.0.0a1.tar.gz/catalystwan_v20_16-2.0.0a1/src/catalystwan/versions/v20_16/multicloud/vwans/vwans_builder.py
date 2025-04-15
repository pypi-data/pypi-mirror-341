# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface


class VwansBuilder:
    """
    Builds and executes requests for operations under /multicloud/vwans
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        account_id: Optional[str] = None,
        cloud_type: Optional[str] = None,
        resource_group: Optional[str] = None,
        refresh: Optional[str] = None,
        **kw,
    ) -> Any:
        """
        Get Virtual Wans
        GET /dataservice/multicloud/vwans

        :param account_id: Account Id
        :param cloud_type: Cloud Type
        :param resource_group: Resource Group
        :param refresh: Refresh
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "getVWans")
        params = {
            "accountId": account_id,
            "cloudType": cloud_type,
            "resourceGroup": resource_group,
            "refresh": refresh,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/multicloud/vwans", params=params, **kw
        )
