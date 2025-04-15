# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .application.application_builder import ApplicationBuilder
    from .application_mapping.application_mapping_builder import ApplicationMappingBuilder
    from .applications.applications_builder import ApplicationsBuilder
    from .common.common_builder import CommonBuilder
    from .device.device_builder import DeviceBuilder
    from .devicedetails.devicedetails_builder import DevicedetailsBuilder
    from .flows.flows_builder import FlowsBuilder
    from .qosmos.qosmos_builder import QosmosBuilder
    from .qosmos_static.qosmos_static_builder import QosmosStaticBuilder
    from .summary.summary_builder import SummaryBuilder
    from .supported_applications.supported_applications_builder import SupportedApplicationsBuilder


class DpiBuilder:
    """
    Builds and executes requests for operations under /device/dpi
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
    def application_mapping(self) -> ApplicationMappingBuilder:
        """
        The application-mapping property
        """
        from .application_mapping.application_mapping_builder import ApplicationMappingBuilder

        return ApplicationMappingBuilder(self._request_adapter)

    @property
    def applications(self) -> ApplicationsBuilder:
        """
        The applications property
        """
        from .applications.applications_builder import ApplicationsBuilder

        return ApplicationsBuilder(self._request_adapter)

    @property
    def common(self) -> CommonBuilder:
        """
        The common property
        """
        from .common.common_builder import CommonBuilder

        return CommonBuilder(self._request_adapter)

    @property
    def device(self) -> DeviceBuilder:
        """
        The device property
        """
        from .device.device_builder import DeviceBuilder

        return DeviceBuilder(self._request_adapter)

    @property
    def devicedetails(self) -> DevicedetailsBuilder:
        """
        The devicedetails property
        """
        from .devicedetails.devicedetails_builder import DevicedetailsBuilder

        return DevicedetailsBuilder(self._request_adapter)

    @property
    def flows(self) -> FlowsBuilder:
        """
        The flows property
        """
        from .flows.flows_builder import FlowsBuilder

        return FlowsBuilder(self._request_adapter)

    @property
    def qosmos(self) -> QosmosBuilder:
        """
        The qosmos property
        """
        from .qosmos.qosmos_builder import QosmosBuilder

        return QosmosBuilder(self._request_adapter)

    @property
    def qosmos_static(self) -> QosmosStaticBuilder:
        """
        The qosmos-static property
        """
        from .qosmos_static.qosmos_static_builder import QosmosStaticBuilder

        return QosmosStaticBuilder(self._request_adapter)

    @property
    def summary(self) -> SummaryBuilder:
        """
        The summary property
        """
        from .summary.summary_builder import SummaryBuilder

        return SummaryBuilder(self._request_adapter)

    @property
    def supported_applications(self) -> SupportedApplicationsBuilder:
        """
        The supported-applications property
        """
        from .supported_applications.supported_applications_builder import (
            SupportedApplicationsBuilder,
        )

        return SupportedApplicationsBuilder(self._request_adapter)
