# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import AlarmResponse

if TYPE_CHECKING:
    from .aggregation.aggregation_builder import AggregationBuilder
    from .clear.clear_builder import ClearBuilder
    from .count.count_builder import CountBuilder
    from .disabled.disabled_builder import DisabledBuilder
    from .doccount.doccount_builder import DoccountBuilder
    from .dump.dump_builder import DumpBuilder
    from .fields.fields_builder import FieldsBuilder
    from .link_state_alarm.link_state_alarm_builder import LinkStateAlarmBuilder
    from .markallasviewed.markallasviewed_builder import MarkallasviewedBuilder
    from .markviewed.markviewed_builder import MarkviewedBuilder
    from .master.master_builder import MasterBuilder
    from .notviewed.notviewed_builder import NotviewedBuilder
    from .page.page_builder import PageBuilder
    from .purgefrequency.purgefrequency_builder import PurgefrequencyBuilder
    from .query.query_builder import QueryBuilder
    from .reset.reset_builder import ResetBuilder
    from .restart.restart_builder import RestartBuilder
    from .rulenamedisplay.rulenamedisplay_builder import RulenamedisplayBuilder
    from .severity.severity_builder import SeverityBuilder
    from .severitymappings.severitymappings_builder import SeveritymappingsBuilder
    from .starttracking.starttracking_builder import StarttrackingBuilder
    from .stats.stats_builder import StatsBuilder
    from .stoptracking.stoptracking_builder import StoptrackingBuilder
    from .topic.topic_builder import TopicBuilder
    from .topn.topn_builder import TopnBuilder
    from .uuid.uuid_builder import UuidBuilder


