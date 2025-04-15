# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .app.app_builder import AppBuilder
    from .appprobe.appprobe_builder import AppprobeBuilder
    from .aspath.aspath_builder import AspathBuilder
    from .class_.class_builder import ClassBuilder
    from .color.color_builder import ColorBuilder
    from .community.community_builder import CommunityBuilder
    from .dataipv6prefix.dataipv6_prefix_builder import Dataipv6PrefixBuilder
    from .dataprefix.dataprefix_builder import DataprefixBuilder
    from .dataprefixall.dataprefixall_builder import DataprefixallBuilder
    from .dataprefixfqdn.dataprefixfqdn_builder import DataprefixfqdnBuilder
    from .expandedcommunity.expandedcommunity_builder import ExpandedcommunityBuilder
    from .extcommunity.extcommunity_builder import ExtcommunityBuilder
    from .faxprotocol.faxprotocol_builder import FaxprotocolBuilder
    from .fqdn.fqdn_builder import FqdnBuilder
    from .geolocation.geolocation_builder import GeolocationBuilder
    from .identity.identity_builder import IdentityBuilder
    from .ipprefixall.ipprefixall_builder import IpprefixallBuilder
    from .ipssignature.ipssignature_builder import IpssignatureBuilder
    from .ipv6prefix.ipv6_prefix_builder import Ipv6PrefixBuilder
    from .localapp.localapp_builder import LocalappBuilder
    from .localdomain.localdomain_builder import LocaldomainBuilder
    from .mediaprofile.mediaprofile_builder import MediaprofileBuilder
    from .mirror.mirror_builder import MirrorBuilder
    from .modempassthrough.modempassthrough_builder import ModempassthroughBuilder
    from .policer.policer_builder import PolicerBuilder
    from .port.port_builder import PortBuilder
    from .preferredcolorgroup.preferredcolorgroup_builder import PreferredcolorgroupBuilder
    from .prefix.prefix_builder import PrefixBuilder
    from .protocolname.protocolname_builder import ProtocolnameBuilder
    from .region.region_builder import RegionBuilder
    from .scalablegrouptag.scalablegrouptag_builder import ScalablegrouptagBuilder
    from .site.site_builder import SiteBuilder
    from .sla.sla_builder import SlaBuilder
    from .supervisorydisc.supervisorydisc_builder import SupervisorydiscBuilder
    from .tgapikey.tgapikey_builder import TgapikeyBuilder
    from .tloc.tloc_builder import TlocBuilder
    from .translationprofile.translationprofile_builder import TranslationprofileBuilder
    from .translationrules.translationrules_builder import TranslationrulesBuilder
    from .trunkgroup.trunkgroup_builder import TrunkgroupBuilder
    from .umbrelladata.umbrelladata_builder import UmbrelladataBuilder
    from .urlblacklist.urlblacklist_builder import UrlblacklistBuilder
    from .urlwhitelist.urlwhitelist_builder import UrlwhitelistBuilder
    from .vpn.vpn_builder import VpnBuilder
    from .webex.webex_builder import WebexBuilder
    from .zone.zone_builder import ZoneBuilder


