# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class StatusBuilder:
    """
    Builds and executes requests for operations under /stream/device/status
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, device_uuid: str, payload: str, **kw):
        """
        Get device status stream
        POST /dataservice/stream/device/status/{deviceUUID}

        :param device_uuid: Device uuid
        :param payload: Payload
        :returns: None
        """
        params = {
            "deviceUUID": device_uuid,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/stream/device/status/{deviceUUID}",
            params=params,
            payload=payload,
            **kw,
        )
