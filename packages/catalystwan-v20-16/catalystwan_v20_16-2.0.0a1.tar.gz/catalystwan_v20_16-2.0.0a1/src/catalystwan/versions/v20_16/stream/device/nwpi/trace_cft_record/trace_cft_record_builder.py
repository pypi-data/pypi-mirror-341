# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import TraceCftRecordResponsePayload


class TraceCftRecordBuilder:
    """
    Builds and executes requests for operations under /stream/device/nwpi/traceCftRecord
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        trace_id: int,
        entry_time: int,
        trace_state: str,
        vpn_ids: Optional[List[int]] = None,
        local_colors: Optional[List[str]] = None,
        devices: Optional[List[str]] = None,
        vrf_names: Optional[List[str]] = None,
        **kw,
    ) -> TraceCftRecordResponsePayload:
        """
        Get Trace CFT record
        GET /dataservice/stream/device/nwpi/traceCftRecord

        :param trace_id: TraceId
        :param entry_time: entryTime
        :param trace_state: traceState
        :param vpn_ids: vpnIds
        :param local_colors: localColors
        :param devices: devices
        :param vrf_names: vrfNames
        :returns: TraceCftRecordResponsePayload
        """
        logging.warning("Operation: %s is deprecated", "getTraceCftRecord")
        params = {
            "traceId": trace_id,
            "entryTime": entry_time,
            "traceState": trace_state,
            "vpnIds": vpn_ids,
            "localColors": local_colors,
            "devices": devices,
            "vrfNames": vrf_names,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/stream/device/nwpi/traceCftRecord",
            return_type=TraceCftRecordResponsePayload,
            params=params,
            **kw,
        )
