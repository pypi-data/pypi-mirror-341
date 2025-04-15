# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class SystemipBuilder:
    """
    Builds and executes requests for operations under /system/device/management/systemip
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Get management system IP mapping
        GET /dataservice/system/device/management/systemip

        :returns: Any
        """
        return self._request_adapter.request(
            "GET", "/dataservice/system/device/management/systemip", **kw
        )
