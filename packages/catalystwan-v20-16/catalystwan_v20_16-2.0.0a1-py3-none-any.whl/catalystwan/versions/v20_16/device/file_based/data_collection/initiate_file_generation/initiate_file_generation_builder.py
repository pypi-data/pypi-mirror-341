# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import InitiateFileGenerationRequest


class InitiateFileGenerationBuilder:
    """
    Builds and executes requests for operations under /device/file-based/data-collection/initiate-file-generation
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: InitiateFileGenerationRequest, **kw) -> str:
        """
        Request device to prepare realtime collection data in required file format
        POST /dataservice/device/file-based/data-collection/initiate-file-generation

        :param payload: Initiate file generation payload
        :returns: str
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/device/file-based/data-collection/initiate-file-generation",
            return_type=str,
            payload=payload,
            **kw,
        )
