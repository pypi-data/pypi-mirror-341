# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import CreateFilterVpnList


class VpnBuilder:
    """
    Builds and executes requests for operations under /device/action/filter/vpn
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self, site_id: Optional[str] = None, device_id: Optional[str] = None, **kw
    ) -> CreateFilterVpnList:
        """
        Get filter VPN list
        GET /dataservice/device/action/filter/vpn

        :param site_id: site-id
        :param device_id: deviceId
        :returns: CreateFilterVpnList
        """
        params = {
            "site-id": site_id,
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/device/action/filter/vpn",
            return_type=CreateFilterVpnList,
            params=params,
            **kw,
        )
