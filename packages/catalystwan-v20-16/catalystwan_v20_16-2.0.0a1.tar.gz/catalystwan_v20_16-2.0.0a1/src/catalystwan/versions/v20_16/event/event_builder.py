# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .aggregation.aggregation_builder import AggregationBuilder
    from .byuuids.byuuids_builder import ByuuidsBuilder
    from .component.component_builder import ComponentBuilder
    from .doccount.doccount_builder import DoccountBuilder
    from .enable.enable_builder import EnableBuilder
    from .get_events_by_component.get_events_by_component_builder import GetEventsByComponentBuilder
    from .listeners.listeners_builder import ListenersBuilder
    from .page.page_builder import PageBuilder
    from .query.query_builder import QueryBuilder
    from .severity.severity_builder import SeverityBuilder
    from .types.types_builder import TypesBuilder


class EventBuilder:
    """
    Builds and executes requests for operations under /event
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        query: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = None,
        site_id: Optional[str] = None,
        include_tenants: Optional[bool] = None,
        **kw,
    ) -> Any:
        """
        Get events for given query. If query is empty then last 30 mins data will be returned.
        GET /dataservice/event

        :param query: Query
        :param page: Specify page number. Value should be a positive integer
        :param page_size: Specify page size. Value should be a positive integer
        :param sort_by: Specify a field by which alarms need to be sorted
        :param sort_order: Select sorting order. Use ASC for ascending and DESC for descending
        :param site_id: Specify the site-id to filter the events
        :param include_tenants: Include tenants
        :returns: Any
        """
        params = {
            "query": query,
            "page": page,
            "pageSize": page_size,
            "sortBy": sort_by,
            "sortOrder": sort_order,
            "site-id": site_id,
            "includeTenants": include_tenants,
        }
        return self._request_adapter.request("GET", "/dataservice/event", params=params, **kw)

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
    ) -> Any:
        """
        Get events for given query.
        POST /dataservice/event

        :param page: Specify page number. Value should be a positive integer
        :param page_size: Specify page size. Value should be a positive integer
        :param sort_by: Specify a field by which alarms need to be sorted
        :param sort_order: Select sorting order. Use ASC for ascending and DESC for descending
        :param site_id: Specify the site-id to filter the events
        :param include_tenants: Include tenants
        :param payload: Event query string
        :returns: Any
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
            "POST", "/dataservice/event", params=params, payload=payload, **kw
        )

    @property
    def aggregation(self) -> AggregationBuilder:
        """
        The aggregation property
        """
        from .aggregation.aggregation_builder import AggregationBuilder

        return AggregationBuilder(self._request_adapter)

    @property
    def byuuids(self) -> ByuuidsBuilder:
        """
        The byuuids property
        """
        from .byuuids.byuuids_builder import ByuuidsBuilder

        return ByuuidsBuilder(self._request_adapter)

    @property
    def component(self) -> ComponentBuilder:
        """
        The component property
        """
        from .component.component_builder import ComponentBuilder

        return ComponentBuilder(self._request_adapter)

    @property
    def doccount(self) -> DoccountBuilder:
        """
        The doccount property
        """
        from .doccount.doccount_builder import DoccountBuilder

        return DoccountBuilder(self._request_adapter)

    @property
    def enable(self) -> EnableBuilder:
        """
        The enable property
        """
        from .enable.enable_builder import EnableBuilder

        return EnableBuilder(self._request_adapter)

    @property
    def get_events_by_component(self) -> GetEventsByComponentBuilder:
        """
        The getEventsByComponent property
        """
        from .get_events_by_component.get_events_by_component_builder import (
            GetEventsByComponentBuilder,
        )

        return GetEventsByComponentBuilder(self._request_adapter)

    @property
    def listeners(self) -> ListenersBuilder:
        """
        The listeners property
        """
        from .listeners.listeners_builder import ListenersBuilder

        return ListenersBuilder(self._request_adapter)

    @property
    def page(self) -> PageBuilder:
        """
        The page property
        """
        from .page.page_builder import PageBuilder

        return PageBuilder(self._request_adapter)

    @property
    def query(self) -> QueryBuilder:
        """
        The query property
        """
        from .query.query_builder import QueryBuilder

        return QueryBuilder(self._request_adapter)

    @property
    def severity(self) -> SeverityBuilder:
        """
        The severity property
        """
        from .severity.severity_builder import SeverityBuilder

        return SeverityBuilder(self._request_adapter)

    @property
    def types(self) -> TypesBuilder:
        """
        The types property
        """
        from .types.types_builder import TypesBuilder

        return TypesBuilder(self._request_adapter)
