# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface


class PeerStatsBuilder:
    """
    Builds and executes requests for operations under /device/dre/peer-stats
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        device_id: str,
        appqoe_dre_stats_peer_system_ip: Optional[str] = None,
        appqoe_dre_stats_peer_peer_no: Optional[int] = None,
        **kw,
    ) -> Any:
        """
        Get DRE peer statistics
        GET /dataservice/device/dre/peer-stats

        :param appqoe_dre_stats_peer_system_ip: System IP
        :param appqoe_dre_stats_peer_peer_no: Peer Number
        :param device_id: deviceId - Device IP
        :returns: Any
        """
        params = {
            "appqoe-dre-stats-peer-system-ip": appqoe_dre_stats_peer_system_ip,
            "appqoe-dre-stats-peer-peer-no": appqoe_dre_stats_peer_peer_no,
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/dre/peer-stats", params=params, **kw
        )
