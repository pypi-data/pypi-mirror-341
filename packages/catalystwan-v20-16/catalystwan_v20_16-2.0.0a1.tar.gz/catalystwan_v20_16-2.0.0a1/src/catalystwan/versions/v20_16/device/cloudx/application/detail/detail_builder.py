# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import VpnIdParam


class DetailBuilder:
    """
    Builds and executes requests for operations under /device/cloudx/application/detail
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        vpn_id: Optional[VpnIdParam] = None,
        application: Optional[str] = None,
        query: Optional[str] = None,
        **kw,
    ) -> Any:
        """
        Get list of cloudexpress applications from device (Real Time)
        GET /dataservice/device/cloudx/application/detail

        :param vpn_id: VPN Id
        :param application: Application
        :param query: Query
        :returns: Any
        """
        params = {
            "vpn-id": vpn_id,
            "application": application,
            "query": query,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/cloudx/application/detail", params=params, **kw
        )
