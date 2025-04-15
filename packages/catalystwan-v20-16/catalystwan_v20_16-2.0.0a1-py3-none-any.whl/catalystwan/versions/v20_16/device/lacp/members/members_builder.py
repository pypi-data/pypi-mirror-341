# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface


class MembersBuilder:
    """
    Builds and executes requests for operations under /device/lacp/members
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        device_id: str,
        channel_group: Optional[str] = None,
        if_name: Optional[str] = None,
        **kw,
    ) -> Any:
        """
        Get device lacp port channel interface table (Real Time)
        GET /dataservice/device/lacp/members

        :param channel_group: Channel-group
        :param if_name: Interface Name
        :param device_id: deviceId - Device IP
        :returns: Any
        """
        params = {
            "channel-group": channel_group,
            "ifName": if_name,
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/lacp/members", params=params, **kw
        )
