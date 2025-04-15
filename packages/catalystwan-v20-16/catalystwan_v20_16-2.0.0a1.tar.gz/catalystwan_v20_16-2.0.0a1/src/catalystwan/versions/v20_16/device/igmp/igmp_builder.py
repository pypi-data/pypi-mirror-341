# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .groups.groups_builder import GroupsBuilder
    from .interface.interface_builder import InterfaceBuilder
    from .statistics.statistics_builder import StatisticsBuilder
    from .summary.summary_builder import SummaryBuilder


class IgmpBuilder:
    """
    Builds and executes requests for operations under /device/igmp
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def groups(self) -> GroupsBuilder:
        """
        The groups property
        """
        from .groups.groups_builder import GroupsBuilder

        return GroupsBuilder(self._request_adapter)

    @property
    def interface(self) -> InterfaceBuilder:
        """
        The interface property
        """
        from .interface.interface_builder import InterfaceBuilder

        return InterfaceBuilder(self._request_adapter)

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
