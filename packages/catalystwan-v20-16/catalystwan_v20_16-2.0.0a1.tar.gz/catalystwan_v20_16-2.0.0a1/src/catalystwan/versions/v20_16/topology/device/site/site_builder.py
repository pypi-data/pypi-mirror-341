# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class SiteBuilder:
    """
    Builds and executes requests for operations under /topology/device/site
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, site_id: str, **kw) -> Any:
        """
        Get topology for a given site id
        GET /dataservice/topology/device/site/{siteId}

        :param site_id: Site Id
        :returns: Any
        """
        params = {
            "siteId": site_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/topology/device/site/{siteId}", params=params, **kw
        )
