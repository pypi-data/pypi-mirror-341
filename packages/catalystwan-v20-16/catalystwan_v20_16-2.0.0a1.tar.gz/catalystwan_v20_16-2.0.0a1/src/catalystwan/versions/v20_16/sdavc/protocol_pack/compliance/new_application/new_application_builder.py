# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class NewApplicationBuilder:
    """
    Builds and executes requests for operations under /sdavc/protocol-pack/compliance/new-application
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_uuid: str, **kw) -> Any:
        """
        Get New Application List for given Device UUID
        GET /dataservice/sdavc/protocol-pack/compliance/new-application/{deviceUUID}

        :param device_uuid: Device uuid
        :returns: Any
        """
        params = {
            "deviceUUID": device_uuid,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/sdavc/protocol-pack/compliance/new-application/{deviceUUID}",
            params=params,
            **kw,
        )
