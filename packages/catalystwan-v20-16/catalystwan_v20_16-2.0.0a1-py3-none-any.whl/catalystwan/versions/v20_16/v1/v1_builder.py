# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .cloudonramp.cloudonramp_builder import CloudonrampBuilder
    from .config_group.config_group_builder import ConfigGroupBuilder
    from .device.device_builder import DeviceBuilder
    from .feature_profile.feature_profile_builder import FeatureProfileBuilder
    from .licensing.licensing_builder import LicensingBuilder
    from .multicloud.multicloud_builder import MulticloudBuilder
    from .policy_group.policy_group_builder import PolicyGroupBuilder
    from .reports.reports_builder import ReportsBuilder
    from .securedeviceonboarding.securedeviceonboarding_builder import SecuredeviceonboardingBuilder
    from .service_insertion.service_insertion_builder import ServiceInsertionBuilder
    from .smart_licensing.smart_licensing_builder import SmartLicensingBuilder
    from .topology_group.topology_group_builder import TopologyGroupBuilder


class V1Builder:
    """
    Builds and executes requests for operations under /v1
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def cloudonramp(self) -> CloudonrampBuilder:
        """
        The cloudonramp property
        """
        from .cloudonramp.cloudonramp_builder import CloudonrampBuilder

        return CloudonrampBuilder(self._request_adapter)

    @property
    def config_group(self) -> ConfigGroupBuilder:
        """
        The config-group property
        """
        from .config_group.config_group_builder import ConfigGroupBuilder

        return ConfigGroupBuilder(self._request_adapter)

    @property
    def device(self) -> DeviceBuilder:
        """
        The device property
        """
        from .device.device_builder import DeviceBuilder

        return DeviceBuilder(self._request_adapter)

    @property
    def feature_profile(self) -> FeatureProfileBuilder:
        """
        The feature-profile property
        """
        from .feature_profile.feature_profile_builder import FeatureProfileBuilder

        return FeatureProfileBuilder(self._request_adapter)

    @property
    def licensing(self) -> LicensingBuilder:
        """
        The licensing property
        """
        from .licensing.licensing_builder import LicensingBuilder

        return LicensingBuilder(self._request_adapter)

    @property
    def multicloud(self) -> MulticloudBuilder:
        """
        The multicloud property
        """
        from .multicloud.multicloud_builder import MulticloudBuilder

        return MulticloudBuilder(self._request_adapter)

    @property
    def policy_group(self) -> PolicyGroupBuilder:
        """
        The policy-group property
        """
        from .policy_group.policy_group_builder import PolicyGroupBuilder

        return PolicyGroupBuilder(self._request_adapter)

    @property
    def reports(self) -> ReportsBuilder:
        """
        The reports property
        """
        from .reports.reports_builder import ReportsBuilder

        return ReportsBuilder(self._request_adapter)

    @property
    def securedeviceonboarding(self) -> SecuredeviceonboardingBuilder:
        """
        The securedeviceonboarding property
        """
        from .securedeviceonboarding.securedeviceonboarding_builder import (
            SecuredeviceonboardingBuilder,
        )

        return SecuredeviceonboardingBuilder(self._request_adapter)

    @property
    def service_insertion(self) -> ServiceInsertionBuilder:
        """
        The service-insertion property
        """
        from .service_insertion.service_insertion_builder import ServiceInsertionBuilder

        return ServiceInsertionBuilder(self._request_adapter)

    @property
    def smart_licensing(self) -> SmartLicensingBuilder:
        """
        The smart-licensing property
        """
        from .smart_licensing.smart_licensing_builder import SmartLicensingBuilder

        return SmartLicensingBuilder(self._request_adapter)

    @property
    def topology_group(self) -> TopologyGroupBuilder:
        """
        The topology-group property
        """
        from .topology_group.topology_group_builder import TopologyGroupBuilder

        return TopologyGroupBuilder(self._request_adapter)
