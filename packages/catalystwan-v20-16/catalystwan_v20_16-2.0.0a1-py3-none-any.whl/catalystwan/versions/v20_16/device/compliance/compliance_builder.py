# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DeviceComplianceApiResponse, OrderByParam

if TYPE_CHECKING:
    from .summary.summary_builder import SummaryBuilder


class ComplianceBuilder:
    """
    Builds and executes requests for operations under /device/compliance
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        offset: Optional[int] = 0,
        limit: Optional[int] = 25,
        device_type: Optional[List[str]] = None,
        status: Optional[List[str]] = None,
        type_: Optional[List[str]] = None,
        sort_by: Optional[str] = None,
        order_by: Optional[OrderByParam] = None,
        **kw,
    ) -> DeviceComplianceApiResponse:
        """
        Get compliance information for devices
        GET /dataservice/device/compliance

        :param offset: Offset
        :param limit: Limit
        :param device_type: deviceType example: vedge
        :param status: Status
        :param type_: Type
        :param sort_by: Sort by
        :param order_by: Order by
        :returns: DeviceComplianceApiResponse
        """
        params = {
            "offset": offset,
            "limit": limit,
            "deviceType": device_type,
            "status": status,
            "type": type_,
            "sort_by": sort_by,
            "order_by": order_by,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/device/compliance",
            return_type=DeviceComplianceApiResponse,
            params=params,
            **kw,
        )

    @property
    def summary(self) -> SummaryBuilder:
        """
        The summary property
        """
        from .summary.summary_builder import SummaryBuilder

        return SummaryBuilder(self._request_adapter)
