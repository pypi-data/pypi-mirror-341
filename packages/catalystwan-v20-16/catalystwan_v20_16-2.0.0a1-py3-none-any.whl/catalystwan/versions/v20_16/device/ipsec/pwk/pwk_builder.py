# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .inbound.inbound_builder import InboundBuilder
    from .localsa.localsa_builder import LocalsaBuilder
    from .outbound.outbound_builder import OutboundBuilder


class PwkBuilder:
    """
    Builds and executes requests for operations under /device/ipsec/pwk
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def inbound(self) -> InboundBuilder:
        """
        The inbound property
        """
        from .inbound.inbound_builder import InboundBuilder

        return InboundBuilder(self._request_adapter)

    @property
    def localsa(self) -> LocalsaBuilder:
        """
        The localsa property
        """
        from .localsa.localsa_builder import LocalsaBuilder

        return LocalsaBuilder(self._request_adapter)

    @property
    def outbound(self) -> OutboundBuilder:
        """
        The outbound property
        """
        from .outbound.outbound_builder import OutboundBuilder

        return OutboundBuilder(self._request_adapter)
