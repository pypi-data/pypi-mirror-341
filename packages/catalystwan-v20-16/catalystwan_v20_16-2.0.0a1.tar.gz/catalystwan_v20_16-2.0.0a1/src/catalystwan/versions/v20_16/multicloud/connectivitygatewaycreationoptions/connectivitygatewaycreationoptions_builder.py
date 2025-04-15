# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface


class ConnectivitygatewaycreationoptionsBuilder:
    """
    Builds and executes requests for operations under /multicloud/connectivitygatewaycreationoptions
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        account_id: Optional[str] = None,
        cloud_type: Optional[str] = None,
        connectivity_type: Optional[str] = None,
        refresh: Optional[str] = None,
        **kw,
    ) -> Any:
        """
        Get connectivity gateway creation options
        GET /dataservice/multicloud/connectivitygatewaycreationoptions

        :param account_id: Account Id
        :param cloud_type: Cloud Type
        :param connectivity_type: Cloud Connectivity Type
        :param refresh: Refresh
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "getConnectivityGatewayCreationOptions")
        params = {
            "accountId": account_id,
            "cloudType": cloud_type,
            "connectivityType": connectivity_type,
            "refresh": refresh,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/multicloud/connectivitygatewaycreationoptions", params=params, **kw
        )
