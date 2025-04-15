# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .assign_licenses.assign_licenses_builder import AssignLicensesBuilder
    from .devices.devices_builder import DevicesBuilder
    from .licenses.licenses_builder import LicensesBuilder
    from .monitoring.monitoring_builder import MonitoringBuilder
    from .template.template_builder import TemplateBuilder
    from .va.va_builder import VaBuilder


class MslaBuilder:
    """
    Builds and executes requests for operations under /msla
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def assign_licenses(self) -> AssignLicensesBuilder:
        """
        The assignLicenses property
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
    def licenses(self) -> LicensesBuilder:
        """
        The licenses property
        """
        from .licenses.licenses_builder import LicensesBuilder

        return LicensesBuilder(self._request_adapter)

    @property
    def monitoring(self) -> MonitoringBuilder:
        """
        The monitoring property
        """
        from .monitoring.monitoring_builder import MonitoringBuilder

        return MonitoringBuilder(self._request_adapter)

    @property
    def template(self) -> TemplateBuilder:
        """
        The template property
        """
        from .template.template_builder import TemplateBuilder

        return TemplateBuilder(self._request_adapter)

    @property
    def va(self) -> VaBuilder:
        """
        The va property
        """
        from .va.va_builder import VaBuilder

        return VaBuilder(self._request_adapter)
