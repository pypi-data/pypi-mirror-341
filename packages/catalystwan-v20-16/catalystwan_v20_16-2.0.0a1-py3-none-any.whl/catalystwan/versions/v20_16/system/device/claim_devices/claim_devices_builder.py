# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import ClaimDevicesRequest, ClaimDevicesResponse


class ClaimDevicesBuilder:
    """
    Builds and executes requests for operations under /system/device/claimDevices
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: ClaimDevicesRequest, **kw) -> ClaimDevicesResponse:
        """
        Claim the selected unclaimed devices
        POST /dataservice/system/device/claimDevices

        :param payload: Claim device request
        :returns: ClaimDevicesResponse
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/system/device/claimDevices",
            return_type=ClaimDevicesResponse,
            payload=payload,
            **kw,
        )
