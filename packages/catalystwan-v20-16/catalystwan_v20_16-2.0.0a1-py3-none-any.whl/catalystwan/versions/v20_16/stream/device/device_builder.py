# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .capture.capture_builder import CaptureBuilder
    from .log.log_builder import LogBuilder
    from .nwpi.nwpi_builder import NwpiBuilder
    from .speed.speed_builder import SpeedBuilder
    from .status.status_builder import StatusBuilder
    from .umts.umts_builder import UmtsBuilder


class DeviceBuilder:
    """
    Builds and executes requests for operations under /stream/device
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def capture(self) -> CaptureBuilder:
        """
        The capture property
        """
        from .capture.capture_builder import CaptureBuilder

        return CaptureBuilder(self._request_adapter)

    @property
    def log(self) -> LogBuilder:
        """
        The log property
        """
        from .log.log_builder import LogBuilder

        return LogBuilder(self._request_adapter)

    @property
    def nwpi(self) -> NwpiBuilder:
        """
        The nwpi property
        """
        from .nwpi.nwpi_builder import NwpiBuilder

        return NwpiBuilder(self._request_adapter)

    @property
    def speed(self) -> SpeedBuilder:
        """
        The speed property
        """
        from .speed.speed_builder import SpeedBuilder

        return SpeedBuilder(self._request_adapter)

    @property
    def status(self) -> StatusBuilder:
        """
        The status property
        """
        from .status.status_builder import StatusBuilder

        return StatusBuilder(self._request_adapter)

    @property
    def umts(self) -> UmtsBuilder:
        """
        The umts property
        """
        from .umts.umts_builder import UmtsBuilder

        return UmtsBuilder(self._request_adapter)
