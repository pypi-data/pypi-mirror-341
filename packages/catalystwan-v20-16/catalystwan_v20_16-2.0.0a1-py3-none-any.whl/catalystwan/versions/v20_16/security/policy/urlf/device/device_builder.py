# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DeviceLists


class DeviceBuilder:
    """
    Builds and executes requests for operations under /security/policy/urlf/device
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw) -> List[DeviceLists]:
        """
        Get url filtering devices list
        POST /dataservice/security/policy/urlf/device

        :param payload: Stats query string
        :returns: List[DeviceLists]
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/security/policy/urlf/device",
            return_type=List[DeviceLists],
            payload=payload,
            **kw,
        )
