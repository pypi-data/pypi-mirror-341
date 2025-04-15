# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class TlocInterfaceMapBuilder:
    """
    Builds and executes requests for operations under /device/bfd/state/device/tlocInterfaceMap
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_id: str, **kw) -> Any:
        """
        Get device tloc color to Intf Mapping Relationship
        GET /dataservice/device/bfd/state/device/tlocInterfaceMap

        :param device_id: deviceId - Device IP
        :returns: Any
        """
        params = {
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/bfd/state/device/tlocInterfaceMap", params=params, **kw
        )
