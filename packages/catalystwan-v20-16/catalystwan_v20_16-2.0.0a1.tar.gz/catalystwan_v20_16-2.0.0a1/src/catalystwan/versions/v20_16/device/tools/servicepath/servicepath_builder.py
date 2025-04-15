# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class ServicepathBuilder:
    """
    Builds and executes requests for operations under /device/tools/servicepath
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, device_ip: str, payload: Any, **kw):
        """
        Service path
        POST /dataservice/device/tools/servicepath/{deviceIP}

        :param device_ip: Device IP
        :param payload: Service path parameter
        :returns: None
        """
        params = {
            "deviceIP": device_ip,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/device/tools/servicepath/{deviceIP}",
            params=params,
            payload=payload,
            **kw,
        )
