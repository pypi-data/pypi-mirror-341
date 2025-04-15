# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import SetLogLevelPostRequest


class LevelBuilder:
    """
    Builds and executes requests for operations under /util/logging/level
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: SetLogLevelPostRequest, **kw):
        """
        Set log level for logger
        POST /dataservice/util/logging/level

        :param payload: Payload
        :returns: None
        """
        return self._request_adapter.request(
            "POST", "/dataservice/util/logging/level", payload=payload, **kw
        )
