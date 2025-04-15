# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import SubmitDay0ConfigPostRequest


class SubmitDevicesBuilder:
    """
    Builds and executes requests for operations under /template/config/quickConnect/submitDevices
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: SubmitDay0ConfigPostRequest, **kw) -> List[Any]:
        """
        Creates and pushes bootstrap configurations onto day0 devices.
        POST /dataservice/template/config/quickConnect/submitDevices

        :param payload: Payload
        :returns: List[Any]
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/template/config/quickConnect/submitDevices",
            return_type=List[Any],
            payload=payload,
            **kw,
        )
