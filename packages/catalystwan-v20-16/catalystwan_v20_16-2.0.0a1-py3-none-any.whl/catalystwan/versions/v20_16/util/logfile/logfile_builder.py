# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .appserver.appserver_builder import AppserverBuilder


class LogfileBuilder:
    """
    Builds and executes requests for operations under /util/logfile
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def appserver(self) -> AppserverBuilder:
        """
        The appserver property
        """
        from .appserver.appserver_builder import AppserverBuilder

        return AppserverBuilder(self._request_adapter)
