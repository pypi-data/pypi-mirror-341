# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import ProtoParam


class FilterBuilder:
    """
    Builds and executes requests for operations under /device/ip/nat/filter
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        device_id: str,
        nat_vpn_id: Optional[str] = None,
        nat_ifname: Optional[str] = None,
        private_source_address: Optional[str] = None,
        proto: Optional[ProtoParam] = None,
        **kw,
    ) -> Any:
        """
        Get NAT filter list from device
        GET /dataservice/device/ip/nat/filter

        :param nat_vpn_id: NAT VPN Id
        :param nat_ifname: NAT interface name
        :param private_source_address: Private source address
        :param proto: Protocol
        :param device_id: deviceId - Device IP
        :returns: Any
        """
        params = {
            "nat-vpn-id": nat_vpn_id,
            "nat-ifname": nat_ifname,
            "private-source-address": private_source_address,
            "proto": proto,
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/ip/nat/filter", params=params, **kw
        )
