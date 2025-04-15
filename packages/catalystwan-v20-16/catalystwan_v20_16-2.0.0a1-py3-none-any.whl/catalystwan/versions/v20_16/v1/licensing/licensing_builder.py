# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .assign_licenses.assign_licenses_builder import AssignLicensesBuilder
    from .devices.devices_builder import DevicesBuilder
    from .edit_licenses.edit_licenses_builder import EditLicensesBuilder
    from .licenses.licenses_builder import LicensesBuilder
    from .release_licenses.release_licenses_builder import ReleaseLicensesBuilder
    from .sa_va_distribution.sa_va_distribution_builder import SaVaDistributionBuilder


class LicensingBuilder:
    """
    Builds and executes requests for operations under /v1/licensing
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def assign_licenses(self) -> AssignLicensesBuilder:
        """
        The assign-licenses property
        """
        from .assign_licenses.assign_licenses_builder import AssignLicensesBuilder

        return AssignLicensesBuilder(self._request_adapter)

    @property
    def devices(self) -> DevicesBuilder:
        """
        The devices property
        """
        from .devices.devices_builder import DevicesBuilder

        return DevicesBuilder(self._request_adapter)

    @property
    def edit_licenses(self) -> EditLicensesBuilder:
        """
        The edit-licenses property
        """
        from .edit_licenses.edit_licenses_builder import EditLicensesBuilder

        return EditLicensesBuilder(self._request_adapter)

    @property
    def licenses(self) -> LicensesBuilder:
        """
        The licenses property
        """
        from .licenses.licenses_builder import LicensesBuilder

        return LicensesBuilder(self._request_adapter)

    @property
    def release_licenses(self) -> ReleaseLicensesBuilder:
        """
        The release-licenses property
        """
        from .release_licenses.release_licenses_builder import ReleaseLicensesBuilder

        return ReleaseLicensesBuilder(self._request_adapter)

    @property
    def sa_va_distribution(self) -> SaVaDistributionBuilder:
        """
        The sa-va-distribution property
        """
        from .sa_va_distribution.sa_va_distribution_builder import SaVaDistributionBuilder

        return SaVaDistributionBuilder(self._request_adapter)
