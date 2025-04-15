# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .cpu_info.cpu_info_builder import CpuInfoBuilder


class ResourcesBuilder:
    """
    Builds and executes requests for operations under /device/csp/resources
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def cpu_info(self) -> CpuInfoBuilder:
        """
        The cpu-info property
        """
        from .cpu_info.cpu_info_builder import CpuInfoBuilder

        return CpuInfoBuilder(self._request_adapter)
