# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .configurations.configurations_builder import ConfigurationsBuilder
    from .debuglog.debuglog_builder import DebuglogBuilder
    from .level.level_builder import LevelBuilder
    from .loggers.loggers_builder import LoggersBuilder
    from .update_configuration.update_configuration_builder import UpdateConfigurationBuilder


class LoggingBuilder:
    """
    Builds and executes requests for operations under /util/logging
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def configurations(self) -> ConfigurationsBuilder:
        """
        The configurations property
        """
        from .configurations.configurations_builder import ConfigurationsBuilder

        return ConfigurationsBuilder(self._request_adapter)

    @property
    def debuglog(self) -> DebuglogBuilder:
        """
        The debuglog property
        """
        from .debuglog.debuglog_builder import DebuglogBuilder

        return DebuglogBuilder(self._request_adapter)

    @property
    def level(self) -> LevelBuilder:
        """
        The level property
        """
        from .level.level_builder import LevelBuilder

        return LevelBuilder(self._request_adapter)

    @property
    def loggers(self) -> LoggersBuilder:
        """
        The loggers property
        """
        from .loggers.loggers_builder import LoggersBuilder

        return LoggersBuilder(self._request_adapter)

    @property
    def update_configuration(self) -> UpdateConfigurationBuilder:
        """
        The updateConfiguration property
        """
        from .update_configuration.update_configuration_builder import UpdateConfigurationBuilder

        return UpdateConfigurationBuilder(self._request_adapter)
