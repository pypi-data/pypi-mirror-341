# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import AppQosDataResponsePayloadInner


class AppQosDataBuilder:
    """
    Builds and executes requests for operations under /stream/device/nwpi/appQosData
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        trace_id: int,
        timestamp: int,
        received_timestamp: int,
        system_ip: Optional[str] = None,
        **kw,
    ) -> List[AppQosDataResponsePayloadInner]:
        """
        Get QoS Application data for NWPI.
        GET /dataservice/stream/device/nwpi/appQosData

        :param trace_id: Trace id
        :param timestamp: Timestamp
        :param received_timestamp: Received timestamp
        :param system_ip: systemIp
        :returns: List[AppQosDataResponsePayloadInner]
        """
        logging.warning("Operation: %s is deprecated", "getAppQosData")
        params = {
            "traceId": trace_id,
            "timestamp": timestamp,
            "receivedTimestamp": received_timestamp,
            "systemIp": system_ip,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/stream/device/nwpi/appQosData",
            return_type=List[AppQosDataResponsePayloadInner],
            params=params,
            **kw,
        )
