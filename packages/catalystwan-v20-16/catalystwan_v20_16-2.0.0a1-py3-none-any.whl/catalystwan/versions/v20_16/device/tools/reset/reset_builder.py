# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .interface.interface_builder import InterfaceBuilder


class ResetBuilder:
    """
    Builds and executes requests for operations under /device/tools/reset
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def interface(self) -> InterfaceBuilder:
        """
        The interface property
        """
        from .interface.interface_builder import InterfaceBuilder

        return InterfaceBuilder(self._request_adapter)
