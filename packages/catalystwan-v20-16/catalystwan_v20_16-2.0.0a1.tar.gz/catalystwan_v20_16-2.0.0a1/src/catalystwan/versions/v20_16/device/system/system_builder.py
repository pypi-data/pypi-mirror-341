# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .clock.clock_builder import ClockBuilder
    from .info.info_builder import InfoBuilder
    from .statistics.statistics_builder import StatisticsBuilder
    from .status.status_builder import StatusBuilder
    from .synced.synced_builder import SyncedBuilder


class SystemBuilder:
    """
    Builds and executes requests for operations under /device/system
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def clock(self) -> ClockBuilder:
        """
        The clock property
        """
        from .clock.clock_builder import ClockBuilder

        return ClockBuilder(self._request_adapter)

    @property
    def info(self) -> InfoBuilder:
        """
        The info property
        """
        from .info.info_builder import InfoBuilder

        return InfoBuilder(self._request_adapter)

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
    def synced(self) -> SyncedBuilder:
        """
        The synced property
        """
        from .synced.synced_builder import SyncedBuilder

        return SyncedBuilder(self._request_adapter)
