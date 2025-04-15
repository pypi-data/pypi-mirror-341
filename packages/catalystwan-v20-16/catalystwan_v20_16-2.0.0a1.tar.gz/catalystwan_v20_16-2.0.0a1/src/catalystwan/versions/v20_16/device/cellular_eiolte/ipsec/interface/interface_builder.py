# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .counters.counters_builder import CountersBuilder
    from .session.session_builder import SessionBuilder


class InterfaceBuilder:
    """
    Builds and executes requests for operations under /device/cellularEiolte/ipsec/interface
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def counters(self) -> CountersBuilder:
        """
        The counters property
        """
        from .counters.counters_builder import CountersBuilder

        return CountersBuilder(self._request_adapter)

    @property
    def session(self) -> SessionBuilder:
        """
        The session property
        """
        from .session.session_builder import SessionBuilder

        return SessionBuilder(self._request_adapter)
