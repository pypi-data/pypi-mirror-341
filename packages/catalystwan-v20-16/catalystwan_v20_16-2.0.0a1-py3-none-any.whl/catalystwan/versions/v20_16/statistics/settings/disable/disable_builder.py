# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .devicelist.devicelist_builder import DevicelistBuilder


class DisableBuilder:
    """
    Builds and executes requests for operations under /statistics/settings/disable
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def devicelist(self) -> DevicelistBuilder:
        """
        The devicelist property
        """
        from .devicelist.devicelist_builder import DevicelistBuilder

        return DevicelistBuilder(self._request_adapter)
