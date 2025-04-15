# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DeviceBlistDeleteResponsePayload


class DelBuilder:
    """
    Builds and executes requests for operations under /stream/device/nwpi/device/blist/del
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def delete(self, system_ip: str, **kw) -> DeviceBlistDeleteResponsePayload:
        """
        Delete Device BlackList for NWPI.
        DELETE /dataservice/stream/device/nwpi/device/blist/del

        :param system_ip: systemIp
        :returns: DeviceBlistDeleteResponsePayload
        """
        logging.warning("Operation: %s is deprecated", "delDeviceBlack")
        params = {
            "systemIp": system_ip,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/stream/device/nwpi/device/blist/del",
            return_type=DeviceBlistDeleteResponsePayload,
            params=params,
            **kw,
        )
