# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import VpnIdParam


class GatewayexitsBuilder:
    """
    Builds and executes requests for operations under /device/cloudx/gatewayexits
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        device_id: str,
        vpn_id: Optional[VpnIdParam] = None,
        application: Optional[str] = None,
        **kw,
    ) -> Any:
        """
        Get list of cloudexpress gateway exits from device (Real Time)
        GET /dataservice/device/cloudx/gatewayexits

        :param vpn_id: VPN Id
        :param application: Application
        :param device_id: deviceId - Device IP
        :returns: Any
        """
        params = {
            "vpn-id": vpn_id,
            "application": application,
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/cloudx/gatewayexits", params=params, **kw
        )
