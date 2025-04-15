# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .active.active_builder import ActiveBuilder


class AlarmBuilder:
    """
    Builds and executes requests for operations under /data/device/statistics/alarm
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def active(self) -> ActiveBuilder:
        """
        The active property
        """
        from .active.active_builder import ActiveBuilder

        return ActiveBuilder(self._request_adapter)
