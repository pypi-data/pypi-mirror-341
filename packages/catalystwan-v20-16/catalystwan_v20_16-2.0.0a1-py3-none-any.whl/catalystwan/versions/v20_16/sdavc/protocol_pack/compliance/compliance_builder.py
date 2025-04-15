# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .all_devices.all_devices_builder import AllDevicesBuilder
    from .application.application_builder import ApplicationBuilder
    from .custom_application.custom_application_builder import CustomApplicationBuilder
    from .device.device_builder import DeviceBuilder
    from .initiate_device_compliance.initiate_device_compliance_builder import (
        InitiateDeviceComplianceBuilder,
    )
    from .initiate_policy_compliance.initiate_policy_compliance_builder import (
        InitiatePolicyComplianceBuilder,
    )
    from .new_application.new_application_builder import NewApplicationBuilder
    from .policy.policy_builder import PolicyBuilder


class ComplianceBuilder:
    """
    Builds and executes requests for operations under /sdavc/protocol-pack/compliance
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def all_devices(self) -> AllDevicesBuilder:
        """
        The all-devices property
        """
        from .all_devices.all_devices_builder import AllDevicesBuilder

        return AllDevicesBuilder(self._request_adapter)

    @property
    def application(self) -> ApplicationBuilder:
        """
        The application property
        """
        from .application.application_builder import ApplicationBuilder

        return ApplicationBuilder(self._request_adapter)

    @property
    def custom_application(self) -> CustomApplicationBuilder:
        """
        The custom-application property
        """
        from .custom_application.custom_application_builder import CustomApplicationBuilder

        return CustomApplicationBuilder(self._request_adapter)

    @property
    def device(self) -> DeviceBuilder:
        """
        The device property
        """
        from .device.device_builder import DeviceBuilder

        return DeviceBuilder(self._request_adapter)

    @property
    def initiate_device_compliance(self) -> InitiateDeviceComplianceBuilder:
        """
        The initiate-device-compliance property
        """
        from .initiate_device_compliance.initiate_device_compliance_builder import (
            InitiateDeviceComplianceBuilder,
        )

        return InitiateDeviceComplianceBuilder(self._request_adapter)

    @property
    def initiate_policy_compliance(self) -> InitiatePolicyComplianceBuilder:
        """
        The initiate-policy-compliance property
        """
        from .initiate_policy_compliance.initiate_policy_compliance_builder import (
            InitiatePolicyComplianceBuilder,
        )

        return InitiatePolicyComplianceBuilder(self._request_adapter)

    @property
    def new_application(self) -> NewApplicationBuilder:
        """
        The new-application property
        """
        from .new_application.new_application_builder import NewApplicationBuilder

        return NewApplicationBuilder(self._request_adapter)

    @property
    def policy(self) -> PolicyBuilder:
        """
        The policy property
        """
        from .policy.policy_builder import PolicyBuilder

        return PolicyBuilder(self._request_adapter)
