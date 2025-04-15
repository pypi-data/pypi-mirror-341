# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import InlineResponse2001


class AggregationBuilder:
    """
    Builds and executes requests for operations under /multicloud/statistics/interface/aggregation
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw) -> InlineResponse2001:
        """
        Get aggregated data based on input query and filter. The data can be filtered on time and other unique parameters based upon necessity and intended usage
        POST /dataservice/multicloud/statistics/interface/aggregation

        :param payload: Stats query string
        :returns: InlineResponse2001
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/multicloud/statistics/interface/aggregation",
            return_type=InlineResponse2001,
            payload=payload,
            **kw,
        )
