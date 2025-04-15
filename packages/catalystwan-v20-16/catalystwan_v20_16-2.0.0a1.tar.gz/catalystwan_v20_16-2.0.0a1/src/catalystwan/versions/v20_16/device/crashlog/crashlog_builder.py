# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .details.details_builder import DetailsBuilder
    from .log.log_builder import LogBuilder
    from .synced.synced_builder import SyncedBuilder


class CrashlogBuilder:
    """
    Builds and executes requests for operations under /device/crashlog
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, device_id: str, **kw) -> Any:
        """
        Get device crash logs from device
        GET /dataservice/device/crashlog

        :param device_id: deviceId - Device IP
        :returns: Any
        """
        params = {
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/crashlog", params=params, **kw
        )

    @property
    def details(self) -> DetailsBuilder:
        """
        The details property
        """
        from .details.details_builder import DetailsBuilder

        return DetailsBuilder(self._request_adapter)

    @property
    def log(self) -> LogBuilder:
        """
        The log property
        """
        from .log.log_builder import LogBuilder

        return LogBuilder(self._request_adapter)

    @property
    def synced(self) -> SyncedBuilder:
        """
        The synced property
        """
        from .synced.synced_builder import SyncedBuilder

        return SyncedBuilder(self._request_adapter)
