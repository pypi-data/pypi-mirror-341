# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class VpnBuilder:
    """
    Builds and executes requests for operations under /template/config/vpn
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_id: str, **kw) -> List[Any]:
        """
        Get list of configured VPN (excluding reserved VPN) for a device
        GET /dataservice/template/config/vpn/{deviceId}

        :param device_id: Device Model ID
        :returns: List[Any]
        """
        params = {
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/template/config/vpn/{deviceId}",
            return_type=List[Any],
            params=params,
            **kw,
        )
