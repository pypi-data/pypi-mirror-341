# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import Vpnid


class ConnectionssummaryBuilder:
    """
    Builds and executes requests for operations under /network/connectionssummary
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        is_cached: Optional[bool] = False,
        vpn_id: Optional[List[Vpnid]] = None,
        site_id: Optional[str] = None,
        **kw,
    ) -> Any:
        """
        Retrieve vManage control status
        GET /dataservice/network/connectionssummary

        :param is_cached: Is cached flag
        :param vpn_id: VPN Id
        :param site_id: Optional site ID  to filter devices
        :returns: Any
        """
        params = {
            "isCached": is_cached,
            "vpnId": vpn_id,
            "site-id": site_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/network/connectionssummary", params=params, **kw
        )
