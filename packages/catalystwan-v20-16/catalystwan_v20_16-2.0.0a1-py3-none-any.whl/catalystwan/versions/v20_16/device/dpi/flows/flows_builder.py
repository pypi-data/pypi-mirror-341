# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import VpnIdParam


class FlowsBuilder:
    """
    Builds and executes requests for operations under /device/dpi/flows
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        device_id: str,
        vpn_id: Optional[VpnIdParam] = None,
        src_ip: Optional[str] = None,
        application: Optional[str] = None,
        family: Optional[str] = None,
        **kw,
    ) -> List[Any]:
        """
        Get DPI flow list from device (Real Time)
        GET /dataservice/device/dpi/flows

        :param vpn_id: VPN Id
        :param src_ip: Source IP
        :param application: Application
        :param family: Family
        :param device_id: deviceId - Device IP
        :returns: List[Any]
        """
        params = {
            "vpn-id": vpn_id,
            "src-ip": src_ip,
            "application": application,
            "family": family,
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/dpi/flows", return_type=List[Any], params=params, **kw
        )
