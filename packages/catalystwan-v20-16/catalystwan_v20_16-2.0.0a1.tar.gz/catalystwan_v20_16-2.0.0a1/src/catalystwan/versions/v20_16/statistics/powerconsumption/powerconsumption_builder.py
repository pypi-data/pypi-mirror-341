# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import PowerConsumptionResp, SortOrderParam

if TYPE_CHECKING:
    from .aggregation.aggregation_builder import AggregationBuilder
    from .device.device_builder import DeviceBuilder
    from .energymix.energymix_builder import EnergymixBuilder
    from .supportdevicelist.supportdevicelist_builder import SupportdevicelistBuilder
    from .total.total_builder import TotalBuilder


class PowerconsumptionBuilder:
    """
    Builds and executes requests for operations under /statistics/powerconsumption
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        payload: Any,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort_by: Optional[str] = None,
        sort_order: Optional[SortOrderParam] = None,
        **kw,
    ) -> List[PowerConsumptionResp]:
        """
        Get aggregated data based on input query and filters. The data can be filtered on time and other unique parameters based upon necessity and intended usage
        POST /dataservice/statistics/powerconsumption

        :param page: Page
        :param page_size: Page size
        :param sort_by: Sort by
        :param sort_order: Sort order
        :param payload: Stats query string
        :returns: List[PowerConsumptionResp]
        """
        params = {
            "page": page,
            "pageSize": page_size,
            "sortBy": sort_by,
            "sortOrder": sort_order,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/statistics/powerconsumption",
            return_type=List[PowerConsumptionResp],
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
    def device(self) -> DeviceBuilder:
        """
        The device property
        """
        from .device.device_builder import DeviceBuilder

        return DeviceBuilder(self._request_adapter)

    @property
    def energymix(self) -> EnergymixBuilder:
        """
        The energymix property
        """
        from .energymix.energymix_builder import EnergymixBuilder

        return EnergymixBuilder(self._request_adapter)

    @property
    def supportdevicelist(self) -> SupportdevicelistBuilder:
        """
        The supportdevicelist property
        """
        from .supportdevicelist.supportdevicelist_builder import SupportdevicelistBuilder

        return SupportdevicelistBuilder(self._request_adapter)

    @property
    def total(self) -> TotalBuilder:
        """
        The total property
        """
        from .total.total_builder import TotalBuilder

        return TotalBuilder(self._request_adapter)
