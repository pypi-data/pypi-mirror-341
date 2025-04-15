# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .te.te_builder import TeBuilder
    from .utd.utd_builder import UtdBuilder
    from .waas.waas_builder import WaasBuilder


class VirtualApplicationBuilder:
    """
    Builds and executes requests for operations under /device/virtualApplication
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def te(self) -> TeBuilder:
        """
        The te property
        """
        from .te.te_builder import TeBuilder

        return TeBuilder(self._request_adapter)

    @property
    def utd(self) -> UtdBuilder:
        """
        The utd property
        """
        from .utd.utd_builder import UtdBuilder

        return UtdBuilder(self._request_adapter)

    @property
    def waas(self) -> WaasBuilder:
        """
        The waas property
        """
        from .waas.waas_builder import WaasBuilder

        return WaasBuilder(self._request_adapter)
