# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .affinity.affinity_builder import AffinityBuilder
    from .connections.connections_builder import ConnectionsBuilder
    from .connectionshistory.connectionshistory_builder import ConnectionshistoryBuilder
    from .connectionsinfo.connectionsinfo_builder import ConnectionsinfoBuilder
    from .count.count_builder import CountBuilder
    from .links.links_builder import LinksBuilder
    from .localproperties.localproperties_builder import LocalpropertiesBuilder
    from .networksummary.networksummary_builder import NetworksummaryBuilder
    from .regionconnections.regionconnections_builder import RegionconnectionsBuilder
    from .statistics.statistics_builder import StatisticsBuilder
    from .status.status_builder import StatusBuilder
    from .summary.summary_builder import SummaryBuilder
    from .synced.synced_builder import SyncedBuilder
    from .validdevices.validdevices_builder import ValiddevicesBuilder
    from .validvmanageid.validvmanageid_builder import ValidvmanageidBuilder
    from .validvsmarts.validvsmarts_builder import ValidvsmartsBuilder
    from .waninterface.waninterface_builder import WaninterfaceBuilder


class ControlBuilder:
    """
    Builds and executes requests for operations under /device/control
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def affinity(self) -> AffinityBuilder:
        """
        The affinity property
        """
        from .affinity.affinity_builder import AffinityBuilder

        return AffinityBuilder(self._request_adapter)

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
    def connectionsinfo(self) -> ConnectionsinfoBuilder:
        """
        The connectionsinfo property
        """
        from .connectionsinfo.connectionsinfo_builder import ConnectionsinfoBuilder

        return ConnectionsinfoBuilder(self._request_adapter)

    @property
    def count(self) -> CountBuilder:
        """
        The count property
        """
        from .count.count_builder import CountBuilder

        return CountBuilder(self._request_adapter)

    @property
    def links(self) -> LinksBuilder:
        """
        The links property
        """
        from .links.links_builder import LinksBuilder

        return LinksBuilder(self._request_adapter)

    @property
    def localproperties(self) -> LocalpropertiesBuilder:
        """
        The localproperties property
        """
        from .localproperties.localproperties_builder import LocalpropertiesBuilder

        return LocalpropertiesBuilder(self._request_adapter)

    @property
    def networksummary(self) -> NetworksummaryBuilder:
        """
        The networksummary property
        """
        from .networksummary.networksummary_builder import NetworksummaryBuilder

        return NetworksummaryBuilder(self._request_adapter)

    @property
    def regionconnections(self) -> RegionconnectionsBuilder:
        """
        The regionconnections property
        """
        from .regionconnections.regionconnections_builder import RegionconnectionsBuilder

        return RegionconnectionsBuilder(self._request_adapter)

    @property
    def statistics(self) -> StatisticsBuilder:
        """
        The statistics property
        """
        from .statistics.statistics_builder import StatisticsBuilder

        return StatisticsBuilder(self._request_adapter)

    @property
    def status(self) -> StatusBuilder:
        """
        The status property
        """
        from .status.status_builder import StatusBuilder

        return StatusBuilder(self._request_adapter)

    @property
    def summary(self) -> SummaryBuilder:
        """
        The summary property
        """
        from .summary.summary_builder import SummaryBuilder

        return SummaryBuilder(self._request_adapter)

    @property
    def synced(self) -> SyncedBuilder:
        """
        The synced property
        """
        from .synced.synced_builder import SyncedBuilder

        return SyncedBuilder(self._request_adapter)

    @property
    def validdevices(self) -> ValiddevicesBuilder:
        """
        The validdevices property
        """
        from .validdevices.validdevices_builder import ValiddevicesBuilder

        return ValiddevicesBuilder(self._request_adapter)

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

    @property
    def waninterface(self) -> WaninterfaceBuilder:
        """
        The waninterface property
        """
        from .waninterface.waninterface_builder import WaninterfaceBuilder

        return WaninterfaceBuilder(self._request_adapter)
