# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import EventReadoutResponsePayloadInner


class EventReadoutBuilder:
    """
    Builds and executes requests for operations under /stream/device/nwpi/eventReadout
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        trace_id: int,
        timestamp: int,
        state: Optional[str] = None,
        vpn: Optional[str] = None,
        user_name: Optional[str] = None,
        version: Optional[str] = None,
        **kw,
    ) -> List[EventReadoutResponsePayloadInner]:
        """
        Get Trace Event Readout for NWPI.
        GET /dataservice/stream/device/nwpi/eventReadout

        :param trace_id: Trace id
        :param timestamp: Timestamp
        :param state: State
        :param vpn: Vpn
        :param user_name: User name
        :param version: Version
        :returns: List[EventReadoutResponsePayloadInner]
        """
        logging.warning("Operation: %s is deprecated", "getEventReadout")
        params = {
            "traceId": trace_id,
            "timestamp": timestamp,
            "state": state,
            "vpn": vpn,
            "userName": user_name,
            "version": version,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/stream/device/nwpi/eventReadout",
            return_type=List[EventReadoutResponsePayloadInner],
            params=params,
            **kw,
        )
