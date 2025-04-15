# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .config.config_builder import ConfigBuilder
    from .status.status_builder import StatusBuilder


class AffinityBuilder:
    """
    Builds and executes requests for operations under /device/control/affinity
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def config(self) -> ConfigBuilder:
        """
        The config property
        """
        from .config.config_builder import ConfigBuilder

        return ConfigBuilder(self._request_adapter)

    @property
    def status(self) -> StatusBuilder:
        """
        The status property
        """
        from .status.status_builder import StatusBuilder

        return StatusBuilder(self._request_adapter)
