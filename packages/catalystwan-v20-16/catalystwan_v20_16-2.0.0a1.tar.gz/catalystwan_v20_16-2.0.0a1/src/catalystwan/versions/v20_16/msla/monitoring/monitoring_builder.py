# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .licensed_device_count.licensed_device_count_builder import LicensedDeviceCountBuilder
    from .licensed_distribution_details.licensed_distribution_details_builder import (
        LicensedDistributionDetailsBuilder,
    )
    from .packaging_distribution_details.packaging_distribution_details_builder import (
        PackagingDistributionDetailsBuilder,
    )


class MonitoringBuilder:
    """
    Builds and executes requests for operations under /msla/monitoring
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def licensed_device_count(self) -> LicensedDeviceCountBuilder:
        """
        The licensedDeviceCount property
        """
        from .licensed_device_count.licensed_device_count_builder import LicensedDeviceCountBuilder

        return LicensedDeviceCountBuilder(self._request_adapter)

    @property
    def licensed_distribution_details(self) -> LicensedDistributionDetailsBuilder:
        """
        The licensedDistributionDetails property
        """
        from .licensed_distribution_details.licensed_distribution_details_builder import (
            LicensedDistributionDetailsBuilder,
        )

        return LicensedDistributionDetailsBuilder(self._request_adapter)

    @property
    def packaging_distribution_details(self) -> PackagingDistributionDetailsBuilder:
        """
        The packagingDistributionDetails property
        """
        from .packaging_distribution_details.packaging_distribution_details_builder import (
            PackagingDistributionDetailsBuilder,
        )

        return PackagingDistributionDetailsBuilder(self._request_adapter)
