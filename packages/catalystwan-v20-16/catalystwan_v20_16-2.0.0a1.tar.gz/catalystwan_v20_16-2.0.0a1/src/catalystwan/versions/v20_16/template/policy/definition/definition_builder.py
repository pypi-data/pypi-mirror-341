# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .acl.acl_builder import AclBuilder
    from .aclv6.aclv6_builder import Aclv6Builder
    from .advanced_malware_protection.advanced_malware_protection_builder import (
        AdvancedMalwareProtectionBuilder,
    )
    from .advancedinspectionprofile.advancedinspectionprofile_builder import (
        AdvancedinspectionprofileBuilder,
    )
    from .approute.approute_builder import ApprouteBuilder
    from .cflowd.cflowd_builder import CflowdBuilder
    from .control.control_builder import ControlBuilder
    from .data.data_builder import DataBuilder
    from .deviceaccesspolicy.deviceaccesspolicy_builder import DeviceaccesspolicyBuilder
    from .deviceaccesspolicyv6.deviceaccesspolicyv6_builder import Deviceaccesspolicyv6Builder
    from .dialpeer.dialpeer_builder import DialpeerBuilder
    from .dnssecurity.dnssecurity_builder import DnssecurityBuilder
    from .fxoport.fxoport_builder import FxoportBuilder
    from .fxsdidport.fxsdidport_builder import FxsdidportBuilder
    from .fxsport.fxsport_builder import FxsportBuilder
    from .hubandspoke.hubandspoke_builder import HubandspokeBuilder
    from .intrusionprevention.intrusionprevention_builder import IntrusionpreventionBuilder
    from .mesh.mesh_builder import MeshBuilder
    from .priisdnport.priisdnport_builder import PriisdnportBuilder
    from .qosmap.qosmap_builder import QosmapBuilder
    from .rewriterule.rewriterule_builder import RewriteruleBuilder
    from .ruleset.ruleset_builder import RulesetBuilder
    from .securitygroup.securitygroup_builder import SecuritygroupBuilder
    from .srstphoneprofile.srstphoneprofile_builder import SrstphoneprofileBuilder
    from .ssldecryption.ssldecryption_builder import SsldecryptionBuilder
    from .sslutdprofile.sslutdprofile_builder import SslutdprofileBuilder
    from .urlfiltering.urlfiltering_builder import UrlfilteringBuilder
    from .vedgeroute.vedgeroute_builder import VedgerouteBuilder
    from .vpnmembershipgroup.vpnmembershipgroup_builder import VpnmembershipgroupBuilder
    from .vpnqosmap.vpnqosmap_builder import VpnqosmapBuilder
    from .zonebasedfw.zonebasedfw_builder import ZonebasedfwBuilder


