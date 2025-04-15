# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import GenerateBootstrapConfigForVedgesResponse, VEdgeBootstrapConfig


class DevicesBuilder:
    """
    Builds and executes requests for operations under /system/device/bootstrap/devices
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: VEdgeBootstrapConfig, **kw) -> GenerateBootstrapConfigForVedgesResponse:
        """
        Create bootstrap config for software vEdges
        POST /dataservice/system/device/bootstrap/devices

        :param payload: Request body for Device bootstrap configuration
        :returns: GenerateBootstrapConfigForVedgesResponse
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/system/device/bootstrap/devices",
            return_type=GenerateBootstrapConfigForVedgesResponse,
            payload=payload,
            **kw,
        )