class ListBuilder:
    """
    Builds and executes requests for operations under /template/policy/list
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[Any]:
        """
        Get all policy lists
        GET /dataservice/template/policy/list

        :returns: List[Any]
        """
        return self._request_adapter.request(
            "GET", "/dataservice/template/policy/list", return_type=List[Any], **kw
        )

    @property
    def app(self) -> AppBuilder:
        """
        The app property
        """
        from .app.app_builder import AppBuilder

        return AppBuilder(self._request_adapter)

    @property
    def appprobe(self) -> AppprobeBuilder:
        """
        The appprobe property
        """
        from .appprobe.appprobe_builder import AppprobeBuilder

        return AppprobeBuilder(self._request_adapter)

    @property
    def aspath(self) -> AspathBuilder:
        """
        The aspath property
        """
        from .aspath.aspath_builder import AspathBuilder

        return AspathBuilder(self._request_adapter)

    @property
    def class_(self) -> ClassBuilder:
        """
        The class property
        """
        from .class_.class_builder import ClassBuilder

        return ClassBuilder(self._request_adapter)

    @property
    def color(self) -> ColorBuilder:
        """
        The color property
        """
        from .color.color_builder import ColorBuilder

        return ColorBuilder(self._request_adapter)

    @property
    def community(self) -> CommunityBuilder:
        """
        The community property
        """
        from .community.community_builder import CommunityBuilder

        return CommunityBuilder(self._request_adapter)

    @property
    def dataipv6prefix(self) -> Dataipv6PrefixBuilder:
        """
        The dataipv6prefix property
        """
        from .dataipv6prefix.dataipv6_prefix_builder import Dataipv6PrefixBuilder

        return Dataipv6PrefixBuilder(self._request_adapter)

    @property
    def dataprefix(self) -> DataprefixBuilder:
        """
        The dataprefix property
        """
        from .dataprefix.dataprefix_builder import DataprefixBuilder

        return DataprefixBuilder(self._request_adapter)

    @property
    def dataprefixall(self) -> DataprefixallBuilder:
        """
        The dataprefixall property
        """
        from .dataprefixall.dataprefixall_builder import DataprefixallBuilder

        return DataprefixallBuilder(self._request_adapter)

    @property
    def dataprefixfqdn(self) -> DataprefixfqdnBuilder:
        """
        The dataprefixfqdn property
        """
        from .dataprefixfqdn.dataprefixfqdn_builder import DataprefixfqdnBuilder

        return DataprefixfqdnBuilder(self._request_adapter)

    @property
    def expandedcommunity(self) -> ExpandedcommunityBuilder:
        """
        The expandedcommunity property
        """
        from .expandedcommunity.expandedcommunity_builder import ExpandedcommunityBuilder

        return ExpandedcommunityBuilder(self._request_adapter)

    @property
    def extcommunity(self) -> ExtcommunityBuilder:
        """
        The extcommunity property
        """
        from .extcommunity.extcommunity_builder import ExtcommunityBuilder

        return ExtcommunityBuilder(self._request_adapter)

    @property
    def faxprotocol(self) -> FaxprotocolBuilder:
        """
        The faxprotocol property
        """
        from .faxprotocol.faxprotocol_builder import FaxprotocolBuilder

        return FaxprotocolBuilder(self._request_adapter)

    @property
    def fqdn(self) -> FqdnBuilder:
        """
        The fqdn property
        """
        from .fqdn.fqdn_builder import FqdnBuilder

        return FqdnBuilder(self._request_adapter)

    @property
    def geolocation(self) -> GeolocationBuilder:
        """
        The geolocation property
        """
        from .geolocation.geolocation_builder import GeolocationBuilder

        return GeolocationBuilder(self._request_adapter)

    @property
    def identity(self) -> IdentityBuilder:
        """
        The identity property
        """
        from .identity.identity_builder import IdentityBuilder

        return IdentityBuilder(self._request_adapter)

    @property
    def ipprefixall(self) -> IpprefixallBuilder:
        """
        The ipprefixall property
        """
        from .ipprefixall.ipprefixall_builder import IpprefixallBuilder

        return IpprefixallBuilder(self._request_adapter)

    @property
    def ipssignature(self) -> IpssignatureBuilder:
        """
        The ipssignature property
        """
        from .ipssignature.ipssignature_builder import IpssignatureBuilder

        return IpssignatureBuilder(self._request_adapter)

    @property
    def ipv6prefix(self) -> Ipv6PrefixBuilder:
        """
        The ipv6prefix property
        """
        from .ipv6prefix.ipv6_prefix_builder import Ipv6PrefixBuilder

        return Ipv6PrefixBuilder(self._request_adapter)

    @property
    def localapp(self) -> LocalappBuilder:
        """
        The localapp property
        """
        from .localapp.localapp_builder import LocalappBuilder

        return LocalappBuilder(self._request_adapter)

    @property
    def localdomain(self) -> LocaldomainBuilder:
        """
        The localdomain property
        """
        from .localdomain.localdomain_builder import LocaldomainBuilder

        return LocaldomainBuilder(self._request_adapter)

    @property
    def mediaprofile(self) -> MediaprofileBuilder:
        """
        The mediaprofile property
        """
        from .mediaprofile.mediaprofile_builder import MediaprofileBuilder

        return MediaprofileBuilder(self._request_adapter)

    @property
    def mirror(self) -> MirrorBuilder:
        """
        The mirror property
        """
        from .mirror.mirror_builder import MirrorBuilder

        return MirrorBuilder(self._request_adapter)

    @property
    def modempassthrough(self) -> ModempassthroughBuilder:
        """
        The modempassthrough property
        """
        from .modempassthrough.modempassthrough_builder import ModempassthroughBuilder

        return ModempassthroughBuilder(self._request_adapter)

    @property
    def policer(self) -> PolicerBuilder:
        """
        The policer property
        """
        from .policer.policer_builder import PolicerBuilder

        return PolicerBuilder(self._request_adapter)

    @property
    def port(self) -> PortBuilder:
        """
        The port property
        """
        from .port.port_builder import PortBuilder

        return PortBuilder(self._request_adapter)

    @property
    def preferredcolorgroup(self) -> PreferredcolorgroupBuilder:
        """
        The preferredcolorgroup property
        """
        from .preferredcolorgroup.preferredcolorgroup_builder import PreferredcolorgroupBuilder

        return PreferredcolorgroupBuilder(self._request_adapter)

    @property
    def prefix(self) -> PrefixBuilder:
        """
        The prefix property
        """
        from .prefix.prefix_builder import PrefixBuilder

        return PrefixBuilder(self._request_adapter)

    @property
    def protocolname(self) -> ProtocolnameBuilder:
        """
        The protocolname property
        """
        from .protocolname.protocolname_builder import ProtocolnameBuilder

        return ProtocolnameBuilder(self._request_adapter)

    @property
    def region(self) -> RegionBuilder:
        """
        The region property
        """
        from .region.region_builder import RegionBuilder

        return RegionBuilder(self._request_adapter)

    @property
    def scalablegrouptag(self) -> ScalablegrouptagBuilder:
        """
        The scalablegrouptag property
        """
        from .scalablegrouptag.scalablegrouptag_builder import ScalablegrouptagBuilder

        return ScalablegrouptagBuilder(self._request_adapter)

    @property
    def site(self) -> SiteBuilder:
        """
        The site property
        """
        from .site.site_builder import SiteBuilder

        return SiteBuilder(self._request_adapter)

    @property
    def sla(self) -> SlaBuilder:
        """
        The sla property
        """
        from .sla.sla_builder import SlaBuilder

        return SlaBuilder(self._request_adapter)

    @property
    def supervisorydisc(self) -> SupervisorydiscBuilder:
        """
        The supervisorydisc property
        """
        from .supervisorydisc.supervisorydisc_builder import SupervisorydiscBuilder

        return SupervisorydiscBuilder(self._request_adapter)

    @property
    def tgapikey(self) -> TgapikeyBuilder:
        """
        The tgapikey property
        """
        from .tgapikey.tgapikey_builder import TgapikeyBuilder

        return TgapikeyBuilder(self._request_adapter)

    @property
    def tloc(self) -> TlocBuilder:
        """
        The tloc property
        """
        from .tloc.tloc_builder import TlocBuilder

        return TlocBuilder(self._request_adapter)

    @property
    def translationprofile(self) -> TranslationprofileBuilder:
        """
        The translationprofile property
        """
        from .translationprofile.translationprofile_builder import TranslationprofileBuilder

        return TranslationprofileBuilder(self._request_adapter)

    @property
    def translationrules(self) -> TranslationrulesBuilder:
        """
        The translationrules property
        """
        from .translationrules.translationrules_builder import TranslationrulesBuilder

        return TranslationrulesBuilder(self._request_adapter)

    @property
    def trunkgroup(self) -> TrunkgroupBuilder:
        """
        The trunkgroup property
        """
        from .trunkgroup.trunkgroup_builder import TrunkgroupBuilder

        return TrunkgroupBuilder(self._request_adapter)

    @property
    def umbrelladata(self) -> UmbrelladataBuilder:
        """
        The umbrelladata property
        """
        from .umbrelladata.umbrelladata_builder import UmbrelladataBuilder

        return UmbrelladataBuilder(self._request_adapter)

    @property
    def urlblacklist(self) -> UrlblacklistBuilder:
        """
        The urlblacklist property
        """
        from .urlblacklist.urlblacklist_builder import UrlblacklistBuilder

        return UrlblacklistBuilder(self._request_adapter)

    @property
    def urlwhitelist(self) -> UrlwhitelistBuilder:
        """
        The urlwhitelist property
        """
        from .urlwhitelist.urlwhitelist_builder import UrlwhitelistBuilder

        return UrlwhitelistBuilder(self._request_adapter)

    @property
    def vpn(self) -> VpnBuilder:
        """
        The vpn property
        """
        from .vpn.vpn_builder import VpnBuilder

        return VpnBuilder(self._request_adapter)

    @property
    def webex(self) -> WebexBuilder:
        """
        The webex property
        """
        from .webex.webex_builder import WebexBuilder

        return WebexBuilder(self._request_adapter)

    @property
    def zone(self) -> ZoneBuilder:
        """
        The zone property
        """
        from .zone.zone_builder import ZoneBuilder

        return ZoneBuilder(self._request_adapter)
