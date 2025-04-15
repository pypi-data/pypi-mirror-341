# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DeviceIp


class PhysicalBuilder:
    """
    Builds and executes requests for operations under /topology/physical
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_id: List[DeviceIp], **kw) -> Any:
        """
        Create pysical topology
        GET /dataservice/topology/physical

        :param device_id: Device Id list
        :returns: Any
        """
        params = {
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/topology/physical", params=params, **kw
        )
