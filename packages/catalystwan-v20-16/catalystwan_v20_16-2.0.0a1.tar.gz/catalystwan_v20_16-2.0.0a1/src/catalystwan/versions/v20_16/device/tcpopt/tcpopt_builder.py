# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .activeflows.activeflows_builder import ActiveflowsBuilder
    from .expiredflows.expiredflows_builder import ExpiredflowsBuilder
    from .summary.summary_builder import SummaryBuilder


class TcpoptBuilder:
    """
    Builds and executes requests for operations under /device/tcpopt
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def activeflows(self) -> ActiveflowsBuilder:
        """
        The activeflows property
        """
        from .activeflows.activeflows_builder import ActiveflowsBuilder

        return ActiveflowsBuilder(self._request_adapter)

    @property
    def expiredflows(self) -> ExpiredflowsBuilder:
        """
        The expiredflows property
        """
        from .expiredflows.expiredflows_builder import ExpiredflowsBuilder

        return ExpiredflowsBuilder(self._request_adapter)

    @property
    def summary(self) -> SummaryBuilder:
        """
        The summary property
        """
        from .summary.summary_builder import SummaryBuilder

        return SummaryBuilder(self._request_adapter)
