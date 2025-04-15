# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import QoSRespWithPageInfo, SortOrderParam

if TYPE_CHECKING:
    from .aggregation.aggregation_builder import AggregationBuilder
    from .app_agg.app_agg_builder import AppAggBuilder
    from .csv.csv_builder import CsvBuilder
    from .doccount.doccount_builder import DoccountBuilder
    from .fields.fields_builder import FieldsBuilder
    from .page.page_builder import PageBuilder
    from .query.query_builder import QueryBuilder


class QosBuilder:
    """
    Builds and executes requests for operations under /statistics/qos
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        query: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort_by: Optional[str] = None,
        sort_order: Optional[SortOrderParam] = None,
        **kw,
    ) -> List[QoSRespWithPageInfo]:
        """
        Get stats raw data
        GET /dataservice/statistics/qos

        :param query: Query
        :param page: Page
        :param page_size: Page size
        :param sort_by: Sort by
        :param sort_order: Sort order
        :returns: List[QoSRespWithPageInfo]
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
            "/dataservice/statistics/qos",
            return_type=List[QoSRespWithPageInfo],
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
    ) -> List[QoSRespWithPageInfo]:
        """
        Get stats raw data
        POST /dataservice/statistics/qos

        :param page: Page
        :param page_size: Page size
        :param sort_by: Sort by
        :param sort_order: Sort order
        :param payload: Stats query string
        :returns: List[QoSRespWithPageInfo]
        """
        params = {
            "page": page,
            "pageSize": page_size,
            "sortBy": sort_by,
            "sortOrder": sort_order,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/statistics/qos",
            return_type=List[QoSRespWithPageInfo],
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
