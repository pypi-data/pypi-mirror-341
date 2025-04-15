# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .bandwidth.bandwidth_builder import BandwidthBuilder


class InterfaceBuilder:
    """
    Builds and executes requests for operations under /stream/device/speed/interface
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def bandwidth(self) -> BandwidthBuilder:
        """
        The bandwidth property
        """
        from .bandwidth.bandwidth_builder import BandwidthBuilder

        return BandwidthBuilder(self._request_adapter)
