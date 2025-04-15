# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class RemoveBuilder:
    """
    Builds and executes requests for operations under /clusterManagement/remove
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw):
        """
        Remove vManage from cluster


        Note: In a multitenant vManage system, this API is only available in the Provider view.
        POST /dataservice/clusterManagement/remove

        :param payload: vManage server info
        :returns: None
        """
        return self._request_adapter.request(
            "POST", "/dataservice/clusterManagement/remove", payload=payload, **kw
        )
