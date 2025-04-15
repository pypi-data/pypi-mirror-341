# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import AddressFamilyParam, VpnIdParam


class RoutetableBuilder:
    """
    Builds and executes requests for operations under /device/ip/routetable
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        device_id: str,
        vpn_id: Optional[VpnIdParam] = None,
        address_family: Optional[AddressFamilyParam] = None,
        prefix: Optional[str] = None,
        protocol: Optional[str] = None,
        **kw,
    ) -> Any:
        """
        Get route table list from device (Real Time)
        GET /dataservice/device/ip/routetable

        :param vpn_id: VPN Id
        :param address_family: Address family
        :param prefix: IP prefix
        :param protocol: IP protocol
        :param device_id: deviceId - Device IP
        :returns: Any
        """
        params = {
            "vpn-id": vpn_id,
            "address-family": address_family,
            "prefix": prefix,
            "protocol": protocol,
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/ip/routetable", params=params, **kw
        )
