# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import NwpiResponsePayload


class RecordBuilder:
    """
    Builds and executes requests for operations under /stream/device/nwpi/trace/record
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, device_uuid: str, payload: str, **kw) -> NwpiResponsePayload:
        """
        post flow data
        POST /dataservice/stream/device/nwpi/trace/record/{deviceUUID}

        :param device_uuid: Device uuid
        :param payload: Payload
        :returns: NwpiResponsePayload
        """
        logging.warning("Operation: %s is deprecated", "nwpiPostFlowData")
        params = {
            "deviceUUID": device_uuid,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/stream/device/nwpi/trace/record/{deviceUUID}",
            return_type=NwpiResponsePayload,
            params=params,
            payload=payload,
            **kw,
        )
