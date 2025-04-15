# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import GetDeviceConfiguration


class DevicebringupBuilder:
    """
    Builds and executes requests for operations under /troubleshooting/devicebringup
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, uuid: str, **kw) -> GetDeviceConfiguration:
        """
        Debug device bring up
        GET /dataservice/troubleshooting/devicebringup

        :param uuid: Uuid
        :returns: GetDeviceConfiguration
        """
        params = {
            "uuid": uuid,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/troubleshooting/devicebringup",
            return_type=GetDeviceConfiguration,
            params=params,
            **kw,
        )
