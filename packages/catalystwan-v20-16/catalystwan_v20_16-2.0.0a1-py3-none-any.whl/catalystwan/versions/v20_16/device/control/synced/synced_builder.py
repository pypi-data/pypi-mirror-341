# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .connections.connections_builder import ConnectionsBuilder
    from .localproperties.localproperties_builder import LocalpropertiesBuilder
    from .waninterface.waninterface_builder import WaninterfaceBuilder


class SyncedBuilder:
    """
    Builds and executes requests for operations under /device/control/synced
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def connections(self) -> ConnectionsBuilder:
        """
        The connections property
        """
        from .connections.connections_builder import ConnectionsBuilder

        return ConnectionsBuilder(self._request_adapter)

    @property
    def localproperties(self) -> LocalpropertiesBuilder:
        """
        The localproperties property
        """
        from .localproperties.localproperties_builder import LocalpropertiesBuilder

        return LocalpropertiesBuilder(self._request_adapter)

    @property
    def waninterface(self) -> WaninterfaceBuilder:
        """
        The waninterface property
        """
        from .waninterface.waninterface_builder import WaninterfaceBuilder

        return WaninterfaceBuilder(self._request_adapter)
