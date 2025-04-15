# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import GenerateGenericBootstrapConfigForVedges


class DevicesBuilder:
    """
    Builds and executes requests for operations under /system/device/bootstrap/generic/devices
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self, wanif: Optional[str] = None, sd_routing_device: Optional[bool] = None, **kw
    ) -> GenerateGenericBootstrapConfigForVedges:
        """
        Create bootstrap config for software vEdges
        GET /dataservice/system/device/bootstrap/generic/devices

        :param wanif: Device WAN interface
        :param sd_routing_device: Flag indicating if this is SD-Routing device
        :returns: GenerateGenericBootstrapConfigForVedges
        """
        params = {
            "wanif": wanif,
            "sdRoutingDevice": sd_routing_device,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/system/device/bootstrap/generic/devices",
            return_type=GenerateGenericBootstrapConfigForVedges,
            params=params,
            **kw,
        )
