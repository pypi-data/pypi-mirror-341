# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import NwpipacketRespPayload


class PacketFeaturesBuilder:
    """
    Builds and executes requests for operations under /stream/device/nwpi/packetFeatures
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, trace_id: int, timestamp: int, flow_id: int, **kw) -> NwpipacketRespPayload:
        """
        packetFeatures for NWPI.
        GET /dataservice/stream/device/nwpi/packetFeatures

        :param trace_id: trace id
        :param timestamp: start time
        :param flow_id: flow id
        :returns: NwpipacketRespPayload
        """
        logging.warning("Operation: %s is deprecated", "getPacketFeatures")
        params = {
            "traceId": trace_id,
            "timestamp": timestamp,
            "flowId": flow_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/stream/device/nwpi/packetFeatures",
            return_type=NwpipacketRespPayload,
            params=params,
            **kw,
        )
