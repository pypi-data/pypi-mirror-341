# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import MapVpnsResponse


class VpnsBuilder:
    """
    Builds and executes requests for operations under /multicloud/map/vpns
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> MapVpnsResponse:
        """
        Get default mapping values
        GET /dataservice/multicloud/map/vpns

        :returns: MapVpnsResponse
        """
        return self._request_adapter.request(
            "GET", "/dataservice/multicloud/map/vpns", return_type=MapVpnsResponse, **kw
        )
