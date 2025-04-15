# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .cpustat.cpustat_builder import CpustatBuilder
    from .memstat.memstat_builder import MemstatBuilder


class QfpBuilder:
    """
    Builds and executes requests for operations under /device/qfp
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def cpustat(self) -> CpustatBuilder:
        """
        The cpustat property
        """
        from .cpustat.cpustat_builder import CpustatBuilder

        return CpustatBuilder(self._request_adapter)

    @property
    def memstat(self) -> MemstatBuilder:
        """
        The memstat property
        """
        from .memstat.memstat_builder import MemstatBuilder

        return MemstatBuilder(self._request_adapter)
