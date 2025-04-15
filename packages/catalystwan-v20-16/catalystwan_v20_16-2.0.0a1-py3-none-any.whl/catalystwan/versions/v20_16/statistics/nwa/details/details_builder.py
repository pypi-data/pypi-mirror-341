# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import NetworkAvailabilityResp


class DetailsBuilder:
    """
    Builds and executes requests for operations under /statistics/nwa/details
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, payload: Any, include_prev: Optional[bool] = False, **kw
    ) -> List[NetworkAvailabilityResp]:
        """
        Get network availability aggregated data with details based on input query and filters.
        POST /dataservice/statistics/nwa/details

        :param include_prev: Include prev
        :param payload: Stats query string
        :returns: List[NetworkAvailabilityResp]
        """
        params = {
            "includePrev": include_prev,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/statistics/nwa/details",
            return_type=List[NetworkAvailabilityResp],
            params=params,
            payload=payload,
            **kw,
        )
