# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .configdb.configdb_builder import ConfigdbBuilder
    from .logfile.logfile_builder import LogfileBuilder
    from .logging.logging_builder import LoggingBuilder
    from .olapdb.olapdb_builder import OlapdbBuilder


class UtilBuilder:
    """
    Builds and executes requests for operations under /util
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def configdb(self) -> ConfigdbBuilder:
        """
        The configdb property
        """
        from .configdb.configdb_builder import ConfigdbBuilder

        return ConfigdbBuilder(self._request_adapter)

    @property
    def logfile(self) -> LogfileBuilder:
        """
        The logfile property
        """
        from .logfile.logfile_builder import LogfileBuilder

        return LogfileBuilder(self._request_adapter)

    @property
    def logging(self) -> LoggingBuilder:
        """
        The logging property
        """
        from .logging.logging_builder import LoggingBuilder

        return LoggingBuilder(self._request_adapter)

    @property
    def olapdb(self) -> OlapdbBuilder:
        """
        The olapdb property
        """
        from .olapdb.olapdb_builder import OlapdbBuilder

        return OlapdbBuilder(self._request_adapter)
