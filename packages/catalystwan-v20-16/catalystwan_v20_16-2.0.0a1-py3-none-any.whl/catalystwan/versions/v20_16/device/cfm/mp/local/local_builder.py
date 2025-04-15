# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .mep.mep_builder import MepBuilder
    from .mip.mip_builder import MipBuilder


class LocalBuilder:
    """
    Builds and executes requests for operations under /device/cfm/mp/local
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def mep(self) -> MepBuilder:
        """
        The mep property
        """
        from .mep.mep_builder import MepBuilder

        return MepBuilder(self._request_adapter)

    @property
    def mip(self) -> MipBuilder:
        """
        The mip property
        """
        from .mip.mip_builder import MipBuilder

        return MipBuilder(self._request_adapter)
