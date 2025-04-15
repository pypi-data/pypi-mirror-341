# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .attach_devices.attach_devices_builder import AttachDevicesBuilder
    from .detach_devices.detach_devices_builder import DetachDevicesBuilder
    from .devices.devices_builder import DevicesBuilder
    from .disconnect.disconnect_builder import DisconnectBuilder
    from .onboard.onboard_builder import OnboardBuilder
    from .policies.policies_builder import PoliciesBuilder


class MdpBuilder:
    """
    Builds and executes requests for operations under /mdp
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def attach_devices(self) -> AttachDevicesBuilder:
        """
        The attachDevices property
        """
        from .attach_devices.attach_devices_builder import AttachDevicesBuilder

        return AttachDevicesBuilder(self._request_adapter)

    @property
    def detach_devices(self) -> DetachDevicesBuilder:
        """
        The detachDevices property
        """
        from .detach_devices.detach_devices_builder import DetachDevicesBuilder

        return DetachDevicesBuilder(self._request_adapter)

    @property
    def devices(self) -> DevicesBuilder:
        """
        The devices property
        """
        from .devices.devices_builder import DevicesBuilder

        return DevicesBuilder(self._request_adapter)

    @property
    def disconnect(self) -> DisconnectBuilder:
        """
        The disconnect property
        """
        from .disconnect.disconnect_builder import DisconnectBuilder

        return DisconnectBuilder(self._request_adapter)

    @property
    def onboard(self) -> OnboardBuilder:
        """
        The onboard property
        """
        from .onboard.onboard_builder import OnboardBuilder

        return OnboardBuilder(self._request_adapter)

    @property
    def policies(self) -> PoliciesBuilder:
        """
        The policies property
        """
        from .policies.policies_builder import PoliciesBuilder

        return PoliciesBuilder(self._request_adapter)
