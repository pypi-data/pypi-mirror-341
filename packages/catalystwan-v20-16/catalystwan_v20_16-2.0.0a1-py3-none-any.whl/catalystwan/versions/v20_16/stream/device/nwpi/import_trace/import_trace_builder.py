# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import ImportTraceRequest, ImportTraceResponse


class ImportTraceBuilder:
    """
    Builds and executes requests for operations under /stream/device/nwpi/importTrace
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, payload: ImportTraceRequest, new_trace_name: Optional[str] = None, **kw
    ) -> ImportTraceResponse:
        """
        Import Trace
        POST /dataservice/stream/device/nwpi/importTrace

        :param new_trace_name: New trace name
        :param payload: Trace Data File
        :returns: ImportTraceResponse
        """
        params = {
            "newTraceName": new_trace_name,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/stream/device/nwpi/importTrace",
            return_type=ImportTraceResponse,
            params=params,
            payload=payload,
            **kw,
        )
