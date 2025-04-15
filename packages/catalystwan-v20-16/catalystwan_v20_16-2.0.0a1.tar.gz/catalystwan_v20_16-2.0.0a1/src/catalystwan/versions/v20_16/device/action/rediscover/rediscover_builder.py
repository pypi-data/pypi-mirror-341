# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import GenerateRediscoverInfo


class RediscoverBuilder:
    """
    Builds and executes requests for operations under /device/action/rediscover
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> GenerateRediscoverInfo:
        """
        Get rediscover operation information
        GET /dataservice/device/action/rediscover

        :returns: GenerateRediscoverInfo
        """
        return self._request_adapter.request(
            "GET", "/dataservice/device/action/rediscover", return_type=GenerateRediscoverInfo, **kw
        )

    def post(self, payload: Any, **kw):
        """
        Rediscover device
        POST /dataservice/device/action/rediscover

        :param payload: Rediscover device request payload
        :returns: None
        """
        return self._request_adapter.request(
            "POST", "/dataservice/device/action/rediscover", payload=payload, **kw
        )
