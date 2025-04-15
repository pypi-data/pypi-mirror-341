# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .compliance.compliance_builder import ComplianceBuilder


class SoftwareBuilder:
    """
    Builds and executes requests for operations under /software
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def compliance(self) -> ComplianceBuilder:
        """
        The compliance property
        """
        from .compliance.compliance_builder import ComplianceBuilder

        return ComplianceBuilder(self._request_adapter)
