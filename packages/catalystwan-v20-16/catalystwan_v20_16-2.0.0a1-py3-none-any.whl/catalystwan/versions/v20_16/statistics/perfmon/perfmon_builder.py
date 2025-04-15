# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .aggregation.aggregation_builder import AggregationBuilder
    from .application.application_builder import ApplicationBuilder
    from .applications.applications_builder import ApplicationsBuilder


class PerfmonBuilder:
    """
    Builds and executes requests for operations under /statistics/perfmon
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def aggregation(self) -> AggregationBuilder:
        """
        The aggregation property
        """
        from .aggregation.aggregation_builder import AggregationBuilder

        return AggregationBuilder(self._request_adapter)

    @property
    def application(self) -> ApplicationBuilder:
        """
        The application property
        """
        from .application.application_builder import ApplicationBuilder

        return ApplicationBuilder(self._request_adapter)

    @property
    def applications(self) -> ApplicationsBuilder:
        """
        The applications property
        """
        from .applications.applications_builder import ApplicationsBuilder

        return ApplicationsBuilder(self._request_adapter)
