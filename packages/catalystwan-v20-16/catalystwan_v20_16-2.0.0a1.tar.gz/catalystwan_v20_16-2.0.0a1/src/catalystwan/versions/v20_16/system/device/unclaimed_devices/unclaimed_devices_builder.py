# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import GetAllUnclaimedDevices


class UnclaimedDevicesBuilder:
    """
    Builds and executes requests for operations under /system/device/unclaimedDevices
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> GetAllUnclaimedDevices:
        """
        Get list of all unclaimed devices
        GET /dataservice/system/device/unclaimedDevices

        :returns: GetAllUnclaimedDevices
        """
        return self._request_adapter.request(
            "GET",
            "/dataservice/system/device/unclaimedDevices",
            return_type=GetAllUnclaimedDevices,
            **kw,
        )
