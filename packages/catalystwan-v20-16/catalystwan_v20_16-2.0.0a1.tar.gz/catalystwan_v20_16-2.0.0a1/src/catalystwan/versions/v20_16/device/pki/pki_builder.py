# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .trustpoint.trustpoint_builder import TrustpointBuilder


class PkiBuilder:
    """
    Builds and executes requests for operations under /device/pki
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def trustpoint(self) -> TrustpointBuilder:
        """
        The trustpoint property
        """
        from .trustpoint.trustpoint_builder import TrustpointBuilder

        return TrustpointBuilder(self._request_adapter)
