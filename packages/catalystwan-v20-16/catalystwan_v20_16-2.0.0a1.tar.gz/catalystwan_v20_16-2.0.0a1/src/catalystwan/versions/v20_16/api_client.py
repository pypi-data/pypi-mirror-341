# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .accesstoken.accesstoken_builder import AccesstokenBuilder
    from .admin.admin_builder import AdminBuilder
    from .alarms.alarms_builder import AlarmsBuilder
    from .app_registry.app_registry_builder import AppRegistryBuilder
    from .auditlog.auditlog_builder import AuditlogBuilder
    from .backup.backup_builder import BackupBuilder
    from .cdna.cdna_builder import CdnaBuilder
    from .certificate.certificate_builder import CertificateBuilder
    from .client.client_builder import ClientBuilder
    from .cloudservices.cloudservices_builder import CloudservicesBuilder
    from .cluster_management.cluster_management_builder import ClusterManagementBuilder
    from .colocation.colocation_builder import ColocationBuilder
    from .container_manager.container_manager_builder import ContainerManagerBuilder
    from .data.data_builder import DataBuilder
    from .dca.dca_builder import DcaBuilder
    from .device.device_builder import DeviceBuilder
    from .device_authorization.device_authorization_builder import DeviceAuthorizationBuilder
    from .disasterrecovery.disasterrecovery_builder import DisasterrecoveryBuilder
    from .entityownership.entityownership_builder import EntityownershipBuilder
    from .event.event_builder import EventBuilder
    from .featurecertificate.featurecertificate_builder import FeaturecertificateBuilder
    from .fedramp.fedramp_builder import FedrampBuilder
    from .group.group_builder import GroupBuilder
    from .health.health_builder import HealthBuilder
    from .hsec.hsec_builder import HsecBuilder
    from .ise.ise_builder import IseBuilder
    from .localization.localization_builder import LocalizationBuilder
    from .management.management_builder import ManagementBuilder
    from .mdp.mdp_builder import MdpBuilder
    from .messaging.messaging_builder import MessagingBuilder
    from .monitor.monitor_builder import MonitorBuilder
    from .msla.msla_builder import MslaBuilder
    from .multicloud.multicloud_builder import MulticloudBuilder
    from .network.network_builder import NetworkBuilder
    from .networkdesign.networkdesign_builder import NetworkdesignBuilder
    from .notifications.notifications_builder import NotificationsBuilder
    from .onboard.onboard_builder import OnboardBuilder
    from .opentaccase.opentaccase_builder import OpentaccaseBuilder
    from .partner.partner_builder import PartnerBuilder
    from .policy.policy_builder import PolicyBuilder
    from .refreshtoken.refreshtoken_builder import RefreshtokenBuilder
    from .resourcepool.resourcepool_builder import ResourcepoolBuilder
    from .restore.restore_builder import RestoreBuilder
    from .schedule.schedule_builder import ScheduleBuilder
    from .sdavc.sdavc_builder import SdavcBuilder
    from .security.security_builder import SecurityBuilder
    from .segment.segment_builder import SegmentBuilder
    from .server.server_builder import ServerBuilder
    from .serverlongpoll.serverlongpoll_builder import ServerlongpollBuilder
    from .setting.setting_builder import SettingBuilder
    from .settings.settings_builder import SettingsBuilder
    from .sig.sig_builder import SigBuilder
    from .smart_licensing.smart_licensing_builder import SmartLicensingBuilder
    from .software.software_builder import SoftwareBuilder
    from .sslproxy.sslproxy_builder import SslproxyBuilder
    from .statistics.statistics_builder import StatisticsBuilder
    from .stream.stream_builder import StreamBuilder
    from .system.system_builder import SystemBuilder
    from .template.template_builder import TemplateBuilder
    from .tenant.tenant_builder import TenantBuilder
    from .tenantbackup.tenantbackup_builder import TenantbackupBuilder
    from .tenantmigration.tenantmigration_builder import TenantmigrationBuilder
    from .tenantstatus.tenantstatus_builder import TenantstatusBuilder
    from .token.token_builder import TokenBuilder
    from .topology.topology_builder import TopologyBuilder
    from .troubleshooting.troubleshooting_builder import TroubleshootingBuilder
    from .umbrella.umbrella_builder import UmbrellaBuilder
    from .ump.ump_builder import UmpBuilder
    from .url.url_builder import UrlBuilder
    from .util.util_builder import UtilBuilder
    from .v1.v1_builder import V1Builder
    from .v2.v2_builder import V2Builder
    from .wani.wani_builder import WaniBuilder
    from .webex.webex_builder import WebexBuilder


