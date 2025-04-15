# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .ip.ip_builder import IpBuilder


class ComplianceBuilder:
    """
    Builds and executes requests for operations under /software/compliance
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def ip(self) -> IpBuilder:
        """
        The ip property
        """
        from .ip.ip_builder import IpBuilder

        return IpBuilder(self._request_adapter)
