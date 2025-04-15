# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DeviceIp


class AppGroupBuilder:
    """
    Builds and executes requests for operations under /device/redundancy-group/app-group
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_id: DeviceIp, **kw):
        """
        Get Redundancy Group Information
        GET /dataservice/device/redundancy-group/app-group

        :param device_id: Device id
        :returns: None
        """
        params = {
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/redundancy-group/app-group", params=params, **kw
        )
