# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .device.device_builder import DeviceBuilder
    from .devices.devices_builder import DevicesBuilder
    from .download.download_builder import DownloadBuilder
    from .generic.generic_builder import GenericBuilder


class BootstrapBuilder:
    """
    Builds and executes requests for operations under /system/device/bootstrap
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def device(self) -> DeviceBuilder:
        """
        The device property
        """
        from .device.device_builder import DeviceBuilder

        return DeviceBuilder(self._request_adapter)

    @property
    def devices(self) -> DevicesBuilder:
        """
        The devices property
        """
        from .devices.devices_builder import DevicesBuilder

        return DevicesBuilder(self._request_adapter)

    @property
    def download(self) -> DownloadBuilder:
        """
        The download property
        """
        from .download.download_builder import DownloadBuilder

        return DownloadBuilder(self._request_adapter)

    @property
    def generic(self) -> GenericBuilder:
        """
        The generic property
        """
        from .generic.generic_builder import GenericBuilder

        return GenericBuilder(self._request_adapter)
