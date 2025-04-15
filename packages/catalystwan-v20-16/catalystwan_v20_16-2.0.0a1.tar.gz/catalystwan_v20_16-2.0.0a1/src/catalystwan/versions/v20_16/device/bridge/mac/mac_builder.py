# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import IfNameParam


class MacBuilder:
    """
    Builds and executes requests for operations under /device/bridge/mac
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        device_id: str,
        bridge_id: Optional[str] = None,
        if_name: Optional[IfNameParam] = None,
        mac_address: Optional[str] = None,
        **kw,
    ) -> Any:
        """
        Get device bridge interface MAC (Real Time)
        GET /dataservice/device/bridge/mac

        :param bridge_id: Bridge ID
        :param if_name: Interface name
        :param mac_address: MAC address
        :param device_id: deviceId - Device IP
        :returns: Any
        """
        params = {
            "bridge-id": bridge_id,
            "if-name": if_name,
            "mac-address": mac_address,
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/bridge/mac", params=params, **kw
        )
