# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .gateways.gateways_builder import GatewaysBuilder


class InterconnectBuilder:
    """
    Builds and executes requests for operations under /v1/multicloud/interconnect
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def gateways(self) -> GatewaysBuilder:
        """
        The gateways property
        """
        from .gateways.gateways_builder import GatewaysBuilder

        return GatewaysBuilder(self._request_adapter)
