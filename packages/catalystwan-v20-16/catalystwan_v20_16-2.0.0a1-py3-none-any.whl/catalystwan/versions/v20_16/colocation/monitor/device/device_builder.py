# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .vnf.vnf_builder import VnfBuilder


class DeviceBuilder:
    """
    Builds and executes requests for operations under /colocation/monitor/device
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def vnf(self) -> VnfBuilder:
        """
        The vnf property
        """
        from .vnf.vnf_builder import VnfBuilder

        return VnfBuilder(self._request_adapter)
