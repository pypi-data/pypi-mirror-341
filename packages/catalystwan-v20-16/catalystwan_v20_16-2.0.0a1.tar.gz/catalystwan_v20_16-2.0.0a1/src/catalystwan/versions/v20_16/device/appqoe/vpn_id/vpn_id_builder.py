# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface


class VpnIdBuilder:
    """
    Builds and executes requests for operations under /device/appqoe/vpn-id
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        vpn_id: str,
        device_id: str,
        client_ip: Optional[str] = None,
        server_ip: Optional[str] = None,
        server_port: Optional[str] = None,
        **kw,
    ) -> Any:
        """
        Get Appqoe Active vpn Id details from device
        GET /dataservice/device/appqoe/vpn-id

        :param vpn_id: VPN Id
        :param client_ip: Client Ip
        :param server_ip: Server Ip
        :param server_port: Server-Port
        :param device_id: Device IP
        :returns: Any
        """
        params = {
            "vpn-id": vpn_id,
            "client-ip": client_ip,
            "server-ip": server_ip,
            "server-port": server_port,
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/appqoe/vpn-id", params=params, **kw
        )
