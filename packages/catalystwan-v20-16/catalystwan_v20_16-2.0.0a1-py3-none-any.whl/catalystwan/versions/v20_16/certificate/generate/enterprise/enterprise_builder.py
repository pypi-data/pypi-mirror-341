# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .csr.csr_builder import CsrBuilder


class EnterpriseBuilder:
    """
    Builds and executes requests for operations under /certificate/generate/enterprise
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
