# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import InterfaceQuery, InterfaceRespWithPageInfo, SortOrderParam

if TYPE_CHECKING:
    from .aggregation.aggregation_builder import AggregationBuilder
    from .app_agg.app_agg_builder import AppAggBuilder
    from .ccapacity.ccapacity_builder import CcapacityBuilder
    from .csv.csv_builder import CsvBuilder
    from .doccount.doccount_builder import DoccountBuilder
    from .fields.fields_builder import FieldsBuilder
    from .page.page_builder import PageBuilder
    from .query.query_builder import QueryBuilder
    from .type_.type_builder import TypeBuilder


class InterfaceBuilder:
    """
    Builds and executes requests for operations under /statistics/interface
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        query: str,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort_by: Optional[str] = None,
        sort_order: Optional[SortOrderParam] = None,
        **kw,
    ) -> InterfaceQuery:
        """
        Get stats raw data
        GET /dataservice/statistics/interface

        :param query: Query
        :param page: Page
        :param page_size: Page size
        :param sort_by: Sort by
        :param sort_order: Sort order
        :returns: InterfaceQuery
        """
        params = {
            "query": query,
            "page": page,
            "pageSize": page_size,
            "sortBy": sort_by,
            "sortOrder": sort_order,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/statistics/interface",
            return_type=InterfaceQuery,
            params=params,
            **kw,
        )

    def post(
        self,
        payload: Any,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort_by: Optional[str] = None,
        sort_order: Optional[SortOrderParam] = None,
        **kw,
    ) -> List[InterfaceRespWithPageInfo]:
        """
        Get stats raw data
        POST /dataservice/statistics/interface

        :param page: Page
        :param page_size: Page size
        :param sort_by: Sort by
        :param sort_order: Sort order
        :param payload: Query filter
        :returns: List[InterfaceRespWithPageInfo]
        """
        params = {
            "page": page,
            "pageSize": page_size,
            "sortBy": sort_by,
            "sortOrder": sort_order,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/statistics/interface",
            return_type=List[InterfaceRespWithPageInfo],
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
    def app_agg(self) -> AppAggBuilder:
        """
        The app-agg property
        """
        from .app_agg.app_agg_builder import AppAggBuilder

        return AppAggBuilder(self._request_adapter)

    @property
    def ccapacity(self) -> CcapacityBuilder:
        """
        The ccapacity property
        """
        from .ccapacity.ccapacity_builder import CcapacityBuilder

        return CcapacityBuilder(self._request_adapter)

    @property
    def csv(self) -> CsvBuilder:
        """
        The csv property
        """
        from .csv.csv_builder import CsvBuilder

        return CsvBuilder(self._request_adapter)

    @property
    def doccount(self) -> DoccountBuilder:
        """
        The doccount property
        """
        from .doccount.doccount_builder import DoccountBuilder

        return DoccountBuilder(self._request_adapter)

    @property
    def fields(self) -> FieldsBuilder:
        """
        The fields property
        """
        from .fields.fields_builder import FieldsBuilder

        return FieldsBuilder(self._request_adapter)

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
    def type_(self) -> TypeBuilder:
        """
        The type property
        """
        from .type_.type_builder import TypeBuilder

        return TypeBuilder(self._request_adapter)
