# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import VpnIdParam


class FlowsCountBuilder:
    """
    Builds and executes requests for operations under /device/cflowd/flows-count
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        device_id: str,
        vpn_id: Optional[VpnIdParam] = None,
        src_ip: Optional[str] = None,
        dest_ip: Optional[str] = None,
        **kw,
    ) -> Any:
        """
        Get cflowd flow count from device
        GET /dataservice/device/cflowd/flows-count

        :param vpn_id: VPN Id
        :param src_ip: Source IP
        :param dest_ip: Destination IP
        :param device_id: Device IP
        :returns: Any
        """
        params = {
            "vpn-id": vpn_id,
            "src-ip": src_ip,
            "dest-ip": dest_ip,
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/cflowd/flows-count", params=params, **kw
        )
