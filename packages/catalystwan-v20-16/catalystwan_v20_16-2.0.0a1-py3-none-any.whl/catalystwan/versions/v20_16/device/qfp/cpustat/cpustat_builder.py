# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import QfpCpuState


class CpustatBuilder:
    """
    Builds and executes requests for operations under /device/qfp/cpustat
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_id: str, **kw) -> QfpCpuState:
        """
        Get QFP cpu status
        GET /dataservice/device/qfp/cpustat

        :param device_id: deviceId - Device IP
        :returns: QfpCpuState
        """
        params = {
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/qfp/cpustat", return_type=QfpCpuState, params=params, **kw
        )
