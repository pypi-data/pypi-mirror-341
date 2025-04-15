# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import NetworkAvailabilityResp

if TYPE_CHECKING:
    from .aggregation.aggregation_builder import AggregationBuilder
    from .details.details_builder import DetailsBuilder


class NwaBuilder:
    """
    Builds and executes requests for operations under /statistics/nwa
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        query: str,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = None,
        **kw,
    ) -> List[NetworkAvailabilityResp]:
        """
        Get network availability raw data based on input query and filters.
        POST /dataservice/statistics/nwa

        :param query: Query
        :param page: Page
        :param page_size: Page size
        :param sort_by: Sort by
        :param sort_order: Sort order
        :returns: List[NetworkAvailabilityResp]
        """
        params = {
            "query": query,
            "page": page,
            "pageSize": page_size,
            "sortBy": sort_by,
            "sortOrder": sort_order,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/statistics/nwa",
            return_type=List[NetworkAvailabilityResp],
            params=params,
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
    def details(self) -> DetailsBuilder:
        """
        The details property
        """
        from .details.details_builder import DetailsBuilder

        return DetailsBuilder(self._request_adapter)
