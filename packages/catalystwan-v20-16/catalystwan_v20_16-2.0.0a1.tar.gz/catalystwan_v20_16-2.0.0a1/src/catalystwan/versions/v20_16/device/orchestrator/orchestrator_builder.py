# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .connections.connections_builder import ConnectionsBuilder
    from .connectionshistory.connectionshistory_builder import ConnectionshistoryBuilder
    from .localproperties.localproperties_builder import LocalpropertiesBuilder
    from .proxymapping.proxymapping_builder import ProxymappingBuilder
    from .statistics.statistics_builder import StatisticsBuilder
    from .summary.summary_builder import SummaryBuilder
    from .validvedges.validvedges_builder import ValidvedgesBuilder
    from .validvmanageid.validvmanageid_builder import ValidvmanageidBuilder
    from .validvsmarts.validvsmarts_builder import ValidvsmartsBuilder


class OrchestratorBuilder:
    """
    Builds and executes requests for operations under /device/orchestrator
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def connections(self) -> ConnectionsBuilder:
        """
        The connections property
        """
        from .connections.connections_builder import ConnectionsBuilder

        return ConnectionsBuilder(self._request_adapter)

    @property
    def connectionshistory(self) -> ConnectionshistoryBuilder:
        """
        The connectionshistory property
        """
        from .connectionshistory.connectionshistory_builder import ConnectionshistoryBuilder

        return ConnectionshistoryBuilder(self._request_adapter)

    @property
    def localproperties(self) -> LocalpropertiesBuilder:
        """
        The localproperties property
        """
        from .localproperties.localproperties_builder import LocalpropertiesBuilder

        return LocalpropertiesBuilder(self._request_adapter)

    @property
    def proxymapping(self) -> ProxymappingBuilder:
        """
        The proxymapping property
        """
        from .proxymapping.proxymapping_builder import ProxymappingBuilder

        return ProxymappingBuilder(self._request_adapter)

    @property
    def statistics(self) -> StatisticsBuilder:
        """
        The statistics property
        """
        from .statistics.statistics_builder import StatisticsBuilder

        return StatisticsBuilder(self._request_adapter)

    @property
    def summary(self) -> SummaryBuilder:
        """
        The summary property
        """
        from .summary.summary_builder import SummaryBuilder

        return SummaryBuilder(self._request_adapter)

    @property
    def validvedges(self) -> ValidvedgesBuilder:
        """
        The validvedges property
        """
        from .validvedges.validvedges_builder import ValidvedgesBuilder

        return ValidvedgesBuilder(self._request_adapter)

    @property
    def validvmanageid(self) -> ValidvmanageidBuilder:
        """
        The validvmanageid property
        """
        from .validvmanageid.validvmanageid_builder import ValidvmanageidBuilder

        return ValidvmanageidBuilder(self._request_adapter)

    @property
    def validvsmarts(self) -> ValidvsmartsBuilder:
        """
        The validvsmarts property
        """
        from .validvsmarts.validvsmarts_builder import ValidvsmartsBuilder

        return ValidvsmartsBuilder(self._request_adapter)
