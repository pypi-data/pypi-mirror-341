# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import NwpiflowDetailRespPayloadInner


class FlowDetailBuilder:
    """
    Builds and executes requests for operations under /stream/device/nwpi/flowDetail
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self, trace_id: int, timestamp: int, flow_id: int, **kw
    ) -> List[NwpiflowDetailRespPayloadInner]:
        """
        flowDetail for NWPI.
        GET /dataservice/stream/device/nwpi/flowDetail

        :param trace_id: trace id
        :param timestamp: start time
        :param flow_id: flow id
        :returns: List[NwpiflowDetailRespPayloadInner]
        """
        logging.warning("Operation: %s is deprecated", "getFlowDetail")
        params = {
            "traceId": trace_id,
            "timestamp": timestamp,
            "flowId": flow_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/stream/device/nwpi/flowDetail",
            return_type=List[NwpiflowDetailRespPayloadInner],
            params=params,
            **kw,
        )
