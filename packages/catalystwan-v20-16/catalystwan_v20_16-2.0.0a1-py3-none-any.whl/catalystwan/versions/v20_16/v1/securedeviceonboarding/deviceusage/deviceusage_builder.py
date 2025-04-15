# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DeviceUsageDetails


class DeviceusageBuilder:
    """
    Builds and executes requests for operations under /v1/securedeviceonboarding/{deviceUUID}/deviceusage
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_uuid: str, **kw) -> DeviceUsageDetails:
        """
        Get device data usage using device uuid
        GET /dataservice/v1/securedeviceonboarding/{deviceUUID}/deviceusage

        :param device_uuid: DeviceUUID
        :returns: DeviceUsageDetails
        """
        params = {
            "deviceUUID": device_uuid,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/v1/securedeviceonboarding/{deviceUUID}/deviceusage",
            return_type=DeviceUsageDetails,
            params=params,
            **kw,
        )
