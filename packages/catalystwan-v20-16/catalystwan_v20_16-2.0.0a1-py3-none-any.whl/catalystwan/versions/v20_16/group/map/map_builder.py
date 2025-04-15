# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .devices.devices_builder import DevicesBuilder


class MapBuilder:
    """
    Builds and executes requests for operations under /group/map
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def devices(self) -> DevicesBuilder:
        """
        The devices property
        """
        from .devices.devices_builder import DevicesBuilder

        return DevicesBuilder(self._request_adapter)
