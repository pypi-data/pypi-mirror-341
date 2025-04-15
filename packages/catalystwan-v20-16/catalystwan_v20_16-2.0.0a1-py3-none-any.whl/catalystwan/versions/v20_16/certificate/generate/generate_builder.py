# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .csr.csr_builder import CsrBuilder
    from .enterprise.enterprise_builder import EnterpriseBuilder
    from .wanedge.wanedge_builder import WanedgeBuilder


class GenerateBuilder:
    """
    Builds and executes requests for operations under /certificate/generate
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def csr(self) -> CsrBuilder:
        """
        The csr property
        """
        from .csr.csr_builder import CsrBuilder

        return CsrBuilder(self._request_adapter)

    @property
    def enterprise(self) -> EnterpriseBuilder:
        """
        The enterprise property
        """
        from .enterprise.enterprise_builder import EnterpriseBuilder

        return EnterpriseBuilder(self._request_adapter)

    @property
    def wanedge(self) -> WanedgeBuilder:
        """
        The wanedge property
        """
        from .wanedge.wanedge_builder import WanedgeBuilder

        return WanedgeBuilder(self._request_adapter)
