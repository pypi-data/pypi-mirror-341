# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .sense.sense_builder import SenseBuilder
    from .server.server_builder import ServerBuilder


class CdnaBuilder:
    """
    Builds and executes requests for operations under /cdna
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def sense(self) -> SenseBuilder:
        """
        The sense property
        """
        from .sense.sense_builder import SenseBuilder

        return SenseBuilder(self._request_adapter)

    @property
    def server(self) -> ServerBuilder:
        """
        The server property
        """
        from .server.server_builder import ServerBuilder

        return ServerBuilder(self._request_adapter)
