# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .override_start.override_start_builder import OverrideStartBuilder
    from .start.start_builder import StartBuilder
    from .stop.stop_builder import StopBuilder


class MonitorBuilder:
    """
    Builds and executes requests for operations under /stream/device/nwpi/monitor
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def override_start(self) -> OverrideStartBuilder:
        """
        The overrideStart property
        """
        from .override_start.override_start_builder import OverrideStartBuilder

        return OverrideStartBuilder(self._request_adapter)

    @property
    def start(self) -> StartBuilder:
        """
        The start property
        """
        from .start.start_builder import StartBuilder

        return StartBuilder(self._request_adapter)

    @property
    def stop(self) -> StopBuilder:
        """
        The stop property
        """
        from .stop.stop_builder import StopBuilder

        return StopBuilder(self._request_adapter)
