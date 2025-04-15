# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DeviceIp, PowerConsumptionRealTime


class PowerconsumptionBuilder:
    """
    Builds and executes requests for operations under /device/powerconsumption
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_id: DeviceIp, **kw) -> PowerConsumptionRealTime:
        """
        Get Power Consumption Information
        GET /dataservice/device/powerconsumption

        :param device_id: Device id
        :returns: PowerConsumptionRealTime
        """
        params = {
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/device/powerconsumption",
            return_type=PowerConsumptionRealTime,
            params=params,
            **kw,
        )
