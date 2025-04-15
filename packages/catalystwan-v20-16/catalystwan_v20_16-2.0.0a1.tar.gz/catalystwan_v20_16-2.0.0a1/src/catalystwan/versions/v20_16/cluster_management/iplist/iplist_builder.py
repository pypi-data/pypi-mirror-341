# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class IplistBuilder:
    """
    Builds and executes requests for operations under /clusterManagement/iplist
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, vmanage_id: str, **kw) -> List[Any]:
        """
        Get configured IP addresses


        Note: In a multitenant vManage system, this API is only available in the Provider view.
        GET /dataservice/clusterManagement/iplist/{vmanageID}

        :param vmanage_id: vManage Id
        :returns: List[Any]
        """
        params = {
            "vmanageID": vmanage_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/clusterManagement/iplist/{vmanageID}",
            return_type=List[Any],
            params=params,
            **kw,
        )
