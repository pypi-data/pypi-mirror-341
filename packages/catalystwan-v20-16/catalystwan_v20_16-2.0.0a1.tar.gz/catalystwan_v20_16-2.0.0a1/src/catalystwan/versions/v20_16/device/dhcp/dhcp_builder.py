# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .client.client_builder import ClientBuilder
    from .interface.interface_builder import InterfaceBuilder
    from .server.server_builder import ServerBuilder


class DhcpBuilder:
    """
    Builds and executes requests for operations under /device/dhcp
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def client(self) -> ClientBuilder:
        """
        The client property
        """
        from .client.client_builder import ClientBuilder

        return ClientBuilder(self._request_adapter)

    @property
    def interface(self) -> InterfaceBuilder:
        """
        The interface property
        """
        from .interface.interface_builder import InterfaceBuilder

        return InterfaceBuilder(self._request_adapter)

    @property
    def server(self) -> ServerBuilder:
        """
        The server property
        """
        from .server.server_builder import ServerBuilder

        return ServerBuilder(self._request_adapter)
