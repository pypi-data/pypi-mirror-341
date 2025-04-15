# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DeviceIp


class SessionBuilder:
    """
    Builds and executes requests for operations under /device/pppoe/session
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_id: DeviceIp, **kw) -> Any:
        """
        Get PPPoE session list from device
        GET /dataservice/device/pppoe/session

        :param device_id: deviceId - Device IP
        :returns: Any
        """
        params = {
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/pppoe/session", params=params, **kw
        )
