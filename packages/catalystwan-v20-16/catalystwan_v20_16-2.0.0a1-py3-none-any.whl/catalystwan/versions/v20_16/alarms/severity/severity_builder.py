# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import AlarmResponse

if TYPE_CHECKING:
    from .summary.summary_builder import SummaryBuilder


class SeverityBuilder:
    """
    Builds and executes requests for operations under /alarms/severity
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        severity_level: List[str],
        device_id: Optional[List[str]] = None,
        query: Optional[str] = None,
        site_id: Optional[str] = None,
        **kw,
    ) -> AlarmResponse:
        """
        Get alarms by severity
        GET /dataservice/alarms/severity

        :param severity_level: Severity level
        :param device_id: Device System IP
        :param query: Query
        :param site_id: Specify the site-id to filter the alarms
        :returns: AlarmResponse
        """
        params = {
            "severity-level": severity_level,
            "deviceId": device_id,
            "query": query,
            "site-id": site_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/alarms/severity", return_type=AlarmResponse, params=params, **kw
        )

    @property
    def summary(self) -> SummaryBuilder:
        """
        The summary property
        """
        from .summary.summary_builder import SummaryBuilder

        return SummaryBuilder(self._request_adapter)
