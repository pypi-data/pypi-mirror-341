# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .accesslistassociations.accesslistassociations_builder import AccesslistassociationsBuilder
    from .accesslistcounters.accesslistcounters_builder import AccesslistcountersBuilder
    from .accesslistnames.accesslistnames_builder import AccesslistnamesBuilder
    from .accesslistpolicers.accesslistpolicers_builder import AccesslistpolicersBuilder
    from .approutepolicyfilter.approutepolicyfilter_builder import ApproutepolicyfilterBuilder
    from .datapolicyfilter.datapolicyfilter_builder import DatapolicyfilterBuilder
    from .filtermemoryusage.filtermemoryusage_builder import FiltermemoryusageBuilder
    from .iptosgtbindings.iptosgtbindings_builder import IptosgtbindingsBuilder
    from .iptouserbindings.iptouserbindings_builder import IptouserbindingsBuilder
    from .ipv6.ipv6_builder import Ipv6Builder
    from .pxgridstatus.pxgridstatus_builder import PxgridstatusBuilder
    from .pxgridusersessions.pxgridusersessions_builder import PxgridusersessionsBuilder
    from .qosmapinfo.qosmapinfo_builder import QosmapinfoBuilder
    from .qosschedulerinfo.qosschedulerinfo_builder import QosschedulerinfoBuilder
    from .rewriteassociations.rewriteassociations_builder import RewriteassociationsBuilder
    from .userusergroupbindings.userusergroupbindings_builder import UserusergroupbindingsBuilder
    from .vsmart.vsmart_builder import VsmartBuilder
    from .zbfwdropstatistics.zbfwdropstatistics_builder import ZbfwdropstatisticsBuilder
    from .zbfwstatistics.zbfwstatistics_builder import ZbfwstatisticsBuilder
    from .zonepairsessions.zonepairsessions_builder import ZonepairsessionsBuilder
    from .zonepairstatistics.zonepairstatistics_builder import ZonepairstatisticsBuilder
    from .zonepolicyfilter.zonepolicyfilter_builder import ZonepolicyfilterBuilder


