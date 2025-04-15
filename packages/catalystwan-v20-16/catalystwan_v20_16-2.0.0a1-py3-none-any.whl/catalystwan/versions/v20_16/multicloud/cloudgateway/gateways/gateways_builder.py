# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .device_chassis_numbers.device_chassis_numbers_builder import DeviceChassisNumbersBuilder


class GatewaysBuilder:
    """
    Builds and executes requests for operations under /multicloud/cloudgateway/{cloudType}/gateways
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def device_chassis_numbers(self) -> DeviceChassisNumbersBuilder:
        """
        The device-chassis-numbers property
        """
        from .device_chassis_numbers.device_chassis_numbers_builder import (
            DeviceChassisNumbersBuilder,
        )

        return DeviceChassisNumbersBuilder(self._request_adapter)
