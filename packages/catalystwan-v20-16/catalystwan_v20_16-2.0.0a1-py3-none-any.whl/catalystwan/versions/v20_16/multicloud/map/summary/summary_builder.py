# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import CloudTypeParam, MapSummary


class SummaryBuilder:
    """
    Builds and executes requests for operations under /multicloud/map/summary
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        cloud_type: Optional[CloudTypeParam] = None,
        vpn_tunnel_status: Optional[str] = None,
        **kw,
    ) -> List[MapSummary]:
        """
        Get mapping summary
        GET /dataservice/multicloud/map/summary

        :param cloud_type: Cloud type
        :param vpn_tunnel_status: Vpn tunnel status
        :returns: List[MapSummary]
        """
        params = {
            "cloudType": cloud_type,
            "vpnTunnelStatus": vpn_tunnel_status,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/map/summary",
            return_type=List[MapSummary],
            params=params,
            **kw,
        )
