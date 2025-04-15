# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DeviceData

if TYPE_CHECKING:
    from .aaa.aaa_builder import AaaBuilder
    from .acl.acl_builder import AclBuilder
    from .action.action_builder import ActionBuilder
    from .app.app_builder import AppBuilder
    from .app_hosting.app_hosting_builder import AppHostingBuilder
    from .app_route.app_route_builder import AppRouteBuilder
    from .appqoe.appqoe_builder import AppqoeBuilder
    from .arp.arp_builder import ArpBuilder
    from .autonomousversion.autonomousversion_builder import AutonomousversionBuilder
    from .bfd.bfd_builder import BfdBuilder
    from .bgp.bgp_builder import BgpBuilder
    from .block_sync.block_sync_builder import BlockSyncBuilder
    from .bridge.bridge_builder import BridgeBuilder
    from .bytenants.bytenants_builder import BytenantsBuilder
    from .cedgecflowd.cedgecflowd_builder import CedgecflowdBuilder
    from .cellular.cellular_builder import CellularBuilder
    from .cellular_eiolte.cellular_eiolte_builder import CellularEiolteBuilder
    from .cflowd.cflowd_builder import CflowdBuilder
    from .cfm.cfm_builder import CfmBuilder
    from .cloudx.cloudx_builder import CloudxBuilder
    from .compliance.compliance_builder import ComplianceBuilder
    from .config.config_builder import ConfigBuilder
    from .configuration.configuration_builder import ConfigurationBuilder
    from .control.control_builder import ControlBuilder
    from .counters.counters_builder import CountersBuilder
    from .crashlog.crashlog_builder import CrashlogBuilder
    from .csp.csp_builder import CspBuilder
    from .cts_pac.cts_pac_builder import CtsPacBuilder
    from .devicestatus.devicestatus_builder import DevicestatusBuilder
    from .dhcp.dhcp_builder import DhcpBuilder
    from .dhcpv6.dhcpv6_builder import Dhcpv6Builder
    from .dot1x.dot1_x_builder import Dot1XBuilder
    from .downloaded_images.downloaded_images_builder import DownloadedImagesBuilder
    from .dpi.dpi_builder import DpiBuilder
    from .dre.dre_builder import DreBuilder
    from .dual_static_route_tracker.dual_static_route_tracker_builder import (
        DualStaticRouteTrackerBuilder,
    )
    from .eigrp.eigrp_builder import EigrpBuilder
    from .enable_sdavc.enable_sdavc_builder import EnableSdavcBuilder
    from .endpoint_tracker.endpoint_tracker_builder import EndpointTrackerBuilder
    from .endpoint_tracker_group.endpoint_tracker_group_builder import EndpointTrackerGroupBuilder
    from .environment_data.environment_data_builder import EnvironmentDataBuilder
    from .featurelist.featurelist_builder import FeaturelistBuilder
    from .file_based.file_based_builder import FileBasedBuilder
    from .geofence.geofence_builder import GeofenceBuilder
    from .hardware.hardware_builder import HardwareBuilder
    from .hardwarehealth.hardwarehealth_builder import HardwarehealthBuilder
    from .history.history_builder import HistoryBuilder
    from .igmp.igmp_builder import IgmpBuilder
    from .interface.interface_builder import InterfaceBuilder
    from .ip.ip_builder import IpBuilder
    from .ipsec.ipsec_builder import IpsecBuilder
    from .ipv6.ipv6_builder import Ipv6Builder
    from .keyvalue.keyvalue_builder import KeyvalueBuilder
    from .lacp.lacp_builder import LacpBuilder
    from .license.license_builder import LicenseBuilder
    from .logging.logging_builder import LoggingBuilder
    from .models_request.models_builder import ModelsBuilder
    from .monitor.monitor_builder import MonitorBuilder
    from .multicast.multicast_builder import MulticastBuilder
    from .ndv6.ndv6_builder import Ndv6Builder
    from .nms.nms_builder import NmsBuilder
    from .ntp.ntp_builder import NtpBuilder
    from .omp.omp_builder import OmpBuilder
    from .ondemand.ondemand_builder import OndemandBuilder
    from .orchestrator.orchestrator_builder import OrchestratorBuilder
    from .ospf.ospf_builder import OspfBuilder
    from .pim.pim_builder import PimBuilder
    from .pki.pki_builder import PkiBuilder
    from .policer.policer_builder import PolicerBuilder
    from .policy.policy_builder import PolicyBuilder
    from .powerconsumption.powerconsumption_builder import PowerconsumptionBuilder
    from .ppp.ppp_builder import PppBuilder
    from .pppoe.pppoe_builder import PppoeBuilder
    from .qfp.qfp_builder import QfpBuilder
    from .queues.queues_builder import QueuesBuilder
    from .reachable.reachable_builder import ReachableBuilder
    from .reboothistory.reboothistory_builder import ReboothistoryBuilder
    from .redundancy_group.redundancy_group_builder import RedundancyGroupBuilder
    from .role_based_counters.role_based_counters_builder import RoleBasedCountersBuilder
    from .role_based_ipv6_counters.role_based_ipv6_counters_builder import (
        RoleBasedIpv6CountersBuilder,
    )
    from .role_based_ipv6_permissions.role_based_ipv6_permissions_builder import (
        RoleBasedIpv6PermissionsBuilder,
    )
    from .role_based_permissions.role_based_permissions_builder import RoleBasedPermissionsBuilder
    from .role_based_sgt_map.role_based_sgt_map_builder import RoleBasedSgtMapBuilder
    from .sdwan_global_drop_statistics.sdwan_global_drop_statistics_builder import (
        SdwanGlobalDropStatisticsBuilder,
    )
    from .sdwan_stats.sdwan_stats_builder import SdwanStatsBuilder
    from .security.security_builder import SecurityBuilder
    from .sfp.sfp_builder import SfpBuilder
    from .sig.sig_builder import SigBuilder
    from .smu.smu_builder import SmuBuilder
    from .software.software_builder import SoftwareBuilder
    from .sse.sse_builder import SseBuilder
    from .sslproxy.sslproxy_builder import SslproxyBuilder
    from .static_route_tracker.static_route_tracker_builder import StaticRouteTrackerBuilder
    from .stats.stats_builder import StatsBuilder
    from .status.status_builder import StatusBuilder
    from .sxp_connections.sxp_connections_builder import SxpConnectionsBuilder
    from .sync_status.sync_status_builder import SyncStatusBuilder
    from .syncall.syncall_builder import SyncallBuilder
    from .system.system_builder import SystemBuilder
    from .tcpopt.tcpopt_builder import TcpoptBuilder
    from .tcpproxy.tcpproxy_builder import TcpproxyBuilder
    from .tier.tier_builder import TierBuilder
    from .tloc.tloc_builder import TlocBuilder
    from .tlocutil.tlocutil_builder import TlocutilBuilder
    from .tools.tools_builder import ToolsBuilder
    from .transport.transport_builder import TransportBuilder
    from .tunnel.tunnel_builder import TunnelBuilder
    from .ucse.ucse_builder import UcseBuilder
    from .umbrella.umbrella_builder import UmbrellaBuilder
    from .unclaimed.unclaimed_builder import UnclaimedBuilder
    from .unconfigured.unconfigured_builder import UnconfiguredBuilder
    from .unreachable.unreachable_builder import UnreachableBuilder
    from .users.users_builder import UsersBuilder
    from .utd.utd_builder import UtdBuilder
    from .vdsl_service.vdsl_service_builder import VdslServiceBuilder
    from .vedgeinventory.vedgeinventory_builder import VedgeinventoryBuilder
    from .virtual_application.virtual_application_builder import VirtualApplicationBuilder
    from .vm.vm_builder import VmBuilder
    from .vmanage.vmanage_builder import VmanageBuilder
    from .voice.voice_builder import VoiceBuilder
    from .voiceisdninfo.voiceisdninfo_builder import VoiceisdninfoBuilder
    from .voicet1e1controllerinfo.voicet1_e1_controllerinfo_builder import (
        Voicet1E1ControllerinfoBuilder,
    )
    from .vpn.vpn_builder import VpnBuilder
    from .vrrp.vrrp_builder import VrrpBuilder
    from .wireless.wireless_builder import WirelessBuilder
    from .wlan.wlan_builder import WlanBuilder


