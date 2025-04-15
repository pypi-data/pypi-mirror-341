# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class IsdnstatusBuilder:
    """
    Builds and executes requests for operations under /device/voiceisdninfo/isdnstatus
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_id: str, **kw) -> Any:
        """
        Retrieve Voice ISDN Status from device
        GET /dataservice/device/voiceisdninfo/isdnstatus

        :param device_id: deviceId - Device IP
        :returns: Any
        """
        params = {
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/voiceisdninfo/isdnstatus", params=params, **kw
        )
