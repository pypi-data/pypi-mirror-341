# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import SecurityDeviceHealth


class HealthBuilder:
    """
    Builds and executes requests for operations under /security/device/health
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_ip: Optional[str] = None, **kw) -> List[SecurityDeviceHealth]:
        """
        Get security device health
        GET /dataservice/security/device/health

        :param device_ip: deviceIp - Device IP
        :returns: List[SecurityDeviceHealth]
        """
        params = {
            "deviceIp": device_ip,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/security/device/health",
            return_type=List[SecurityDeviceHealth],
            params=params,
            **kw,
        )