class DeviceBuilder:
    """
    Builds and executes requests for operations under /device
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self, site_id: Optional[str] = None, include_tenantv_smart: Optional[bool] = None, **kw
    ) -> List[DeviceData]:
        """
        List all devices
        GET /dataservice/device

        :param site_id: Site id
        :param include_tenantv_smart: Include tenantv smart
        :returns: List[DeviceData]
        """
        params = {
            "site-id": site_id,
            "includeTenantvSmart": include_tenantv_smart,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device", return_type=List[DeviceData], params=params, **kw
        )

    @property
    def aaa(self) -> AaaBuilder:
        """
        The aaa property
        """
        from .aaa.aaa_builder import AaaBuilder

        return AaaBuilder(self._request_adapter)

    @property
    def acl(self) -> AclBuilder:
        """
        The acl property
        """
        from .acl.acl_builder import AclBuilder

        return AclBuilder(self._request_adapter)

    @property
    def action(self) -> ActionBuilder:
        """
        The action property
        """
        from .action.action_builder import ActionBuilder

        return ActionBuilder(self._request_adapter)

    @property
    def app(self) -> AppBuilder:
        """
        The app property
        """
        from .app.app_builder import AppBuilder

        return AppBuilder(self._request_adapter)

    @property
    def app_hosting(self) -> AppHostingBuilder:
        """
        The app-hosting property
        """
        from .app_hosting.app_hosting_builder import AppHostingBuilder

        return AppHostingBuilder(self._request_adapter)

    @property
    def app_route(self) -> AppRouteBuilder:
        """
        The app-route property
        """
        from .app_route.app_route_builder import AppRouteBuilder

        return AppRouteBuilder(self._request_adapter)

    @property
    def appqoe(self) -> AppqoeBuilder:
        """
        The appqoe property
        """
        from .appqoe.appqoe_builder import AppqoeBuilder

        return AppqoeBuilder(self._request_adapter)

    @property
    def arp(self) -> ArpBuilder:
        """
        The arp property
        """
        from .arp.arp_builder import ArpBuilder

        return ArpBuilder(self._request_adapter)

    @property
    def autonomousversion(self) -> AutonomousversionBuilder:
        """
        The autonomousversion property
        """
        from .autonomousversion.autonomousversion_builder import AutonomousversionBuilder

        return AutonomousversionBuilder(self._request_adapter)

    @property
    def bfd(self) -> BfdBuilder:
        """
        The bfd property
        """
        from .bfd.bfd_builder import BfdBuilder

        return BfdBuilder(self._request_adapter)

    @property
    def bgp(self) -> BgpBuilder:
        """
        The bgp property
        """
        from .bgp.bgp_builder import BgpBuilder

        return BgpBuilder(self._request_adapter)

    @property
    def block_sync(self) -> BlockSyncBuilder:
        """
        The blockSync property
        """
        from .block_sync.block_sync_builder import BlockSyncBuilder

        return BlockSyncBuilder(self._request_adapter)

    @property
    def bridge(self) -> BridgeBuilder:
        """
        The bridge property
        """
        from .bridge.bridge_builder import BridgeBuilder

        return BridgeBuilder(self._request_adapter)

    @property
    def bytenants(self) -> BytenantsBuilder:
        """
        The bytenants property
        """
        from .bytenants.bytenants_builder import BytenantsBuilder

        return BytenantsBuilder(self._request_adapter)

    @property
    def cedgecflowd(self) -> CedgecflowdBuilder:
        """
        The cedgecflowd property
        """
        from .cedgecflowd.cedgecflowd_builder import CedgecflowdBuilder

        return CedgecflowdBuilder(self._request_adapter)

    @property
    def cellular(self) -> CellularBuilder:
        """
        The cellular property
        """
        from .cellular.cellular_builder import CellularBuilder

        return CellularBuilder(self._request_adapter)

    @property
    def cellular_eiolte(self) -> CellularEiolteBuilder:
        """
        The cellularEiolte property
        """
        from .cellular_eiolte.cellular_eiolte_builder import CellularEiolteBuilder

        return CellularEiolteBuilder(self._request_adapter)

    @property
    def cflowd(self) -> CflowdBuilder:
        """
        The cflowd property
        """
        from .cflowd.cflowd_builder import CflowdBuilder

        return CflowdBuilder(self._request_adapter)

    @property
    def cfm(self) -> CfmBuilder:
        """
        The cfm property
        """
        from .cfm.cfm_builder import CfmBuilder

        return CfmBuilder(self._request_adapter)

    @property
    def cloudx(self) -> CloudxBuilder:
        """
        The cloudx property
        """
        from .cloudx.cloudx_builder import CloudxBuilder

        return CloudxBuilder(self._request_adapter)

    @property
    def compliance(self) -> ComplianceBuilder:
        """
        The compliance property
        """
        from .compliance.compliance_builder import ComplianceBuilder

        return ComplianceBuilder(self._request_adapter)

    @property
    def config(self) -> ConfigBuilder:
        """
        The config property
        """
        from .config.config_builder import ConfigBuilder

        return ConfigBuilder(self._request_adapter)

    @property
    def configuration(self) -> ConfigurationBuilder:
        """
        The configuration property
        """
        from .configuration.configuration_builder import ConfigurationBuilder

        return ConfigurationBuilder(self._request_adapter)

    @property
    def control(self) -> ControlBuilder:
        """
        The control property
        """
        from .control.control_builder import ControlBuilder

        return ControlBuilder(self._request_adapter)

    @property
    def counters(self) -> CountersBuilder:
        """
        The counters property
        """
        from .counters.counters_builder import CountersBuilder

        return CountersBuilder(self._request_adapter)

    @property
    def crashlog(self) -> CrashlogBuilder:
        """
        The crashlog property
        """
        from .crashlog.crashlog_builder import CrashlogBuilder

        return CrashlogBuilder(self._request_adapter)

    @property
    def csp(self) -> CspBuilder:
        """
        The csp property
        """
        from .csp.csp_builder import CspBuilder

        return CspBuilder(self._request_adapter)

    @property
    def cts_pac(self) -> CtsPacBuilder:
        """
        The ctsPac property
        """
        from .cts_pac.cts_pac_builder import CtsPacBuilder

        return CtsPacBuilder(self._request_adapter)

    @property
    def devicestatus(self) -> DevicestatusBuilder:
        """
        The devicestatus property
        """
        from .devicestatus.devicestatus_builder import DevicestatusBuilder

        return DevicestatusBuilder(self._request_adapter)

    @property
    def dhcp(self) -> DhcpBuilder:
        """
        The dhcp property
        """
        from .dhcp.dhcp_builder import DhcpBuilder

        return DhcpBuilder(self._request_adapter)

    @property
    def dhcpv6(self) -> Dhcpv6Builder:
        """
        The dhcpv6 property
        """
        from .dhcpv6.dhcpv6_builder import Dhcpv6Builder

        return Dhcpv6Builder(self._request_adapter)

    @property
    def dot1x(self) -> Dot1XBuilder:
        """
        The dot1x property
        """
        from .dot1x.dot1_x_builder import Dot1XBuilder

        return Dot1XBuilder(self._request_adapter)

    @property
    def downloaded_images(self) -> DownloadedImagesBuilder:
        """
        The downloadedImages property
        """
        from .downloaded_images.downloaded_images_builder import DownloadedImagesBuilder

        return DownloadedImagesBuilder(self._request_adapter)

    @property
    def dpi(self) -> DpiBuilder:
        """
        The dpi property
        """
        from .dpi.dpi_builder import DpiBuilder

        return DpiBuilder(self._request_adapter)

    @property
    def dre(self) -> DreBuilder:
        """
        The dre property
        """
        from .dre.dre_builder import DreBuilder

        return DreBuilder(self._request_adapter)

    @property
    def dual_static_route_tracker(self) -> DualStaticRouteTrackerBuilder:
        """
        The dualStaticRouteTracker property
        """
        from .dual_static_route_tracker.dual_static_route_tracker_builder import (
            DualStaticRouteTrackerBuilder,
        )

        return DualStaticRouteTrackerBuilder(self._request_adapter)

    @property
    def eigrp(self) -> EigrpBuilder:
        """
        The eigrp property
        """
        from .eigrp.eigrp_builder import EigrpBuilder

        return EigrpBuilder(self._request_adapter)

    @property
    def enable_sdavc(self) -> EnableSdavcBuilder:
        """
        The enableSDAVC property
        """
        from .enable_sdavc.enable_sdavc_builder import EnableSdavcBuilder

        return EnableSdavcBuilder(self._request_adapter)

    @property
    def endpoint_tracker(self) -> EndpointTrackerBuilder:
        """
        The endpointTracker property
        """
        from .endpoint_tracker.endpoint_tracker_builder import EndpointTrackerBuilder

        return EndpointTrackerBuilder(self._request_adapter)

    @property
    def endpoint_tracker_group(self) -> EndpointTrackerGroupBuilder:
        """
        The endpointTrackerGroup property
        """
        from .endpoint_tracker_group.endpoint_tracker_group_builder import (
            EndpointTrackerGroupBuilder,
        )

        return EndpointTrackerGroupBuilder(self._request_adapter)

    @property
    def environment_data(self) -> EnvironmentDataBuilder:
        """
        The environmentData property
        """
        from .environment_data.environment_data_builder import EnvironmentDataBuilder

        return EnvironmentDataBuilder(self._request_adapter)

    @property
    def featurelist(self) -> FeaturelistBuilder:
        """
        The featurelist property
        """
        from .featurelist.featurelist_builder import FeaturelistBuilder

        return FeaturelistBuilder(self._request_adapter)

    @property
    def file_based(self) -> FileBasedBuilder:
        """
        The file-based property
        """
        from .file_based.file_based_builder import FileBasedBuilder

        return FileBasedBuilder(self._request_adapter)

    @property
    def geofence(self) -> GeofenceBuilder:
        """
        The geofence property
        """
        from .geofence.geofence_builder import GeofenceBuilder

        return GeofenceBuilder(self._request_adapter)

    @property
    def hardware(self) -> HardwareBuilder:
        """
        The hardware property
        """
        from .hardware.hardware_builder import HardwareBuilder

        return HardwareBuilder(self._request_adapter)

    @property
    def hardwarehealth(self) -> HardwarehealthBuilder:
        """
        The hardwarehealth property
        """
        from .hardwarehealth.hardwarehealth_builder import HardwarehealthBuilder

        return HardwarehealthBuilder(self._request_adapter)

    @property
    def history(self) -> HistoryBuilder:
        """
        The history property
        """
        from .history.history_builder import HistoryBuilder

        return HistoryBuilder(self._request_adapter)

    @property
    def igmp(self) -> IgmpBuilder:
        """
        The igmp property
        """
        from .igmp.igmp_builder import IgmpBuilder

        return IgmpBuilder(self._request_adapter)

    @property
    def interface(self) -> InterfaceBuilder:
        """
        The interface property
        """
        from .interface.interface_builder import InterfaceBuilder

        return InterfaceBuilder(self._request_adapter)

    @property
    def ip(self) -> IpBuilder:
        """
        The ip property
        """
        from .ip.ip_builder import IpBuilder

        return IpBuilder(self._request_adapter)

    @property
    def ipsec(self) -> IpsecBuilder:
        """
        The ipsec property
        """
        from .ipsec.ipsec_builder import IpsecBuilder

        return IpsecBuilder(self._request_adapter)

    @property
    def ipv6(self) -> Ipv6Builder:
        """
        The ipv6 property
        """
        from .ipv6.ipv6_builder import Ipv6Builder

        return Ipv6Builder(self._request_adapter)

    @property
    def keyvalue(self) -> KeyvalueBuilder:
        """
        The keyvalue property
        """
        from .keyvalue.keyvalue_builder import KeyvalueBuilder

        return KeyvalueBuilder(self._request_adapter)

    @property
    def lacp(self) -> LacpBuilder:
        """
        The lacp property
        """
        from .lacp.lacp_builder import LacpBuilder

        return LacpBuilder(self._request_adapter)

    @property
    def license(self) -> LicenseBuilder:
        """
        The license property
        """
        from .license.license_builder import LicenseBuilder

        return LicenseBuilder(self._request_adapter)

    @property
    def logging(self) -> LoggingBuilder:
        """
        The logging property
        """
        from .logging.logging_builder import LoggingBuilder

        return LoggingBuilder(self._request_adapter)

    @property
    def models(self) -> ModelsBuilder:
        """
        The models property
        """
        from .models_request.models_builder import ModelsBuilder

        return ModelsBuilder(self._request_adapter)

    @property
    def monitor(self) -> MonitorBuilder:
        """
        The monitor property
        """
        from .monitor.monitor_builder import MonitorBuilder

        return MonitorBuilder(self._request_adapter)

    @property
    def multicast(self) -> MulticastBuilder:
        """
        The multicast property
        """
        from .multicast.multicast_builder import MulticastBuilder

        return MulticastBuilder(self._request_adapter)

    @property
    def ndv6(self) -> Ndv6Builder:
        """
        The ndv6 property
        """
        from .ndv6.ndv6_builder import Ndv6Builder

        return Ndv6Builder(self._request_adapter)

    @property
    def nms(self) -> NmsBuilder:
        """
        The nms property
        """
        from .nms.nms_builder import NmsBuilder

        return NmsBuilder(self._request_adapter)

    @property
    def ntp(self) -> NtpBuilder:
        """
        The ntp property
        """
        from .ntp.ntp_builder import NtpBuilder

        return NtpBuilder(self._request_adapter)

    @property
    def omp(self) -> OmpBuilder:
        """
        The omp property
        """
        from .omp.omp_builder import OmpBuilder

        return OmpBuilder(self._request_adapter)

    @property
    def ondemand(self) -> OndemandBuilder:
        """
        The ondemand property
        """
        from .ondemand.ondemand_builder import OndemandBuilder

        return OndemandBuilder(self._request_adapter)

    @property
    def orchestrator(self) -> OrchestratorBuilder:
        """
        The orchestrator property
        """
        from .orchestrator.orchestrator_builder import OrchestratorBuilder

        return OrchestratorBuilder(self._request_adapter)

    @property
    def ospf(self) -> OspfBuilder:
        """
        The ospf property
        """
        from .ospf.ospf_builder import OspfBuilder

        return OspfBuilder(self._request_adapter)

    @property
    def pim(self) -> PimBuilder:
        """
        The pim property
        """
        from .pim.pim_builder import PimBuilder

        return PimBuilder(self._request_adapter)

    @property
    def pki(self) -> PkiBuilder:
        """
        The pki property
        """
        from .pki.pki_builder import PkiBuilder

        return PkiBuilder(self._request_adapter)

    @property
    def policer(self) -> PolicerBuilder:
        """
        The policer property
        """
        from .policer.policer_builder import PolicerBuilder

        return PolicerBuilder(self._request_adapter)

    @property
    def policy(self) -> PolicyBuilder:
        """
        The policy property
        """
        from .policy.policy_builder import PolicyBuilder

        return PolicyBuilder(self._request_adapter)

    @property
    def powerconsumption(self) -> PowerconsumptionBuilder:
        """
        The powerconsumption property
        """
        from .powerconsumption.powerconsumption_builder import PowerconsumptionBuilder

        return PowerconsumptionBuilder(self._request_adapter)

    @property
    def ppp(self) -> PppBuilder:
        """
        The ppp property
        """
        from .ppp.ppp_builder import PppBuilder

        return PppBuilder(self._request_adapter)

    @property
    def pppoe(self) -> PppoeBuilder:
        """
        The pppoe property
        """
        from .pppoe.pppoe_builder import PppoeBuilder

        return PppoeBuilder(self._request_adapter)

    @property
    def qfp(self) -> QfpBuilder:
        """
        The qfp property
        """
        from .qfp.qfp_builder import QfpBuilder

        return QfpBuilder(self._request_adapter)

    @property
    def queues(self) -> QueuesBuilder:
        """
        The queues property
        """
        from .queues.queues_builder import QueuesBuilder

        return QueuesBuilder(self._request_adapter)

    @property
    def reachable(self) -> ReachableBuilder:
        """
        The reachable property
        """
        from .reachable.reachable_builder import ReachableBuilder

        return ReachableBuilder(self._request_adapter)

    @property
    def reboothistory(self) -> ReboothistoryBuilder:
        """
        The reboothistory property
        """
        from .reboothistory.reboothistory_builder import ReboothistoryBuilder

        return ReboothistoryBuilder(self._request_adapter)

    @property
    def redundancy_group(self) -> RedundancyGroupBuilder:
        """
        The redundancy-group property
        """
        from .redundancy_group.redundancy_group_builder import RedundancyGroupBuilder

        return RedundancyGroupBuilder(self._request_adapter)

    @property
    def role_based_counters(self) -> RoleBasedCountersBuilder:
        """
        The roleBasedCounters property
        """
        from .role_based_counters.role_based_counters_builder import RoleBasedCountersBuilder

        return RoleBasedCountersBuilder(self._request_adapter)

    @property
    def role_based_ipv6_counters(self) -> RoleBasedIpv6CountersBuilder:
        """
        The roleBasedIpv6Counters property
        """
        from .role_based_ipv6_counters.role_based_ipv6_counters_builder import (
            RoleBasedIpv6CountersBuilder,
        )

        return RoleBasedIpv6CountersBuilder(self._request_adapter)

    @property
    def role_based_ipv6_permissions(self) -> RoleBasedIpv6PermissionsBuilder:
        """
        The roleBasedIpv6Permissions property
        """
        from .role_based_ipv6_permissions.role_based_ipv6_permissions_builder import (
            RoleBasedIpv6PermissionsBuilder,
        )

        return RoleBasedIpv6PermissionsBuilder(self._request_adapter)

    @property
    def role_based_permissions(self) -> RoleBasedPermissionsBuilder:
        """
        The roleBasedPermissions property
        """
        from .role_based_permissions.role_based_permissions_builder import (
            RoleBasedPermissionsBuilder,
        )

        return RoleBasedPermissionsBuilder(self._request_adapter)

    @property
    def role_based_sgt_map(self) -> RoleBasedSgtMapBuilder:
        """
        The roleBasedSgtMap property
        """
        from .role_based_sgt_map.role_based_sgt_map_builder import RoleBasedSgtMapBuilder

        return RoleBasedSgtMapBuilder(self._request_adapter)

    @property
    def sdwan_global_drop_statistics(self) -> SdwanGlobalDropStatisticsBuilder:
        """
        The sdwan-global-drop-statistics property
        """
        from .sdwan_global_drop_statistics.sdwan_global_drop_statistics_builder import (
            SdwanGlobalDropStatisticsBuilder,
        )

        return SdwanGlobalDropStatisticsBuilder(self._request_adapter)

    @property
    def sdwan_stats(self) -> SdwanStatsBuilder:
        """
        The sdwan-stats property
        """
        from .sdwan_stats.sdwan_stats_builder import SdwanStatsBuilder

        return SdwanStatsBuilder(self._request_adapter)

    @property
    def security(self) -> SecurityBuilder:
        """
        The security property
        """
        from .security.security_builder import SecurityBuilder

        return SecurityBuilder(self._request_adapter)

    @property
    def sfp(self) -> SfpBuilder:
        """
        The sfp property
        """
        from .sfp.sfp_builder import SfpBuilder

        return SfpBuilder(self._request_adapter)

    @property
    def sig(self) -> SigBuilder:
        """
        The sig property
        """
        from .sig.sig_builder import SigBuilder

        return SigBuilder(self._request_adapter)

    @property
    def smu(self) -> SmuBuilder:
        """
        The smu property
        """
        from .smu.smu_builder import SmuBuilder

        return SmuBuilder(self._request_adapter)

    @property
    def software(self) -> SoftwareBuilder:
        """
        The software property
        """
        from .software.software_builder import SoftwareBuilder

        return SoftwareBuilder(self._request_adapter)

    @property
    def sse(self) -> SseBuilder:
        """
        The sse property
        """
        from .sse.sse_builder import SseBuilder

        return SseBuilder(self._request_adapter)

    @property
    def sslproxy(self) -> SslproxyBuilder:
        """
        The sslproxy property
        """
        from .sslproxy.sslproxy_builder import SslproxyBuilder

        return SslproxyBuilder(self._request_adapter)

    @property
    def static_route_tracker(self) -> StaticRouteTrackerBuilder:
        """
        The staticRouteTracker property
        """
        from .static_route_tracker.static_route_tracker_builder import StaticRouteTrackerBuilder

        return StaticRouteTrackerBuilder(self._request_adapter)

    @property
    def stats(self) -> StatsBuilder:
        """
        The stats property
        """
        from .stats.stats_builder import StatsBuilder

        return StatsBuilder(self._request_adapter)

    @property
    def status(self) -> StatusBuilder:
        """
        The status property
        """
        from .status.status_builder import StatusBuilder

        return StatusBuilder(self._request_adapter)

    @property
    def sxp_connections(self) -> SxpConnectionsBuilder:
        """
        The sxpConnections property
        """
        from .sxp_connections.sxp_connections_builder import SxpConnectionsBuilder

        return SxpConnectionsBuilder(self._request_adapter)

    @property
    def sync_status(self) -> SyncStatusBuilder:
        """
        The sync_status property
        """
        from .sync_status.sync_status_builder import SyncStatusBuilder

        return SyncStatusBuilder(self._request_adapter)

    @property
    def syncall(self) -> SyncallBuilder:
        """
        The syncall property
        """
        from .syncall.syncall_builder import SyncallBuilder

        return SyncallBuilder(self._request_adapter)

    @property
    def system(self) -> SystemBuilder:
        """
        The system property
        """
        from .system.system_builder import SystemBuilder

        return SystemBuilder(self._request_adapter)

    @property
    def tcpopt(self) -> TcpoptBuilder:
        """
        The tcpopt property
        """
        from .tcpopt.tcpopt_builder import TcpoptBuilder

        return TcpoptBuilder(self._request_adapter)

    @property
    def tcpproxy(self) -> TcpproxyBuilder:
        """
        The tcpproxy property
        """
        from .tcpproxy.tcpproxy_builder import TcpproxyBuilder

        return TcpproxyBuilder(self._request_adapter)

    @property
    def tier(self) -> TierBuilder:
        """
        The tier property
        """
        from .tier.tier_builder import TierBuilder

        return TierBuilder(self._request_adapter)

    @property
    def tloc(self) -> TlocBuilder:
        """
        The tloc property
        """
        from .tloc.tloc_builder import TlocBuilder

        return TlocBuilder(self._request_adapter)

    @property
    def tlocutil(self) -> TlocutilBuilder:
        """
        The tlocutil property
        """
        from .tlocutil.tlocutil_builder import TlocutilBuilder

        return TlocutilBuilder(self._request_adapter)

    @property
    def tools(self) -> ToolsBuilder:
        """
        The tools property
        """
        from .tools.tools_builder import ToolsBuilder

        return ToolsBuilder(self._request_adapter)

    @property
    def transport(self) -> TransportBuilder:
        """
        The transport property
        """
        from .transport.transport_builder import TransportBuilder

        return TransportBuilder(self._request_adapter)

    @property
    def tunnel(self) -> TunnelBuilder:
        """
        The tunnel property
        """
        from .tunnel.tunnel_builder import TunnelBuilder

        return TunnelBuilder(self._request_adapter)

    @property
    def ucse(self) -> UcseBuilder:
        """
        The ucse property
        """
        from .ucse.ucse_builder import UcseBuilder

        return UcseBuilder(self._request_adapter)

    @property
    def umbrella(self) -> UmbrellaBuilder:
        """
        The umbrella property
        """
        from .umbrella.umbrella_builder import UmbrellaBuilder

        return UmbrellaBuilder(self._request_adapter)

    @property
    def unclaimed(self) -> UnclaimedBuilder:
        """
        The unclaimed property
        """
        from .unclaimed.unclaimed_builder import UnclaimedBuilder

        return UnclaimedBuilder(self._request_adapter)

    @property
    def unconfigured(self) -> UnconfiguredBuilder:
        """
        The unconfigured property
        """
        from .unconfigured.unconfigured_builder import UnconfiguredBuilder

        return UnconfiguredBuilder(self._request_adapter)

    @property
    def unreachable(self) -> UnreachableBuilder:
        """
        The unreachable property
        """
        from .unreachable.unreachable_builder import UnreachableBuilder

        return UnreachableBuilder(self._request_adapter)

    @property
    def users(self) -> UsersBuilder:
        """
        The users property
        """
        from .users.users_builder import UsersBuilder

        return UsersBuilder(self._request_adapter)

    @property
    def utd(self) -> UtdBuilder:
        """
        The utd property
        """
        from .utd.utd_builder import UtdBuilder

        return UtdBuilder(self._request_adapter)

    @property
    def vdsl_service(self) -> VdslServiceBuilder:
        """
        The vdslService property
        """
        from .vdsl_service.vdsl_service_builder import VdslServiceBuilder

        return VdslServiceBuilder(self._request_adapter)

    @property
    def vedgeinventory(self) -> VedgeinventoryBuilder:
        """
        The vedgeinventory property
        """
        from .vedgeinventory.vedgeinventory_builder import VedgeinventoryBuilder

        return VedgeinventoryBuilder(self._request_adapter)

    @property
    def virtual_application(self) -> VirtualApplicationBuilder:
        """
        The virtualApplication property
        """
        from .virtual_application.virtual_application_builder import VirtualApplicationBuilder

        return VirtualApplicationBuilder(self._request_adapter)

    @property
    def vm(self) -> VmBuilder:
        """
        The vm property
        """
        from .vm.vm_builder import VmBuilder

        return VmBuilder(self._request_adapter)

    @property
    def vmanage(self) -> VmanageBuilder:
        """
        The vmanage property
        """
        from .vmanage.vmanage_builder import VmanageBuilder

        return VmanageBuilder(self._request_adapter)

    @property
    def voice(self) -> VoiceBuilder:
        """
        The voice property
        """
        from .voice.voice_builder import VoiceBuilder

        return VoiceBuilder(self._request_adapter)

    @property
    def voiceisdninfo(self) -> VoiceisdninfoBuilder:
        """
        The voiceisdninfo property
        """
        from .voiceisdninfo.voiceisdninfo_builder import VoiceisdninfoBuilder

        return VoiceisdninfoBuilder(self._request_adapter)

    @property
    def voicet1e1controllerinfo(self) -> Voicet1E1ControllerinfoBuilder:
        """
        The voicet1e1controllerinfo property
        """
        from .voicet1e1controllerinfo.voicet1_e1_controllerinfo_builder import (
            Voicet1E1ControllerinfoBuilder,
        )

        return Voicet1E1ControllerinfoBuilder(self._request_adapter)

    @property
    def vpn(self) -> VpnBuilder:
        """
        The vpn property
        """
        from .vpn.vpn_builder import VpnBuilder

        return VpnBuilder(self._request_adapter)

    @property
    def vrrp(self) -> VrrpBuilder:
        """
        The vrrp property
        """
        from .vrrp.vrrp_builder import VrrpBuilder

        return VrrpBuilder(self._request_adapter)

    @property
    def wireless(self) -> WirelessBuilder:
        """
        The wireless property
        """
        from .wireless.wireless_builder import WirelessBuilder

        return WirelessBuilder(self._request_adapter)

    @property
    def wlan(self) -> WlanBuilder:
        """
        The wlan property
        """
        from .wlan.wlan_builder import WlanBuilder

        return WlanBuilder(self._request_adapter)
