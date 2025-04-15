# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .clients.clients_builder import ClientsBuilder
    from .interfaces.interfaces_builder import InterfacesBuilder
    from .radius.radius_builder import RadiusBuilder


class Dot1XBuilder:
    """
    Builds and executes requests for operations under /device/dot1x
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def clients(self) -> ClientsBuilder:
        """
        The clients property
        """
        from .clients.clients_builder import ClientsBuilder

        return ClientsBuilder(self._request_adapter)

    @property
    def interfaces(self) -> InterfacesBuilder:
        """
        The interfaces property
        """
        from .interfaces.interfaces_builder import InterfacesBuilder

        return InterfacesBuilder(self._request_adapter)

    @property
    def radius(self) -> RadiusBuilder:
        """
        The radius property
        """
        from .radius.radius_builder import RadiusBuilder

        return RadiusBuilder(self._request_adapter)
