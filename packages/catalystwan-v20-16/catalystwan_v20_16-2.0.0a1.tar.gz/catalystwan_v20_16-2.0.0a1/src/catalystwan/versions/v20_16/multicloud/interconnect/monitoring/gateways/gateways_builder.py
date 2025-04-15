# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import InterconnectGatewayMonitoring


class GatewaysBuilder:
    """
    Builds and executes requests for operations under /multicloud/interconnect/{interconnect-type}/monitoring/gateways
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, interconnect_type: str, **kw) -> List[InterconnectGatewayMonitoring]:
        """
        API to retrieve Interconnect gateways by Interconnect type for monitoring.
        GET /dataservice/multicloud/interconnect/{interconnect-type}/monitoring/gateways

        :param interconnect_type: Interconnect provider type
        :returns: List[InterconnectGatewayMonitoring]
        """
        params = {
            "interconnect-type": interconnect_type,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/interconnect/{interconnect-type}/monitoring/gateways",
            return_type=List[InterconnectGatewayMonitoring],
            params=params,
            **kw,
        )
