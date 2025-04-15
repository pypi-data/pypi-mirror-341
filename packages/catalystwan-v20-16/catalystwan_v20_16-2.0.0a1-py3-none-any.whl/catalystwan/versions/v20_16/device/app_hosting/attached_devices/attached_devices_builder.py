# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class AttachedDevicesBuilder:
    """
    Builds and executes requests for operations under /device/app-hosting/attached-devices
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_id: str, **kw) -> Any:
        """
        Get App hosting attached device from device
        GET /dataservice/device/app-hosting/attached-devices

        :param device_id: deviceId - Device IP
        :returns: Any
        """
        params = {
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/app-hosting/attached-devices", params=params, **kw
        )
