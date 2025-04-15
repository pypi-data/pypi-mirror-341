# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .management.management_builder import ManagementBuilder


class LifecycleBuilder:
    """
    Builds and executes requests for operations under /system/device/lifecycle
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def management(self) -> ManagementBuilder:
        """
        The management property
        """
        from .management.management_builder import ManagementBuilder

        return ManagementBuilder(self._request_adapter)
