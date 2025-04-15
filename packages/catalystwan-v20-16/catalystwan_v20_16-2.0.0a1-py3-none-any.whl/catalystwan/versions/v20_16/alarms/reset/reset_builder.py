# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import SimpleMessageResponse


class ResetBuilder:
    """
    Builds and executes requests for operations under /alarms/reset
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> SimpleMessageResponse:
        """
        Reset correlation engine.
        GET /dataservice/alarms/reset

        :returns: SimpleMessageResponse
        """
        return self._request_adapter.request(
            "GET", "/dataservice/alarms/reset", return_type=SimpleMessageResponse, **kw
        )
