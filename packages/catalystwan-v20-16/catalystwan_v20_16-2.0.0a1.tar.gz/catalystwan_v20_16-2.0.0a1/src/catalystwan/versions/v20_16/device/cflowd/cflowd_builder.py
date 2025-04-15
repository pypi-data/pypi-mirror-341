# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .application.application_builder import ApplicationBuilder
    from .collector.collector_builder import CollectorBuilder
    from .device.device_builder import DeviceBuilder
    from .flows.flows_builder import FlowsBuilder
    from .flows_count.flows_count_builder import FlowsCountBuilder
    from .fnf.fnf_builder import FnfBuilder
    from .statistics.statistics_builder import StatisticsBuilder
    from .template.template_builder import TemplateBuilder


class CflowdBuilder:
    """
    Builds and executes requests for operations under /device/cflowd
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def application(self) -> ApplicationBuilder:
        """
        The application property
        """
        from .application.application_builder import ApplicationBuilder

        return ApplicationBuilder(self._request_adapter)

    @property
    def collector(self) -> CollectorBuilder:
        """
        The collector property
        """
        from .collector.collector_builder import CollectorBuilder

        return CollectorBuilder(self._request_adapter)

    @property
    def device(self) -> DeviceBuilder:
        """
        The device property
        """
        from .device.device_builder import DeviceBuilder

        return DeviceBuilder(self._request_adapter)

    @property
    def flows(self) -> FlowsBuilder:
        """
        The flows property
        """
        from .flows.flows_builder import FlowsBuilder

        return FlowsBuilder(self._request_adapter)

    @property
    def flows_count(self) -> FlowsCountBuilder:
        """
        The flows-count property
        """
        from .flows_count.flows_count_builder import FlowsCountBuilder

        return FlowsCountBuilder(self._request_adapter)

    @property
    def fnf(self) -> FnfBuilder:
        """
        The fnf property
        """
        from .fnf.fnf_builder import FnfBuilder

        return FnfBuilder(self._request_adapter)

    @property
    def statistics(self) -> StatisticsBuilder:
        """
        The statistics property
        """
        from .statistics.statistics_builder import StatisticsBuilder

        return StatisticsBuilder(self._request_adapter)

    @property
    def template(self) -> TemplateBuilder:
        """
        The template property
        """
        from .template.template_builder import TemplateBuilder

        return TemplateBuilder(self._request_adapter)