class PolicyBuilder:
    """
    Builds and executes requests for operations under /device/policy
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def accesslistassociations(self) -> AccesslistassociationsBuilder:
        """
        The accesslistassociations property
        """
        from .accesslistassociations.accesslistassociations_builder import (
            AccesslistassociationsBuilder,
        )

        return AccesslistassociationsBuilder(self._request_adapter)

    @property
    def accesslistcounters(self) -> AccesslistcountersBuilder:
        """
        The accesslistcounters property
        """
        from .accesslistcounters.accesslistcounters_builder import AccesslistcountersBuilder

        return AccesslistcountersBuilder(self._request_adapter)

    @property
    def accesslistnames(self) -> AccesslistnamesBuilder:
        """
        The accesslistnames property
        """
        from .accesslistnames.accesslistnames_builder import AccesslistnamesBuilder

        return AccesslistnamesBuilder(self._request_adapter)

    @property
    def accesslistpolicers(self) -> AccesslistpolicersBuilder:
        """
        The accesslistpolicers property
        """
        from .accesslistpolicers.accesslistpolicers_builder import AccesslistpolicersBuilder

        return AccesslistpolicersBuilder(self._request_adapter)

    @property
    def approutepolicyfilter(self) -> ApproutepolicyfilterBuilder:
        """
        The approutepolicyfilter property
        """
        from .approutepolicyfilter.approutepolicyfilter_builder import ApproutepolicyfilterBuilder

        return ApproutepolicyfilterBuilder(self._request_adapter)

    @property
    def datapolicyfilter(self) -> DatapolicyfilterBuilder:
        """
        The datapolicyfilter property
        """
        from .datapolicyfilter.datapolicyfilter_builder import DatapolicyfilterBuilder

        return DatapolicyfilterBuilder(self._request_adapter)

    @property
    def filtermemoryusage(self) -> FiltermemoryusageBuilder:
        """
        The filtermemoryusage property
        """
        from .filtermemoryusage.filtermemoryusage_builder import FiltermemoryusageBuilder

        return FiltermemoryusageBuilder(self._request_adapter)

    @property
    def iptosgtbindings(self) -> IptosgtbindingsBuilder:
        """
        The iptosgtbindings property
        """
        from .iptosgtbindings.iptosgtbindings_builder import IptosgtbindingsBuilder

        return IptosgtbindingsBuilder(self._request_adapter)

    @property
    def iptouserbindings(self) -> IptouserbindingsBuilder:
        """
        The iptouserbindings property
        """
        from .iptouserbindings.iptouserbindings_builder import IptouserbindingsBuilder

        return IptouserbindingsBuilder(self._request_adapter)

    @property
    def ipv6(self) -> Ipv6Builder:
        """
        The ipv6 property
        """
        from .ipv6.ipv6_builder import Ipv6Builder

        return Ipv6Builder(self._request_adapter)

    @property
    def pxgridstatus(self) -> PxgridstatusBuilder:
        """
        The pxgridstatus property
        """
        from .pxgridstatus.pxgridstatus_builder import PxgridstatusBuilder

        return PxgridstatusBuilder(self._request_adapter)

    @property
    def pxgridusersessions(self) -> PxgridusersessionsBuilder:
        """
        The pxgridusersessions property
        """
        from .pxgridusersessions.pxgridusersessions_builder import PxgridusersessionsBuilder

        return PxgridusersessionsBuilder(self._request_adapter)

    @property
    def qosmapinfo(self) -> QosmapinfoBuilder:
        """
        The qosmapinfo property
        """
        from .qosmapinfo.qosmapinfo_builder import QosmapinfoBuilder

        return QosmapinfoBuilder(self._request_adapter)

    @property
    def qosschedulerinfo(self) -> QosschedulerinfoBuilder:
        """
        The qosschedulerinfo property
        """
        from .qosschedulerinfo.qosschedulerinfo_builder import QosschedulerinfoBuilder

        return QosschedulerinfoBuilder(self._request_adapter)

    @property
    def rewriteassociations(self) -> RewriteassociationsBuilder:
        """
        The rewriteassociations property
        """
        from .rewriteassociations.rewriteassociations_builder import RewriteassociationsBuilder

        return RewriteassociationsBuilder(self._request_adapter)

    @property
    def userusergroupbindings(self) -> UserusergroupbindingsBuilder:
        """
        The userusergroupbindings property
        """
        from .userusergroupbindings.userusergroupbindings_builder import (
            UserusergroupbindingsBuilder,
        )

        return UserusergroupbindingsBuilder(self._request_adapter)

    @property
    def vsmart(self) -> VsmartBuilder:
        """
        The vsmart property
        """
        from .vsmart.vsmart_builder import VsmartBuilder

        return VsmartBuilder(self._request_adapter)

    @property
    def zbfwdropstatistics(self) -> ZbfwdropstatisticsBuilder:
        """
        The zbfwdropstatistics property
        """
        from .zbfwdropstatistics.zbfwdropstatistics_builder import ZbfwdropstatisticsBuilder

        return ZbfwdropstatisticsBuilder(self._request_adapter)

    @property
    def zbfwstatistics(self) -> ZbfwstatisticsBuilder:
        """
        The zbfwstatistics property
        """
        from .zbfwstatistics.zbfwstatistics_builder import ZbfwstatisticsBuilder

        return ZbfwstatisticsBuilder(self._request_adapter)

    @property
    def zonepairsessions(self) -> ZonepairsessionsBuilder:
        """
        The zonepairsessions property
        """
        from .zonepairsessions.zonepairsessions_builder import ZonepairsessionsBuilder

        return ZonepairsessionsBuilder(self._request_adapter)

    @property
    def zonepairstatistics(self) -> ZonepairstatisticsBuilder:
        """
        The zonepairstatistics property
        """
        from .zonepairstatistics.zonepairstatistics_builder import ZonepairstatisticsBuilder

        return ZonepairstatisticsBuilder(self._request_adapter)

    @property
    def zonepolicyfilter(self) -> ZonepolicyfilterBuilder:
        """
        The zonepolicyfilter property
        """
        from .zonepolicyfilter.zonepolicyfilter_builder import ZonepolicyfilterBuilder

        return ZonepolicyfilterBuilder(self._request_adapter)
