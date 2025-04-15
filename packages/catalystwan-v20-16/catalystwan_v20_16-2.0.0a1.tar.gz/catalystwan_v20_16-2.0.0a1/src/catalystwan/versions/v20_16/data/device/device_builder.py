# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .state.state_builder import StateBuilder
    from .statistics.statistics_builder import StatisticsBuilder


class DeviceBuilder:
    """
    Builds and executes requests for operations under /data/device
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def state(self) -> StateBuilder:
        """
        The state property
        """
        from .state.state_builder import StateBuilder

        return StateBuilder(self._request_adapter)

    @property
    def statistics(self) -> StatisticsBuilder:
        """
        The statistics property
        """
        from .statistics.statistics_builder import StatisticsBuilder

        return StatisticsBuilder(self._request_adapter)
