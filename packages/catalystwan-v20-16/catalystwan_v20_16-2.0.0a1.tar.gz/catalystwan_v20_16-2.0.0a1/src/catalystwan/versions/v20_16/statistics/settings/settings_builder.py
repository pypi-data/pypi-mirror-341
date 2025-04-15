# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .disable.disable_builder import DisableBuilder
    from .status.status_builder import StatusBuilder


class SettingsBuilder:
    """
    Builds and executes requests for operations under /statistics/settings
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def disable(self) -> DisableBuilder:
        """
        The disable property
        """
        from .disable.disable_builder import DisableBuilder

        return DisableBuilder(self._request_adapter)

    @property
    def status(self) -> StatusBuilder:
        """
        The status property
        """
        from .status.status_builder import StatusBuilder

        return StatusBuilder(self._request_adapter)
