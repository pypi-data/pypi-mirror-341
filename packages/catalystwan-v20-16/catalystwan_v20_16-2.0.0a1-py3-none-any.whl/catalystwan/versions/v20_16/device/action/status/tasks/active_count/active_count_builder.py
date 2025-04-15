# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DeviceTaskStatus


class ActiveCountBuilder:
    """
    Builds and executes requests for operations under /device/action/status/tasks/activeCount
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> DeviceTaskStatus:
        """
        Get active task count
        GET /dataservice/device/action/status/tasks/activeCount

        :returns: DeviceTaskStatus
        """
        return self._request_adapter.request(
            "GET",
            "/dataservice/device/action/status/tasks/activeCount",
            return_type=DeviceTaskStatus,
            **kw,
        )
