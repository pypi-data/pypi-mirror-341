# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import ConcurrentDomainDataResponsePayloadInner


class ConcurrentDomainDataBuilder:
    """
    Builds and executes requests for operations under /stream/device/nwpi/concurrentDomainData
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self, trace_id: int, timestamp: int, query: Optional[str] = None, **kw
    ) -> List[ConcurrentDomainDataResponsePayloadInner]:
        """
        Get concurrent domain data for NWPI.
        GET /dataservice/stream/device/nwpi/concurrentDomainData

        :param trace_id: Trace id
        :param timestamp: Timestamp
        :param query: Query
        :returns: List[ConcurrentDomainDataResponsePayloadInner]
        """
        logging.warning("Operation: %s is deprecated", "getConcurrentDomainData")
        params = {
            "traceId": trace_id,
            "timestamp": timestamp,
            "query": query,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/stream/device/nwpi/concurrentDomainData",
            return_type=List[ConcurrentDomainDataResponsePayloadInner],
            params=params,
            **kw,
        )
