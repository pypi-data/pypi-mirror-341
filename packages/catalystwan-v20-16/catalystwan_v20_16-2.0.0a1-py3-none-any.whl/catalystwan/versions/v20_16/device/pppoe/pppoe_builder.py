# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .session.session_builder import SessionBuilder
    from .statistic.statistic_builder import StatisticBuilder


class PppoeBuilder:
    """
    Builds and executes requests for operations under /device/pppoe
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def session(self) -> SessionBuilder:
        """
        The session property
        """
        from .session.session_builder import SessionBuilder

        return SessionBuilder(self._request_adapter)

    @property
    def statistic(self) -> StatisticBuilder:
        """
        The statistic property
        """
        from .statistic.statistic_builder import StatisticBuilder

        return StatisticBuilder(self._request_adapter)
