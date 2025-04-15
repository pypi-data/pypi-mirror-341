# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .interfacestatistics.interfacestatistics_builder import InterfacestatisticsBuilder


class StatisticsBuilder:
    """
    Builds and executes requests for operations under /v2/data/device/statistics
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def interfacestatistics(self) -> InterfacestatisticsBuilder:
        """
        The interfacestatistics property
        """
        from .interfacestatistics.interfacestatistics_builder import InterfacestatisticsBuilder

        return InterfacestatisticsBuilder(self._request_adapter)
