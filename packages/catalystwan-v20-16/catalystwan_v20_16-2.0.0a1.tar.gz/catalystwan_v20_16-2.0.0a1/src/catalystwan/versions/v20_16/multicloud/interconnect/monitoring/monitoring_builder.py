# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .connected_sites.connected_sites_builder import ConnectedSitesBuilder
    from .devices.devices_builder import DevicesBuilder
    from .gateways.gateways_builder import GatewaysBuilder


class MonitoringBuilder:
    """
    Builds and executes requests for operations under /multicloud/interconnect/{interconnect-type}/monitoring
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def connected_sites(self) -> ConnectedSitesBuilder:
        """
        The connected-sites property
        """
        from .connected_sites.connected_sites_builder import ConnectedSitesBuilder

        return ConnectedSitesBuilder(self._request_adapter)

    @property
    def devices(self) -> DevicesBuilder:
        """
        The devices property
        """
        from .devices.devices_builder import DevicesBuilder

        return DevicesBuilder(self._request_adapter)

    @property
    def gateways(self) -> GatewaysBuilder:
        """
        The gateways property
        """
        from .gateways.gateways_builder import GatewaysBuilder

        return GatewaysBuilder(self._request_adapter)
