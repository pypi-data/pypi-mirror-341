# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .connections.connections_builder import ConnectionsBuilder


class ConnectivityBuilder:
    """
    Builds and executes requests for operations under /multicloud/interconnect/{interconnect-type}/accounts/{interconnect-account-id}/cloud/{cloud-type}/connectivity
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
