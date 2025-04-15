# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import QfpMemoryState


class MemstatBuilder:
    """
    Builds and executes requests for operations under /device/qfp/memstat
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_id: str, **kw) -> QfpMemoryState:
        """
        Get QFP memory status
        GET /dataservice/device/qfp/memstat

        :param device_id: deviceId - Device IP
        :returns: QfpMemoryState
        """
        params = {
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/device/qfp/memstat",
            return_type=QfpMemoryState,
            params=params,
            **kw,
        )
