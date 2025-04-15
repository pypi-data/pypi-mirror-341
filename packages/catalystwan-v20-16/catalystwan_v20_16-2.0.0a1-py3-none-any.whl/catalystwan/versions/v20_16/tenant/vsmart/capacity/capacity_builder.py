# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class CapacityBuilder:
    """
    Builds and executes requests for operations under /tenant/vsmart/capacity
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[Any]:
        """
        Lists all the vsmarts on the vManage and its tenant hosting capacity


        Note: In a multitenant vManage system, this API is only available in the Provider view.
        GET /dataservice/tenant/vsmart/capacity

        :returns: List[Any]
        """
        return self._request_adapter.request(
            "GET", "/dataservice/tenant/vsmart/capacity", return_type=List[Any], **kw
        )
