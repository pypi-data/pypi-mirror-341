# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import InterfaceStatisticsRes

if TYPE_CHECKING:
    from .doccount.doccount_builder import DoccountBuilder
    from .fields.fields_builder import FieldsBuilder


class InterfacestatisticsBuilder:
    """
    Builds and executes requests for operations under /v2/data/device/statistics/interfacestatistics
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        scroll_id: Optional[str] = None,
        count: Optional[int] = None,
        time_zone: Optional[str] = None,
        **kw,
    ) -> List[InterfaceStatisticsRes]:
        """
        Get device statistics data
        GET /dataservice/v2/data/device/statistics/interfacestatistics

        :param start_date: Start date (example:2023-1-1T00:00:00)
        :param end_date: End date (example:2023-1-1T00:00:00)
        :param scroll_id: Scroll Id
        :param count: Count
        :param time_zone: Time zone
        :returns: List[InterfaceStatisticsRes]
        """
        params = {
            "startDate": start_date,
            "endDate": end_date,
            "scrollId": scroll_id,
            "count": count,
            "timeZone": time_zone,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/v2/data/device/statistics/interfacestatistics",
            return_type=List[InterfaceStatisticsRes],
            params=params,
            **kw,
        )

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
