# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .clients.clients_builder import ClientsBuilder
    from .interfaces.interfaces_builder import InterfacesBuilder
    from .radios.radios_builder import RadiosBuilder
    from .radius.radius_builder import RadiusBuilder


class WlanBuilder:
    """
    Builds and executes requests for operations under /device/wlan
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
    def radios(self) -> RadiosBuilder:
        """
        The radios property
        """
        from .radios.radios_builder import RadiosBuilder

        return RadiosBuilder(self._request_adapter)

    @property
    def radius(self) -> RadiusBuilder:
        """
        The radius property
        """
        from .radius.radius_builder import RadiusBuilder

        return RadiusBuilder(self._request_adapter)
