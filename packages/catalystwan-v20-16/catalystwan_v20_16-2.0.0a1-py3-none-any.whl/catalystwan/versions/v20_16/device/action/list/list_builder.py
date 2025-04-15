# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import GenerateDeviceActionListInner


class ListBuilder:
    """
    Builds and executes requests for operations under /device/action/list
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[GenerateDeviceActionListInner]:
        """
        Get device action list
        GET /dataservice/device/action/list

        :returns: List[GenerateDeviceActionListInner]
        """
        return self._request_adapter.request(
            "GET",
            "/dataservice/device/action/list",
            return_type=List[GenerateDeviceActionListInner],
            **kw,
        )
