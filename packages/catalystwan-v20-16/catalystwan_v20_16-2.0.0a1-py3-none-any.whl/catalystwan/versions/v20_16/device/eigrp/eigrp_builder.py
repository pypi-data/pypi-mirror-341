# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .interface.interface_builder import InterfaceBuilder
    from .route.route_builder import RouteBuilder
    from .topology.topology_builder import TopologyBuilder


class EigrpBuilder:
    """
    Builds and executes requests for operations under /device/eigrp
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def interface(self) -> InterfaceBuilder:
        """
        The interface property
        """
        from .interface.interface_builder import InterfaceBuilder

        return InterfaceBuilder(self._request_adapter)

    @property
    def route(self) -> RouteBuilder:
        """
        The route property
        """
        from .route.route_builder import RouteBuilder

        return RouteBuilder(self._request_adapter)

    @property
    def topology(self) -> TopologyBuilder:
        """
        The topology property
        """
        from .topology.topology_builder import TopologyBuilder

        return TopologyBuilder(self._request_adapter)