class DefinitionBuilder:
    """
    Builds and executes requests for operations under /template/policy/definition
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def acl(self) -> AclBuilder:
        """
        The acl property
        """
        from .acl.acl_builder import AclBuilder

        return AclBuilder(self._request_adapter)

    @property
    def aclv6(self) -> Aclv6Builder:
        """
        The aclv6 property
        """
        from .aclv6.aclv6_builder import Aclv6Builder

        return Aclv6Builder(self._request_adapter)

    @property
    def advanced_malware_protection(self) -> AdvancedMalwareProtectionBuilder:
        """
        The advancedMalwareProtection property
        """
        from .advanced_malware_protection.advanced_malware_protection_builder import (
            AdvancedMalwareProtectionBuilder,
        )

        return AdvancedMalwareProtectionBuilder(self._request_adapter)

    @property
    def advancedinspectionprofile(self) -> AdvancedinspectionprofileBuilder:
        """
        The advancedinspectionprofile property
        """
        from .advancedinspectionprofile.advancedinspectionprofile_builder import (
            AdvancedinspectionprofileBuilder,
        )

        return AdvancedinspectionprofileBuilder(self._request_adapter)

    @property
    def approute(self) -> ApprouteBuilder:
        """
        The approute property
        """
        from .approute.approute_builder import ApprouteBuilder

        return ApprouteBuilder(self._request_adapter)

    @property
    def cflowd(self) -> CflowdBuilder:
        """
        The cflowd property
        """
        from .cflowd.cflowd_builder import CflowdBuilder

        return CflowdBuilder(self._request_adapter)

    @property
    def control(self) -> ControlBuilder:
        """
        The control property
        """
        from .control.control_builder import ControlBuilder

        return ControlBuilder(self._request_adapter)

    @property
    def data(self) -> DataBuilder:
        """
        The data property
        """
        from .data.data_builder import DataBuilder

        return DataBuilder(self._request_adapter)

    @property
    def deviceaccesspolicy(self) -> DeviceaccesspolicyBuilder:
        """
        The deviceaccesspolicy property
        """
        from .deviceaccesspolicy.deviceaccesspolicy_builder import DeviceaccesspolicyBuilder

        return DeviceaccesspolicyBuilder(self._request_adapter)

    @property
    def deviceaccesspolicyv6(self) -> Deviceaccesspolicyv6Builder:
        """
        The deviceaccesspolicyv6 property
        """
        from .deviceaccesspolicyv6.deviceaccesspolicyv6_builder import Deviceaccesspolicyv6Builder

        return Deviceaccesspolicyv6Builder(self._request_adapter)

    @property
    def dialpeer(self) -> DialpeerBuilder:
        """
        The dialpeer property
        """
        from .dialpeer.dialpeer_builder import DialpeerBuilder

        return DialpeerBuilder(self._request_adapter)

    @property
    def dnssecurity(self) -> DnssecurityBuilder:
        """
        The dnssecurity property
        """
        from .dnssecurity.dnssecurity_builder import DnssecurityBuilder

        return DnssecurityBuilder(self._request_adapter)

    @property
    def fxoport(self) -> FxoportBuilder:
        """
        The fxoport property
        """
        from .fxoport.fxoport_builder import FxoportBuilder

        return FxoportBuilder(self._request_adapter)

    @property
    def fxsdidport(self) -> FxsdidportBuilder:
        """
        The fxsdidport property
        """
        from .fxsdidport.fxsdidport_builder import FxsdidportBuilder

        return FxsdidportBuilder(self._request_adapter)

    @property
    def fxsport(self) -> FxsportBuilder:
        """
        The fxsport property
        """
        from .fxsport.fxsport_builder import FxsportBuilder

        return FxsportBuilder(self._request_adapter)

    @property
    def hubandspoke(self) -> HubandspokeBuilder:
        """
        The hubandspoke property
        """
        from .hubandspoke.hubandspoke_builder import HubandspokeBuilder

        return HubandspokeBuilder(self._request_adapter)

    @property
    def intrusionprevention(self) -> IntrusionpreventionBuilder:
        """
        The intrusionprevention property
        """
        from .intrusionprevention.intrusionprevention_builder import IntrusionpreventionBuilder

        return IntrusionpreventionBuilder(self._request_adapter)

    @property
    def mesh(self) -> MeshBuilder:
        """
        The mesh property
        """
        from .mesh.mesh_builder import MeshBuilder

        return MeshBuilder(self._request_adapter)

    @property
    def priisdnport(self) -> PriisdnportBuilder:
        """
        The priisdnport property
        """
        from .priisdnport.priisdnport_builder import PriisdnportBuilder

        return PriisdnportBuilder(self._request_adapter)

    @property
    def qosmap(self) -> QosmapBuilder:
        """
        The qosmap property
        """
        from .qosmap.qosmap_builder import QosmapBuilder

        return QosmapBuilder(self._request_adapter)

    @property
    def rewriterule(self) -> RewriteruleBuilder:
        """
        The rewriterule property
        """
        from .rewriterule.rewriterule_builder import RewriteruleBuilder

        return RewriteruleBuilder(self._request_adapter)

    @property
    def ruleset(self) -> RulesetBuilder:
        """
        The ruleset property
        """
        from .ruleset.ruleset_builder import RulesetBuilder

        return RulesetBuilder(self._request_adapter)

    @property
    def securitygroup(self) -> SecuritygroupBuilder:
        """
        The securitygroup property
        """
        from .securitygroup.securitygroup_builder import SecuritygroupBuilder

        return SecuritygroupBuilder(self._request_adapter)

    @property
    def srstphoneprofile(self) -> SrstphoneprofileBuilder:
        """
        The srstphoneprofile property
        """
        from .srstphoneprofile.srstphoneprofile_builder import SrstphoneprofileBuilder

        return SrstphoneprofileBuilder(self._request_adapter)

    @property
    def ssldecryption(self) -> SsldecryptionBuilder:
        """
        The ssldecryption property
        """
        from .ssldecryption.ssldecryption_builder import SsldecryptionBuilder

        return SsldecryptionBuilder(self._request_adapter)

    @property
    def sslutdprofile(self) -> SslutdprofileBuilder:
        """
        The sslutdprofile property
        """
        from .sslutdprofile.sslutdprofile_builder import SslutdprofileBuilder

        return SslutdprofileBuilder(self._request_adapter)

    @property
    def urlfiltering(self) -> UrlfilteringBuilder:
        """
        The urlfiltering property
        """
        from .urlfiltering.urlfiltering_builder import UrlfilteringBuilder

        return UrlfilteringBuilder(self._request_adapter)

    @property
    def vedgeroute(self) -> VedgerouteBuilder:
        """
        The vedgeroute property
        """
        from .vedgeroute.vedgeroute_builder import VedgerouteBuilder

        return VedgerouteBuilder(self._request_adapter)

    @property
    def vpnmembershipgroup(self) -> VpnmembershipgroupBuilder:
        """
        The vpnmembershipgroup property
        """
        from .vpnmembershipgroup.vpnmembershipgroup_builder import VpnmembershipgroupBuilder

        return VpnmembershipgroupBuilder(self._request_adapter)

    @property
    def vpnqosmap(self) -> VpnqosmapBuilder:
        """
        The vpnqosmap property
        """
        from .vpnqosmap.vpnqosmap_builder import VpnqosmapBuilder

        return VpnqosmapBuilder(self._request_adapter)

    @property
    def zonebasedfw(self) -> ZonebasedfwBuilder:
        """
        The zonebasedfw property
        """
        from .zonebasedfw.zonebasedfw_builder import ZonebasedfwBuilder

        return ZonebasedfwBuilder(self._request_adapter)
