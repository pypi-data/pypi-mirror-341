# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class AllDevicesBuilder:
    """
    Builds and executes requests for operations under /sdavc/protocol-pack/compliance/all-devices
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Get all device compliance details
        GET /dataservice/sdavc/protocol-pack/compliance/all-devices

        :returns: Any
        """
        return self._request_adapter.request(
            "GET", "/dataservice/sdavc/protocol-pack/compliance/all-devices", **kw
        )