class ApiClient:
    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def accesstoken(self) -> AccesstokenBuilder:
        """
        The accesstoken property
        """
        from .accesstoken.accesstoken_builder import AccesstokenBuilder

        return AccesstokenBuilder(self._request_adapter)

    @property
    def admin(self) -> AdminBuilder:
        """
        The admin property
        """
        from .admin.admin_builder import AdminBuilder

        return AdminBuilder(self._request_adapter)

    @property
    def alarms(self) -> AlarmsBuilder:
        """
        The alarms property
        """
        from .alarms.alarms_builder import AlarmsBuilder

        return AlarmsBuilder(self._request_adapter)

    @property
    def api_version(self) -> Literal["20.16"]:
        return "20.16"

    @property
    def app_registry(self) -> AppRegistryBuilder:
        """
        The app-registry property
        """
        from .app_registry.app_registry_builder import AppRegistryBuilder

        return AppRegistryBuilder(self._request_adapter)

    @property
    def auditlog(self) -> AuditlogBuilder:
        """
        The auditlog property
        """
        from .auditlog.auditlog_builder import AuditlogBuilder

        return AuditlogBuilder(self._request_adapter)

    @property
    def backup(self) -> BackupBuilder:
        """
        The backup property
        """
        from .backup.backup_builder import BackupBuilder

        return BackupBuilder(self._request_adapter)

    @property
    def cdna(self) -> CdnaBuilder:
        """
        The cdna property
        """
        from .cdna.cdna_builder import CdnaBuilder

        return CdnaBuilder(self._request_adapter)

    @property
    def certificate(self) -> CertificateBuilder:
        """
        The certificate property
        """
        from .certificate.certificate_builder import CertificateBuilder

        return CertificateBuilder(self._request_adapter)

    @property
    def client(self) -> ClientBuilder:
        """
        The client property
        """
        from .client.client_builder import ClientBuilder

        return ClientBuilder(self._request_adapter)

    @property
    def cloudservices(self) -> CloudservicesBuilder:
        """
        The cloudservices property
        """
        from .cloudservices.cloudservices_builder import CloudservicesBuilder

        return CloudservicesBuilder(self._request_adapter)

    @property
    def cluster_management(self) -> ClusterManagementBuilder:
        """
        The clusterManagement property
        """
        from .cluster_management.cluster_management_builder import ClusterManagementBuilder

        return ClusterManagementBuilder(self._request_adapter)

    @property
    def colocation(self) -> ColocationBuilder:
        """
        The colocation property
        """
        from .colocation.colocation_builder import ColocationBuilder

        return ColocationBuilder(self._request_adapter)

    @property
    def container_manager(self) -> ContainerManagerBuilder:
        """
        The container-manager property
        """
        from .container_manager.container_manager_builder import ContainerManagerBuilder

        return ContainerManagerBuilder(self._request_adapter)

    @property
    def data(self) -> DataBuilder:
        """
        The data property
        """
        from .data.data_builder import DataBuilder

        return DataBuilder(self._request_adapter)

    @property
    def dca(self) -> DcaBuilder:
        """
        The dca property
        """
        from .dca.dca_builder import DcaBuilder

        return DcaBuilder(self._request_adapter)

    @property
    def device(self) -> DeviceBuilder:
        """
        The device property
        """
        from .device.device_builder import DeviceBuilder

        return DeviceBuilder(self._request_adapter)

    @property
    def device_authorization(self) -> DeviceAuthorizationBuilder:
        """
        The device_authorization property
        """
        from .device_authorization.device_authorization_builder import DeviceAuthorizationBuilder

        return DeviceAuthorizationBuilder(self._request_adapter)

    @property
    def disasterrecovery(self) -> DisasterrecoveryBuilder:
        """
        The disasterrecovery property
        """
        from .disasterrecovery.disasterrecovery_builder import DisasterrecoveryBuilder

        return DisasterrecoveryBuilder(self._request_adapter)

    @property
    def entityownership(self) -> EntityownershipBuilder:
        """
        The entityownership property
        """
        from .entityownership.entityownership_builder import EntityownershipBuilder

        return EntityownershipBuilder(self._request_adapter)

    @property
    def event(self) -> EventBuilder:
        """
        The event property
        """
        from .event.event_builder import EventBuilder

        return EventBuilder(self._request_adapter)

    @property
    def featurecertificate(self) -> FeaturecertificateBuilder:
        """
        The featurecertificate property
        """
        from .featurecertificate.featurecertificate_builder import FeaturecertificateBuilder

        return FeaturecertificateBuilder(self._request_adapter)

    @property
    def fedramp(self) -> FedrampBuilder:
        """
        The fedramp property
        """
        from .fedramp.fedramp_builder import FedrampBuilder

        return FedrampBuilder(self._request_adapter)

    @property
    def group(self) -> GroupBuilder:
        """
        The group property
        """
        from .group.group_builder import GroupBuilder

        return GroupBuilder(self._request_adapter)

    @property
    def health(self) -> HealthBuilder:
        """
        The health property
        """
        from .health.health_builder import HealthBuilder

        return HealthBuilder(self._request_adapter)

    @property
    def hsec(self) -> HsecBuilder:
        """
        The hsec property
        """
        from .hsec.hsec_builder import HsecBuilder

        return HsecBuilder(self._request_adapter)

    @property
    def ise(self) -> IseBuilder:
        """
        The ise property
        """
        from .ise.ise_builder import IseBuilder

        return IseBuilder(self._request_adapter)

    @property
    def localization(self) -> LocalizationBuilder:
        """
        The localization property
        """
        from .localization.localization_builder import LocalizationBuilder

        return LocalizationBuilder(self._request_adapter)

    @property
    def management(self) -> ManagementBuilder:
        """
        The management property
        """
        from .management.management_builder import ManagementBuilder

        return ManagementBuilder(self._request_adapter)

    @property
    def mdp(self) -> MdpBuilder:
        """
        The mdp property
        """
        from .mdp.mdp_builder import MdpBuilder

        return MdpBuilder(self._request_adapter)

    @property
    def messaging(self) -> MessagingBuilder:
        """
        The messaging property
        """
        from .messaging.messaging_builder import MessagingBuilder

        return MessagingBuilder(self._request_adapter)

    @property
    def monitor(self) -> MonitorBuilder:
        """
        The monitor property
        """
        from .monitor.monitor_builder import MonitorBuilder

        return MonitorBuilder(self._request_adapter)

    @property
    def msla(self) -> MslaBuilder:
        """
        The msla property
        """
        from .msla.msla_builder import MslaBuilder

        return MslaBuilder(self._request_adapter)

    @property
    def multicloud(self) -> MulticloudBuilder:
        """
        The multicloud property
        """
        from .multicloud.multicloud_builder import MulticloudBuilder

        return MulticloudBuilder(self._request_adapter)

    @property
    def network(self) -> NetworkBuilder:
        """
        The network property
        """
        from .network.network_builder import NetworkBuilder

        return NetworkBuilder(self._request_adapter)

    @property
    def networkdesign(self) -> NetworkdesignBuilder:
        """
        The networkdesign property
        """
        from .networkdesign.networkdesign_builder import NetworkdesignBuilder

        return NetworkdesignBuilder(self._request_adapter)

    @property
    def notifications(self) -> NotificationsBuilder:
        """
        The notifications property
        """
        from .notifications.notifications_builder import NotificationsBuilder

        return NotificationsBuilder(self._request_adapter)

    @property
    def onboard(self) -> OnboardBuilder:
        """
        The onboard property
        """
        from .onboard.onboard_builder import OnboardBuilder

        return OnboardBuilder(self._request_adapter)

    @property
    def opentaccase(self) -> OpentaccaseBuilder:
        """
        The opentaccase property
        """
        from .opentaccase.opentaccase_builder import OpentaccaseBuilder

        return OpentaccaseBuilder(self._request_adapter)

    @property
    def partner(self) -> PartnerBuilder:
        """
        The partner property
        """
        from .partner.partner_builder import PartnerBuilder

        return PartnerBuilder(self._request_adapter)

    @property
    def policy(self) -> PolicyBuilder:
        """
        The policy property
        """
        from .policy.policy_builder import PolicyBuilder

        return PolicyBuilder(self._request_adapter)

    @property
    def refreshtoken(self) -> RefreshtokenBuilder:
        """
        The refreshtoken property
        """
        from .refreshtoken.refreshtoken_builder import RefreshtokenBuilder

        return RefreshtokenBuilder(self._request_adapter)

    @property
    def resourcepool(self) -> ResourcepoolBuilder:
        """
        The resourcepool property
        """
        from .resourcepool.resourcepool_builder import ResourcepoolBuilder

        return ResourcepoolBuilder(self._request_adapter)

    @property
    def restore(self) -> RestoreBuilder:
        """
        The restore property
        """
        from .restore.restore_builder import RestoreBuilder

        return RestoreBuilder(self._request_adapter)

    @property
    def schedule(self) -> ScheduleBuilder:
        """
        The schedule property
        """
        from .schedule.schedule_builder import ScheduleBuilder

        return ScheduleBuilder(self._request_adapter)

    @property
    def sdavc(self) -> SdavcBuilder:
        """
        The sdavc property
        """
        from .sdavc.sdavc_builder import SdavcBuilder

        return SdavcBuilder(self._request_adapter)

    @property
    def security(self) -> SecurityBuilder:
        """
        The security property
        """
        from .security.security_builder import SecurityBuilder

        return SecurityBuilder(self._request_adapter)

    @property
    def segment(self) -> SegmentBuilder:
        """
        The segment property
        """
        from .segment.segment_builder import SegmentBuilder

        return SegmentBuilder(self._request_adapter)

    @property
    def server(self) -> ServerBuilder:
        """
        The server property
        """
        from .server.server_builder import ServerBuilder

        return ServerBuilder(self._request_adapter)

    @property
    def serverlongpoll(self) -> ServerlongpollBuilder:
        """
        The serverlongpoll property
        """
        from .serverlongpoll.serverlongpoll_builder import ServerlongpollBuilder

        return ServerlongpollBuilder(self._request_adapter)

    @property
    def setting(self) -> SettingBuilder:
        """
        The setting property
        """
        from .setting.setting_builder import SettingBuilder

        return SettingBuilder(self._request_adapter)

    @property
    def settings(self) -> SettingsBuilder:
        """
        The settings property
        """
        from .settings.settings_builder import SettingsBuilder

        return SettingsBuilder(self._request_adapter)

    @property
    def sig(self) -> SigBuilder:
        """
        The sig property
        """
        from .sig.sig_builder import SigBuilder

        return SigBuilder(self._request_adapter)

    @property
    def smart_licensing(self) -> SmartLicensingBuilder:
        """
        The smartLicensing property
        """
        from .smart_licensing.smart_licensing_builder import SmartLicensingBuilder

        return SmartLicensingBuilder(self._request_adapter)

    @property
    def software(self) -> SoftwareBuilder:
        """
        The software property
        """
        from .software.software_builder import SoftwareBuilder

        return SoftwareBuilder(self._request_adapter)

    @property
    def sslproxy(self) -> SslproxyBuilder:
        """
        The sslproxy property
        """
        from .sslproxy.sslproxy_builder import SslproxyBuilder

        return SslproxyBuilder(self._request_adapter)

    @property
    def statistics(self) -> StatisticsBuilder:
        """
        The statistics property
        """
        from .statistics.statistics_builder import StatisticsBuilder

        return StatisticsBuilder(self._request_adapter)

    @property
    def stream(self) -> StreamBuilder:
        """
        The stream property
        """
        from .stream.stream_builder import StreamBuilder

        return StreamBuilder(self._request_adapter)

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

    @property
    def tenant(self) -> TenantBuilder:
        """
        The tenant property
        """
        from .tenant.tenant_builder import TenantBuilder

        return TenantBuilder(self._request_adapter)

    @property
    def tenantbackup(self) -> TenantbackupBuilder:
        """
        The tenantbackup property
        """
        from .tenantbackup.tenantbackup_builder import TenantbackupBuilder

        return TenantbackupBuilder(self._request_adapter)

    @property
    def tenantmigration(self) -> TenantmigrationBuilder:
        """
        The tenantmigration property
        """
        from .tenantmigration.tenantmigration_builder import TenantmigrationBuilder

        return TenantmigrationBuilder(self._request_adapter)

    @property
    def tenantstatus(self) -> TenantstatusBuilder:
        """
        The tenantstatus property
        """
        from .tenantstatus.tenantstatus_builder import TenantstatusBuilder

        return TenantstatusBuilder(self._request_adapter)

    @property
    def token(self) -> TokenBuilder:
        """
        The token property
        """
        from .token.token_builder import TokenBuilder

        return TokenBuilder(self._request_adapter)

    @property
    def topology(self) -> TopologyBuilder:
        """
        The topology property
        """
        from .topology.topology_builder import TopologyBuilder

        return TopologyBuilder(self._request_adapter)

    @property
    def troubleshooting(self) -> TroubleshootingBuilder:
        """
        The troubleshooting property
        """
        from .troubleshooting.troubleshooting_builder import TroubleshootingBuilder

        return TroubleshootingBuilder(self._request_adapter)

    @property
    def umbrella(self) -> UmbrellaBuilder:
        """
        The umbrella property
        """
        from .umbrella.umbrella_builder import UmbrellaBuilder

        return UmbrellaBuilder(self._request_adapter)

    @property
    def ump(self) -> UmpBuilder:
        """
        The ump property
        """
        from .ump.ump_builder import UmpBuilder

        return UmpBuilder(self._request_adapter)

    @property
    def url(self) -> UrlBuilder:
        """
        The url property
        """
        from .url.url_builder import UrlBuilder

        return UrlBuilder(self._request_adapter)

    @property
    def util(self) -> UtilBuilder:
        """
        The util property
        """
        from .util.util_builder import UtilBuilder

        return UtilBuilder(self._request_adapter)

    @property
    def v1(self) -> V1Builder:
        """
        The v1 property
        """
        from .v1.v1_builder import V1Builder

        return V1Builder(self._request_adapter)

    @property
    def v2(self) -> V2Builder:
        """
        The v2 property
        """
        from .v2.v2_builder import V2Builder

        return V2Builder(self._request_adapter)

    @property
    def wani(self) -> WaniBuilder:
        """
        The wani property
        """
        from .wani.wani_builder import WaniBuilder

        return WaniBuilder(self._request_adapter)

    @property
    def webex(self) -> WebexBuilder:
        """
        The webex property
        """
        from .webex.webex_builder import WebexBuilder

        return WebexBuilder(self._request_adapter)
