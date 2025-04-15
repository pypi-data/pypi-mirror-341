# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class DiffBuilder:
    """
    Builds and executes requests for operations under /template/config/diff
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_id: str, **kw) -> Any:
        """
        Generates a JSON object that contains the diff for a given device
        GET /dataservice/template/config/diff/{deviceId}

        :param device_id: Device Model ID
        :returns: Any
        """
        params = {
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/template/config/diff/{deviceId}", params=params, **kw
        )
