# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List, Optional

from catalystwan.abc import RequestAdapterInterface


class StatusBuilder:
    """
    Builds and executes requests for operations under /template/cloudx/status
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, app_name: str, vpn_id: Optional[int] = None, **kw) -> List[Any]:
        """
        Get sites per application per vpn
        GET /dataservice/template/cloudx/status

        :param app_name: App name
        :param vpn_id: VPN Id
        :returns: List[Any]
        """
        params = {
            "appName": app_name,
            "vpnId": vpn_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/template/cloudx/status", return_type=List[Any], params=params, **kw
        )
