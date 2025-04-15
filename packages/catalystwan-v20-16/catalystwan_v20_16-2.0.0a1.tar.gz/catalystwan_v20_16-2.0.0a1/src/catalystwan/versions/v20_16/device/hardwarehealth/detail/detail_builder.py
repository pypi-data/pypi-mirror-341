# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DeviceHardwareHealthDetail


class DetailBuilder:
    """
    Builds and executes requests for operations under /device/hardwarehealth/detail
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self, device_id: Optional[str] = None, state: Optional[str] = None, **kw
    ) -> List[DeviceHardwareHealthDetail]:
        """
        Get hardware health details for device
        GET /dataservice/device/hardwarehealth/detail

        :param device_id: Device Id
        :param state: Device state
        :returns: List[DeviceHardwareHealthDetail]
        """
        params = {
            "deviceId": device_id,
            "state": state,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/device/hardwarehealth/detail",
            return_type=List[DeviceHardwareHealthDetail],
            params=params,
            **kw,
        )
