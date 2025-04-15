# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class RmalistBuilder:
    """
    Builds and executes requests for operations under /template/config/rmalist
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, old_device_id: str, **kw) -> List[Any]:
        """
        Get compatible devices of model, chassis number, certificate serial number with the old device
        GET /dataservice/template/config/rmalist/{oldDeviceId}

        :param old_device_id: Device Model ID
        :returns: List[Any]
        """
        params = {
            "oldDeviceId": old_device_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/template/config/rmalist/{oldDeviceId}",
            return_type=List[Any],
            params=params,
            **kw,
        )
