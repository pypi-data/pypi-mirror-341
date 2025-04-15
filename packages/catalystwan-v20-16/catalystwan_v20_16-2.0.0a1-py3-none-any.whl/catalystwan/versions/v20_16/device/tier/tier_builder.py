# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class TierBuilder:
    """
    Builds and executes requests for operations under /device/tier
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw):
        """
        getTiers
        GET /dataservice/device/tier

        :returns: None
        """
        return self._request_adapter.request("GET", "/dataservice/device/tier", **kw)

    def post(self, add_tier: str, **kw):
        """
        add tier
        POST /dataservice/device/tier

        :param add_tier: addTier
        :returns: None
        """
        params = {
            "addTier": add_tier,
        }
        return self._request_adapter.request(
            "POST", "/dataservice/device/tier", params=params, **kw
        )

    def delete(self, tier_name: str, **kw):
        """
        deleteTier
        DELETE /dataservice/device/tier/{tierName}

        :param tier_name: deletetier
        :returns: None
        """
        params = {
            "tierName": tier_name,
        }
        return self._request_adapter.request(
            "DELETE", "/dataservice/device/tier/{tierName}", params=params, **kw
        )
