# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .analytics.analytics_builder import AnalyticsBuilder
    from .cloudservices.cloudservices_builder import CloudservicesBuilder
    from .data.data_builder import DataBuilder
    from .dcatenantowners.dcatenantowners_builder import DcatenantownersBuilder
    from .device.device_builder import DeviceBuilder
    from .settings.settings_builder import SettingsBuilder
    from .statistics.statistics_builder import StatisticsBuilder
    from .system.system_builder import SystemBuilder
    from .template.template_builder import TemplateBuilder


class DcaBuilder:
    """
    Builds and executes requests for operations under /dca
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def analytics(self) -> AnalyticsBuilder:
        """
        The analytics property
        """
        from .analytics.analytics_builder import AnalyticsBuilder

        return AnalyticsBuilder(self._request_adapter)

    @property
    def cloudservices(self) -> CloudservicesBuilder:
        """
        The cloudservices property
        """
        from .cloudservices.cloudservices_builder import CloudservicesBuilder

        return CloudservicesBuilder(self._request_adapter)

    @property
    def data(self) -> DataBuilder:
        """
        The data property
        """
        from .data.data_builder import DataBuilder

        return DataBuilder(self._request_adapter)

    @property
    def dcatenantowners(self) -> DcatenantownersBuilder:
        """
        The dcatenantowners property
        """
        from .dcatenantowners.dcatenantowners_builder import DcatenantownersBuilder

        return DcatenantownersBuilder(self._request_adapter)

    @property
    def device(self) -> DeviceBuilder:
        """
        The device property
        """
        from .device.device_builder import DeviceBuilder

        return DeviceBuilder(self._request_adapter)

    @property
    def settings(self) -> SettingsBuilder:
        """
        The settings property
        """
        from .settings.settings_builder import SettingsBuilder

        return SettingsBuilder(self._request_adapter)

    @property
    def statistics(self) -> StatisticsBuilder:
        """
        The statistics property
        """
        from .statistics.statistics_builder import StatisticsBuilder

        return StatisticsBuilder(self._request_adapter)

    @property
    def system(self) -> SystemBuilder:
        """
        The system property
        """
        from .system.system_builder import SystemBuilder

        return SystemBuilder(self._request_adapter)

    @property
    def template(self) -> TemplateBuilder:
        """
        The template property
        """
        from .template.template_builder import TemplateBuilder

        return TemplateBuilder(self._request_adapter)
