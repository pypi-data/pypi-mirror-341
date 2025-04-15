# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import NwpitraceFlowRespPayload


class FinalizedDataBuilder:
    """
    Builds and executes requests for operations under /stream/device/nwpi/finalizedData
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, trace_id: int, timestamp: int, **kw) -> NwpitraceFlowRespPayload:
        """
        finalizedData for NWPI.
        GET /dataservice/stream/device/nwpi/finalizedData

        :param trace_id: trace id
        :param timestamp: start time
        :returns: NwpitraceFlowRespPayload
        """
        logging.warning("Operation: %s is deprecated", "getFinalizedData")
        params = {
            "traceId": trace_id,
            "timestamp": timestamp,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/stream/device/nwpi/finalizedData",
            return_type=NwpitraceFlowRespPayload,
            params=params,
            **kw,
        )
