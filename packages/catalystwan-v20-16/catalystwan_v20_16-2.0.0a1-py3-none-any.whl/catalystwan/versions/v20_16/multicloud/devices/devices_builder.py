# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import CloudTypeParam, DeviceInfoExtendedResponse

if TYPE_CHECKING:
    from .edge.edge_builder import EdgeBuilder


class DevicesBuilder:
    """
    Builds and executes requests for operations under /multicloud/devices
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self, cloud_type: CloudTypeParam, cloud_gateway_name: Optional[str] = None, **kw
    ) -> DeviceInfoExtendedResponse:
        """
        Get cloud devices by cloud type
        GET /dataservice/multicloud/devices/{cloudType}

        :param cloud_type: Cloud type
        :param cloud_gateway_name: Cloud gateway name
        :returns: DeviceInfoExtendedResponse
        """
        params = {
            "cloudType": cloud_type,
            "cloudGatewayName": cloud_gateway_name,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/devices/{cloudType}",
            return_type=DeviceInfoExtendedResponse,
            params=params,
            **kw,
        )

    @property
    def edge(self) -> EdgeBuilder:
        """
        The edge property
        """
        from .edge.edge_builder import EdgeBuilder

        return EdgeBuilder(self._request_adapter)
