# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import AlarmQueryInputResponse


class InputBuilder:
    """
    Builds and executes requests for operations under /alarms/query/input
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> AlarmQueryInputResponse:
        """
        Get alarm field details
        GET /dataservice/alarms/query/input

        :returns: AlarmQueryInputResponse
        """
        return self._request_adapter.request(
            "GET", "/dataservice/alarms/query/input", return_type=AlarmQueryInputResponse, **kw
        )
