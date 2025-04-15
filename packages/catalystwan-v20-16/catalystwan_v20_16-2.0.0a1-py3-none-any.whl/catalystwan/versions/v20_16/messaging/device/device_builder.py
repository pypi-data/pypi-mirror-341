# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .vmanage.vmanage_builder import VmanageBuilder


class DeviceBuilder:
    """
    Builds and executes requests for operations under /messaging/device
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def vmanage(self) -> VmanageBuilder:
        """
        The vmanage property
        """
        from .vmanage.vmanage_builder import VmanageBuilder

        return VmanageBuilder(self._request_adapter)
