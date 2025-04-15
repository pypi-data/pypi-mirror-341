# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DeviceUuid, SpeedTestInterfaceResponse


class BandwidthBuilder:
    """
    Builds and executes requests for operations under /stream/device/speed/interface/bandwidth
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        device_uuid: DeviceUuid,
        circuit: Optional[str] = None,
        source_interface: Optional[str] = None,
        **kw,
    ) -> SpeedTestInterfaceResponse:
        """
        Get
        GET /dataservice/stream/device/speed/interface/bandwidth

        :param device_uuid: Device uuid
        :param circuit: Circuit
        :param source_interface: Source interface
        :returns: SpeedTestInterfaceResponse
        """
        params = {
            "deviceUUID": device_uuid,
            "circuit": circuit,
            "sourceInterface": source_interface,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/stream/device/speed/interface/bandwidth",
            return_type=SpeedTestInterfaceResponse,
            params=params,
            **kw,
        )
