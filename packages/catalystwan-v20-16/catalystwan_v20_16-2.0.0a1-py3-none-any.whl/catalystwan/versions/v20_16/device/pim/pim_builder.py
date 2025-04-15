# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .interface.interface_builder import InterfaceBuilder
    from .neighbor.neighbor_builder import NeighborBuilder
    from .rp_mapping.rp_mapping_builder import RpMappingBuilder
    from .statistics.statistics_builder import StatisticsBuilder


class PimBuilder:
    """
    Builds and executes requests for operations under /device/pim
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
    def neighbor(self) -> NeighborBuilder:
        """
        The neighbor property
        """
        from .neighbor.neighbor_builder import NeighborBuilder

        return NeighborBuilder(self._request_adapter)

    @property
    def rp_mapping(self) -> RpMappingBuilder:
        """
        The rp-mapping property
        """
        from .rp_mapping.rp_mapping_builder import RpMappingBuilder

        return RpMappingBuilder(self._request_adapter)

    @property
    def statistics(self) -> StatisticsBuilder:
        """
        The statistics property
        """
        from .statistics.statistics_builder import StatisticsBuilder

        return StatisticsBuilder(self._request_adapter)
