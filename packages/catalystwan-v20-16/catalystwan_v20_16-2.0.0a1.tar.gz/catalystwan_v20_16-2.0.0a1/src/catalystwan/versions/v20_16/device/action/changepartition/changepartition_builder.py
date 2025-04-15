# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DeviceIp


class ChangepartitionBuilder:
    """
    Builds and executes requests for operations under /device/action/changepartition
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_id: List[DeviceIp], **kw) -> Any:
        """
        Get change partition information
        GET /dataservice/device/action/changepartition

        :param device_id: deviceId - Device IP
        :returns: Any
        """
        params = {
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/action/changepartition", params=params, **kw
        )

    def post(self, payload: Any, **kw) -> Any:
        """
        Process change partition operation
        POST /dataservice/device/action/changepartition

        :param payload: Request body for Process change partition operation
        :returns: Any
        """
        return self._request_adapter.request(
            "POST", "/dataservice/device/action/changepartition", payload=payload, **kw
        )
