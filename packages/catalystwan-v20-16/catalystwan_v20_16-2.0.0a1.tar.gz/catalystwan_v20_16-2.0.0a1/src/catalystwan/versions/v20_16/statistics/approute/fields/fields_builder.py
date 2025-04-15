# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import AppRouteDocCountResponse


class FieldsBuilder:
    """
    Builds and executes requests for operations under /statistics/approute/fields
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[AppRouteDocCountResponse]:
        """
        Get fields and type
        GET /dataservice/statistics/approute/fields

        :returns: List[AppRouteDocCountResponse]
        """
        return self._request_adapter.request(
            "GET",
            "/dataservice/statistics/approute/fields",
            return_type=List[AppRouteDocCountResponse],
            **kw,
        )
