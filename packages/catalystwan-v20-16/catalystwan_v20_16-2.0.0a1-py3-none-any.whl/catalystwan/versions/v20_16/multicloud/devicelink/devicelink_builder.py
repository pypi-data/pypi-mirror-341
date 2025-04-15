# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .edge.edge_builder import EdgeBuilder
    from .metro_speed.metro_speed_builder import MetroSpeedBuilder


class DevicelinkBuilder:
    """
    Builds and executes requests for operations under /multicloud/devicelink
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def edge(self) -> EdgeBuilder:
        """
        The edge property
        """
        from .edge.edge_builder import EdgeBuilder

        return EdgeBuilder(self._request_adapter)

    @property
    def metro_speed(self) -> MetroSpeedBuilder:
        """
        The metroSpeed property
        """
        from .metro_speed.metro_speed_builder import MetroSpeedBuilder

        return MetroSpeedBuilder(self._request_adapter)
