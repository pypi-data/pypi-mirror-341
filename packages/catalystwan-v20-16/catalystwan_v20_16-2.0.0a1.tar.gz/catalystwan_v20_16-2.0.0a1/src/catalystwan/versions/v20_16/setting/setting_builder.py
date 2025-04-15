# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .configuration.configuration_builder import ConfigurationBuilder


class SettingBuilder:
    """
    Builds and executes requests for operations under /setting
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def configuration(self) -> ConfigurationBuilder:
        """
        The configuration property
        """
        from .configuration.configuration_builder import ConfigurationBuilder

        return ConfigurationBuilder(self._request_adapter)
