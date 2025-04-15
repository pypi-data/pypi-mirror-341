# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import RoutingDetailResponsePayloadInner


class RoutingDetailBuilder:
    """
    Builds and executes requests for operations under /stream/device/nwpi/routingDetail
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self, trace_id: int, timestamp: int, trace_state: str, route_prefixs: str, **kw
    ) -> List[RoutingDetailResponsePayloadInner]:
        """
        Get Routing Details for NWPI.
        GET /dataservice/stream/device/nwpi/routingDetail

        :param trace_id: Trace id
        :param timestamp: Timestamp
        :param trace_state: Trace state
        :param route_prefixs: Route prefixs
        :returns: List[RoutingDetailResponsePayloadInner]
        """
        logging.warning("Operation: %s is deprecated", "getRoutingDetailFromLocal")
        params = {
            "traceId": trace_id,
            "timestamp": timestamp,
            "traceState": trace_state,
            "routePrefixs": route_prefixs,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/stream/device/nwpi/routingDetail",
            return_type=List[RoutingDetailResponsePayloadInner],
            params=params,
            **kw,
        )
