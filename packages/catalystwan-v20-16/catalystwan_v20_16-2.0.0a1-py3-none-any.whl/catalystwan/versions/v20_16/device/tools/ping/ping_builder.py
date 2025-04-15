# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import PingRequest, PingResponse


class PingBuilder:
    """
    Builds and executes requests for operations under /device/tools/ping
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, device_ip: str, payload: PingRequest, **kw) -> PingResponse:
        """
        Ping device
        POST /dataservice/device/tools/ping/{deviceIP}

        :param device_ip: Device IP
        :param payload: Ping parameter
        :returns: PingResponse
        """
        params = {
            "deviceIP": device_ip,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/device/tools/ping/{deviceIP}",
            return_type=PingResponse,
            params=params,
            payload=payload,
            **kw,
        )
