# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .delete_devices.delete_devices_builder import DeleteDevicesBuilder
    from .details.details_builder import DetailsBuilder
    from .devices.devices_builder import DevicesBuilder


class OnboardBuilder:
    """
    Builds and executes requests for operations under /onboard
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def delete_devices(self) -> DeleteDevicesBuilder:
        """
        The delete-devices property
        """
        from .delete_devices.delete_devices_builder import DeleteDevicesBuilder

        return DeleteDevicesBuilder(self._request_adapter)

    @property
    def details(self) -> DetailsBuilder:
        """
        The details property
        """
        from .details.details_builder import DetailsBuilder

        return DetailsBuilder(self._request_adapter)

    @property
    def devices(self) -> DevicesBuilder:
        """
        The devices property
        """
        from .devices.devices_builder import DevicesBuilder

        return DevicesBuilder(self._request_adapter)
