# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class DetailsBuilder:
    """
    Builds and executes requests for operations under /clusterManagement/vManage/details
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, vmanage_ip: str, **kw) -> Any:
        """
        Get vManage detail


        Note: In a multitenant vManage system, this API is only available in the Provider view.
        GET /dataservice/clusterManagement/vManage/details/{vmanageIP}

        :param vmanage_ip: vManage IP
        :returns: Any
        """
        params = {
            "vmanageIP": vmanage_ip,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/clusterManagement/vManage/details/{vmanageIP}", params=params, **kw
        )