class AlarmsBuilder:
    """
    Builds and executes requests for operations under /alarms
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        query: Optional[str] = None,
        site_id: Optional[str] = None,
        include_tenants: Optional[bool] = None,
        **kw,
    ) -> AlarmResponse:
        """
        Get alarms for given query. If query is empty then last 30 mins data will be returned.
        GET /dataservice/alarms

        :param query: Query
        :param site_id: Specify the site-id to filter the alarms
        :param include_tenants: Specify whether the tenant alarms need to be visible or not from provider view.
        :returns: AlarmResponse
        """
        params = {
            "query": query,
            "site-id": site_id,
            "includeTenants": include_tenants,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/alarms", return_type=AlarmResponse, params=params, **kw
        )

    def post(
        self,
        payload: Any,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = None,
        site_id: Optional[str] = None,
        include_tenants: Optional[bool] = None,
        **kw,
    ) -> AlarmResponse:
        """
        Get alarms for given query.
        POST /dataservice/alarms

        :param page: Specify page number. Value should be a positive integer
        :param page_size: Specify page size. Value should be a positive integer
        :param sort_by: Specify a field by which alarms need to be sorted
        :param sort_order: Select sorting order. Use ASC for ascending and DESC for descending
        :param site_id: Specify the site-id to filter the alarms
        :param include_tenants: Specify whether the tenant alarms need to be visible or not from provider view.
        :param payload: Alarm query string
        :returns: AlarmResponse
        """
        params = {
            "page": page,
            "pageSize": page_size,
            "sortBy": sort_by,
            "sortOrder": sort_order,
            "site-id": site_id,
            "includeTenants": include_tenants,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/alarms",
            return_type=AlarmResponse,
            params=params,
            payload=payload,
            **kw,
        )

    @property
    def aggregation(self) -> AggregationBuilder:
        """
        The aggregation property
        """
        from .aggregation.aggregation_builder import AggregationBuilder

        return AggregationBuilder(self._request_adapter)

    @property
    def clear(self) -> ClearBuilder:
        """
        The clear property
        """
        from .clear.clear_builder import ClearBuilder

        return ClearBuilder(self._request_adapter)

    @property
    def count(self) -> CountBuilder:
        """
        The count property
        """
        from .count.count_builder import CountBuilder

        return CountBuilder(self._request_adapter)

    @property
    def disabled(self) -> DisabledBuilder:
        """
        The disabled property
        """
        from .disabled.disabled_builder import DisabledBuilder

        return DisabledBuilder(self._request_adapter)

    @property
    def doccount(self) -> DoccountBuilder:
        """
        The doccount property
        """
        from .doccount.doccount_builder import DoccountBuilder

        return DoccountBuilder(self._request_adapter)

    @property
    def dump(self) -> DumpBuilder:
        """
        The dump property
        """
        from .dump.dump_builder import DumpBuilder

        return DumpBuilder(self._request_adapter)

    @property
    def fields(self) -> FieldsBuilder:
        """
        The fields property
        """
        from .fields.fields_builder import FieldsBuilder

        return FieldsBuilder(self._request_adapter)

    @property
    def link_state_alarm(self) -> LinkStateAlarmBuilder:
        """
        The link-state-alarm property
        """
        from .link_state_alarm.link_state_alarm_builder import LinkStateAlarmBuilder

        return LinkStateAlarmBuilder(self._request_adapter)

    @property
    def markallasviewed(self) -> MarkallasviewedBuilder:
        """
        The markallasviewed property
        """
        from .markallasviewed.markallasviewed_builder import MarkallasviewedBuilder

        return MarkallasviewedBuilder(self._request_adapter)

    @property
    def markviewed(self) -> MarkviewedBuilder:
        """
        The markviewed property
        """
        from .markviewed.markviewed_builder import MarkviewedBuilder

        return MarkviewedBuilder(self._request_adapter)

    @property
    def master(self) -> MasterBuilder:
        """
        The master property
        """
        from .master.master_builder import MasterBuilder

        return MasterBuilder(self._request_adapter)

    @property
    def notviewed(self) -> NotviewedBuilder:
        """
        The notviewed property
        """
        from .notviewed.notviewed_builder import NotviewedBuilder

        return NotviewedBuilder(self._request_adapter)

    @property
    def page(self) -> PageBuilder:
        """
        The page property
        """
        from .page.page_builder import PageBuilder

        return PageBuilder(self._request_adapter)

    @property
    def purgefrequency(self) -> PurgefrequencyBuilder:
        """
        The purgefrequency property
        """
        from .purgefrequency.purgefrequency_builder import PurgefrequencyBuilder

        return PurgefrequencyBuilder(self._request_adapter)

    @property
    def query(self) -> QueryBuilder:
        """
        The query property
        """
        from .query.query_builder import QueryBuilder

        return QueryBuilder(self._request_adapter)

    @property
    def reset(self) -> ResetBuilder:
        """
        The reset property
        """
        from .reset.reset_builder import ResetBuilder

        return ResetBuilder(self._request_adapter)

    @property
    def restart(self) -> RestartBuilder:
        """
        The restart property
        """
        from .restart.restart_builder import RestartBuilder

        return RestartBuilder(self._request_adapter)

    @property
    def rulenamedisplay(self) -> RulenamedisplayBuilder:
        """
        The rulenamedisplay property
        """
        from .rulenamedisplay.rulenamedisplay_builder import RulenamedisplayBuilder

        return RulenamedisplayBuilder(self._request_adapter)

    @property
    def severity(self) -> SeverityBuilder:
        """
        The severity property
        """
        from .severity.severity_builder import SeverityBuilder

        return SeverityBuilder(self._request_adapter)

    @property
    def severitymappings(self) -> SeveritymappingsBuilder:
        """
        The severitymappings property
        """
        from .severitymappings.severitymappings_builder import SeveritymappingsBuilder

        return SeveritymappingsBuilder(self._request_adapter)

    @property
    def starttracking(self) -> StarttrackingBuilder:
        """
        The starttracking property
        """
        from .starttracking.starttracking_builder import StarttrackingBuilder

        return StarttrackingBuilder(self._request_adapter)

    @property
    def stats(self) -> StatsBuilder:
        """
        The stats property
        """
        from .stats.stats_builder import StatsBuilder

        return StatsBuilder(self._request_adapter)

    @property
    def stoptracking(self) -> StoptrackingBuilder:
        """
        The stoptracking property
        """
        from .stoptracking.stoptracking_builder import StoptrackingBuilder

        return StoptrackingBuilder(self._request_adapter)

    @property
    def topic(self) -> TopicBuilder:
        """
        The topic property
        """
        from .topic.topic_builder import TopicBuilder

        return TopicBuilder(self._request_adapter)

    @property
    def topn(self) -> TopnBuilder:
        """
        The topn property
        """
        from .topn.topn_builder import TopnBuilder

        return TopnBuilder(self._request_adapter)

    @property
    def uuid(self) -> UuidBuilder:
        """
        The uuid property
        """
        from .uuid.uuid_builder import UuidBuilder

        return UuidBuilder(self._request_adapter)
