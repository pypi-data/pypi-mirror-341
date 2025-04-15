# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class UserusergroupbindingsBuilder:
    """
    Builds and executes requests for operations under /device/policy/userusergroupbindings
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_id: str, **kw) -> Any:
        """
        Show User-Usergroup bindings from Vsmart
        GET /dataservice/device/policy/userusergroupbindings

        :param device_id: Device Id
        :returns: Any
        """
        params = {
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/policy/userusergroupbindings", params=params, **kw
        )
