# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .blist.blist_builder import BlistBuilder


class DeviceBuilder:
    """
    Builds and executes requests for operations under /stream/device/nwpi/device
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def blist(self) -> BlistBuilder:
        """
        The blist property
        """
        from .blist.blist_builder import BlistBuilder

        return BlistBuilder(self._request_adapter)
