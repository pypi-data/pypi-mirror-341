# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class MemorydbBuilder:
    """
    Builds and executes requests for operations under /device/syncall/memorydb
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, **kw):
        """
        Synchronize memory database for all devices
        POST /dataservice/device/syncall/memorydb

        :returns: None
        """
        return self._request_adapter.request("POST", "/dataservice/device/syncall/memorydb", **kw)
