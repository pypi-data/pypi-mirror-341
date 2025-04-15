# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import ActiveFlowResponsePayload


class ActiveFlowWithQueryBuilder:
    """
    Builds and executes requests for operations under /stream/device/nwpi/activeFlowWithQuery
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self, trace_id: int, timestamp: int, query: Optional[str] = None, **kw
    ) -> ActiveFlowResponsePayload:
        """
        Get active flows for NWPI.
        GET /dataservice/stream/device/nwpi/activeFlowWithQuery

        :param trace_id: trace id
        :param timestamp: start time
        :param query: Query filter
        :returns: ActiveFlowResponsePayload
        """
        logging.warning("Operation: %s is deprecated", "activeFlowWithQuery")
        params = {
            "traceId": trace_id,
            "timestamp": timestamp,
            "query": query,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/stream/device/nwpi/activeFlowWithQuery",
            return_type=ActiveFlowResponsePayload,
            params=params,
            **kw,
        )
