# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class WanedgeBuilder:
    """
    Builds and executes requests for operations under /sslproxy/certificate/wanedge
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, device_id: str, payload: Any, **kw):
        """
        Add SSL proxy wan edge
        POST /dataservice/sslproxy/certificate/wanedge/{deviceId}

        :param device_id: Device Id
        :param payload: Cert state
        :returns: None
        """
        params = {
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/sslproxy/certificate/wanedge/{deviceId}",
            params=params,
            payload=payload,
            **kw,
        )
