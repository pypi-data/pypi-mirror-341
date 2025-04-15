# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .active_flow_id.active_flow_id_builder import ActiveFlowIdBuilder
    from .appqoe_hput_stats.appqoe_hput_stats_builder import AppqoeHputStatsBuilder
    from .appqoe_nat_stats.appqoe_nat_stats_builder import AppqoeNatStatsBuilder
    from .appqoe_rm_resource.appqoe_rm_resource_builder import AppqoeRmResourceBuilder
    from .appqoe_rm_stats.appqoe_rm_stats_builder import AppqoeRmStatsBuilder
    from .appqoe_services_status.appqoe_services_status_builder import AppqoeServicesStatusBuilder
    from .appqoe_sppi_pipe_resource.appqoe_sppi_pipe_resource_builder import (
        AppqoeSppiPipeResourceBuilder,
    )
    from .appqoe_sppi_queue_resource.appqoe_sppi_queue_resource_builder import (
        AppqoeSppiQueueResourceBuilder,
    )
    from .cluster_summary.cluster_summary_builder import ClusterSummaryBuilder
    from .error_recent.error_recent_builder import ErrorRecentBuilder
    from .expired_flow_id.expired_flow_id_builder import ExpiredFlowIdBuilder
    from .flow_closed_error.flow_closed_error_builder import FlowClosedErrorBuilder
    from .flow_expired.flow_expired_builder import FlowExpiredBuilder
    from .service_controllers.service_controllers_builder import ServiceControllersBuilder
    from .status.status_builder import StatusBuilder
    from .vpn_id.vpn_id_builder import VpnIdBuilder


class AppqoeBuilder:
    """
    Builds and executes requests for operations under /device/appqoe
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def active_flow_id(self) -> ActiveFlowIdBuilder:
        """
        The active-flow-id property
        """
        from .active_flow_id.active_flow_id_builder import ActiveFlowIdBuilder

        return ActiveFlowIdBuilder(self._request_adapter)

    @property
    def appqoe_hput_stats(self) -> AppqoeHputStatsBuilder:
        """
        The appqoe-hput-stats property
        """
        from .appqoe_hput_stats.appqoe_hput_stats_builder import AppqoeHputStatsBuilder

        return AppqoeHputStatsBuilder(self._request_adapter)

    @property
    def appqoe_nat_stats(self) -> AppqoeNatStatsBuilder:
        """
        The appqoe-nat-stats property
        """
        from .appqoe_nat_stats.appqoe_nat_stats_builder import AppqoeNatStatsBuilder

        return AppqoeNatStatsBuilder(self._request_adapter)

    @property
    def appqoe_rm_resource(self) -> AppqoeRmResourceBuilder:
        """
        The appqoe-rm-resource property
        """
        from .appqoe_rm_resource.appqoe_rm_resource_builder import AppqoeRmResourceBuilder

        return AppqoeRmResourceBuilder(self._request_adapter)

    @property
    def appqoe_rm_stats(self) -> AppqoeRmStatsBuilder:
        """
        The appqoe-rm-stats property
        """
        from .appqoe_rm_stats.appqoe_rm_stats_builder import AppqoeRmStatsBuilder

        return AppqoeRmStatsBuilder(self._request_adapter)

    @property
    def appqoe_services_status(self) -> AppqoeServicesStatusBuilder:
        """
        The appqoe-services-status property
        """
        from .appqoe_services_status.appqoe_services_status_builder import (
            AppqoeServicesStatusBuilder,
        )

        return AppqoeServicesStatusBuilder(self._request_adapter)

    @property
    def appqoe_sppi_pipe_resource(self) -> AppqoeSppiPipeResourceBuilder:
        """
        The appqoe-sppi-pipe-resource property
        """
        from .appqoe_sppi_pipe_resource.appqoe_sppi_pipe_resource_builder import (
            AppqoeSppiPipeResourceBuilder,
        )

        return AppqoeSppiPipeResourceBuilder(self._request_adapter)

    @property
    def appqoe_sppi_queue_resource(self) -> AppqoeSppiQueueResourceBuilder:
        """
        The appqoe-sppi-queue-resource property
        """
        from .appqoe_sppi_queue_resource.appqoe_sppi_queue_resource_builder import (
            AppqoeSppiQueueResourceBuilder,
        )

        return AppqoeSppiQueueResourceBuilder(self._request_adapter)

    @property
    def cluster_summary(self) -> ClusterSummaryBuilder:
        """
        The cluster-summary property
        """
        from .cluster_summary.cluster_summary_builder import ClusterSummaryBuilder

        return ClusterSummaryBuilder(self._request_adapter)

    @property
    def error_recent(self) -> ErrorRecentBuilder:
        """
        The error-recent property
        """
        from .error_recent.error_recent_builder import ErrorRecentBuilder

        return ErrorRecentBuilder(self._request_adapter)

    @property
    def expired_flow_id(self) -> ExpiredFlowIdBuilder:
        """
        The expired-flow-id property
        """
        from .expired_flow_id.expired_flow_id_builder import ExpiredFlowIdBuilder

        return ExpiredFlowIdBuilder(self._request_adapter)

    @property
    def flow_closed_error(self) -> FlowClosedErrorBuilder:
        """
        The flow-closed-error property
        """
        from .flow_closed_error.flow_closed_error_builder import FlowClosedErrorBuilder

        return FlowClosedErrorBuilder(self._request_adapter)

    @property
    def flow_expired(self) -> FlowExpiredBuilder:
        """
        The flow-expired property
        """
        from .flow_expired.flow_expired_builder import FlowExpiredBuilder

        return FlowExpiredBuilder(self._request_adapter)

    @property
    def service_controllers(self) -> ServiceControllersBuilder:
        """
        The service-controllers property
        """
        from .service_controllers.service_controllers_builder import ServiceControllersBuilder

        return ServiceControllersBuilder(self._request_adapter)

    @property
    def status(self) -> StatusBuilder:
        """
        The status property
        """
        from .status.status_builder import StatusBuilder

        return StatusBuilder(self._request_adapter)

    @property
    def vpn_id(self) -> VpnIdBuilder:
        """
        The vpn-id property
        """
        from .vpn_id.vpn_id_builder import VpnIdBuilder

        return VpnIdBuilder(self._request_adapter)
