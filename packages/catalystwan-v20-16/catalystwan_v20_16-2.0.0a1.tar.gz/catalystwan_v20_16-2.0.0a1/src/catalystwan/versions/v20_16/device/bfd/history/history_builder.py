# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import ColorParam


class HistoryBuilder:
    """
    Builds and executes requests for operations under /device/bfd/history
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        device_id: str,
        system_ip: Optional[str] = None,
        color: Optional[ColorParam] = None,
        **kw,
    ) -> List[Any]:
        """
        Get BFD session history from device (Real Time)
        GET /dataservice/device/bfd/history

        :param system_ip: System IP
        :param color: Remote color
        :param device_id: deviceId - Device IP
        :returns: List[Any]
        """
        params = {
            "system-ip": system_ip,
            "color": color,
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/bfd/history", return_type=List[Any], params=params, **kw
        )
