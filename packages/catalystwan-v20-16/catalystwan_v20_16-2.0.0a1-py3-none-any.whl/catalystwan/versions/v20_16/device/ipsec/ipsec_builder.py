# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .identity.identity_builder import IdentityBuilder
    from .ike.ike_builder import IkeBuilder
    from .ikev1.ikev1_builder import Ikev1Builder
    from .ikev2.ikev2_builder import Ikev2Builder
    from .inbound.inbound_builder import InboundBuilder
    from .localsa.localsa_builder import LocalsaBuilder
    from .outbound.outbound_builder import OutboundBuilder
    from .pwk.pwk_builder import PwkBuilder


class IpsecBuilder:
    """
    Builds and executes requests for operations under /device/ipsec
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def identity(self) -> IdentityBuilder:
        """
        The identity property
        """
        from .identity.identity_builder import IdentityBuilder

        return IdentityBuilder(self._request_adapter)

    @property
    def ike(self) -> IkeBuilder:
        """
        The ike property
        """
        from .ike.ike_builder import IkeBuilder

        return IkeBuilder(self._request_adapter)

    @property
    def ikev1(self) -> Ikev1Builder:
        """
        The ikev1 property
        """
        from .ikev1.ikev1_builder import Ikev1Builder

        return Ikev1Builder(self._request_adapter)

    @property
    def ikev2(self) -> Ikev2Builder:
        """
        The ikev2 property
        """
        from .ikev2.ikev2_builder import Ikev2Builder

        return Ikev2Builder(self._request_adapter)

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

    @property
    def pwk(self) -> PwkBuilder:
        """
        The pwk property
        """
        from .pwk.pwk_builder import PwkBuilder

        return PwkBuilder(self._request_adapter)
