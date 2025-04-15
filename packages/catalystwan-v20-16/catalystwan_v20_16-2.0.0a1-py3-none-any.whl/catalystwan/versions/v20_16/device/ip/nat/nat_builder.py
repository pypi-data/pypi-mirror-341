# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .filter.filter_builder import FilterBuilder
    from .interface.interface_builder import InterfaceBuilder
    from .interfacestatistics.interfacestatistics_builder import InterfacestatisticsBuilder
    from .translation.translation_builder import TranslationBuilder


class NatBuilder:
    """
    Builds and executes requests for operations under /device/ip/nat
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def filter(self) -> FilterBuilder:
        """
        The filter property
        """
        from .filter.filter_builder import FilterBuilder

        return FilterBuilder(self._request_adapter)

    @property
    def interface(self) -> InterfaceBuilder:
        """
        The interface property
        """
        from .interface.interface_builder import InterfaceBuilder

        return InterfaceBuilder(self._request_adapter)

    @property
    def interfacestatistics(self) -> InterfacestatisticsBuilder:
        """
        The interfacestatistics property
        """
        from .interfacestatistics.interfacestatistics_builder import InterfacestatisticsBuilder

        return InterfacestatisticsBuilder(self._request_adapter)

    @property
    def translation(self) -> TranslationBuilder:
        """
        The translation property
        """
        from .translation.translation_builder import TranslationBuilder

        return TranslationBuilder(self._request_adapter)
