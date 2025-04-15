# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any

from catalystwan.abc import RequestAdapterInterface


class GetTransitDevicePairAndHostListBuilder:
    """
    Builds and executes requests for operations under /template/cor/getTransitDevicePairAndHostList
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, account_id: str, cloud_region: str, **kw) -> Any:
        """
        Get device and host details
        GET /dataservice/template/cor/getTransitDevicePairAndHostList

        :param account_id: Account Id
        :param cloud_region: Cloud region
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "getTransitDevicePairAndHostList")
        params = {
            "accountId": account_id,
            "cloudRegion": cloud_region,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/template/cor/getTransitDevicePairAndHostList", params=params, **kw
        )
