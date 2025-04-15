# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class SyncStatusBuilder:
    """
    Builds and executes requests for operations under /device/sync_status
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, group_id: str, **kw) -> List[Any]:
        """
        Get list of currently syncing devices
        GET /dataservice/device/sync_status

        :param group_id: Group Id
        :returns: List[Any]
        """
        params = {
            "groupId": group_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/sync_status", return_type=List[Any], params=params, **kw
        )
