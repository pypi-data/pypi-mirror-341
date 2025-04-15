# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DeviceDetailsData


class DevicesBuilder:
    """
    Builds and executes requests for operations under /onboard/devices
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, status: str, **kw) -> List[DeviceDetailsData]:
        """
        GET Manual Onboard Device details
        GET /dataservice/onboard/devices

        :param status: Status
        :returns: List[DeviceDetailsData]
        """
        params = {
            "status": status,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/onboard/devices",
            return_type=List[DeviceDetailsData],
            params=params,
            **kw,
        )

    def post(self, payload: DeviceDetailsData, **kw) -> Any:
        """
        Manual Onboard added Device details
        POST /dataservice/onboard/devices

        :param payload: On board Devices
        :returns: Any
        """
        return self._request_adapter.request(
            "POST", "/dataservice/onboard/devices", payload=payload, **kw
        )
