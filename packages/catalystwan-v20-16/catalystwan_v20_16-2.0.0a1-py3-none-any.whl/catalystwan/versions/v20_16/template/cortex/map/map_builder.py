# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class MapBuilder:
    """
    Builds and executes requests for operations under /template/cortex/map
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, accountid: str, cloudregion: str, **kw) -> Any:
        """
        Get Mapped WAN Resource Groups
        GET /dataservice/template/cortex/map

        :param accountid: Account Id
        :param cloudregion: Cloud region
        :returns: Any
        """
        params = {
            "accountid": accountid,
            "cloudregion": cloudregion,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/template/cortex/map", params=params, **kw
        )
