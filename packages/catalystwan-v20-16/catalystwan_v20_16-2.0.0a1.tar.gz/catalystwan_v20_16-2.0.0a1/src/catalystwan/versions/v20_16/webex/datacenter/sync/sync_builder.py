# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class SyncBuilder:
    """
    Builds and executes requests for operations under /webex/datacenter/sync
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, **kw) -> bool:
        """
        TEMP-Update webex data center data in DB with data from Webex API
        POST /dataservice/webex/datacenter/sync

        :returns: bool
        """
        return self._request_adapter.request(
            "POST", "/dataservice/webex/datacenter/sync", return_type=bool, **kw
        )
