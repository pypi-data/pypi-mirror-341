# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import LocalTlocColorParam, RemoteTlocColorParam


class InboundBuilder:
    """
    Builds and executes requests for operations under /device/ipsec/inbound
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        device_id: str,
        remote_tloc_address: Optional[str] = None,
        remote_tloc_color: Optional[RemoteTlocColorParam] = None,
        local_tloc_color: Optional[LocalTlocColorParam] = None,
        **kw,
    ) -> List[Any]:
        """
        Get IPsec inbound connection list from device (Real Time)
        GET /dataservice/device/ipsec/inbound

        :param remote_tloc_address: Remote TLOC address
        :param remote_tloc_color: Remote tloc color
        :param local_tloc_color: Local tloc color
        :param device_id: deviceId - Device IP
        :returns: List[Any]
        """
        params = {
            "remote-tloc-address": remote_tloc_address,
            "remote-tloc-color": remote_tloc_color,
            "local-tloc-color": local_tloc_color,
            "deviceId": device_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/ipsec/inbound", return_type=List[Any], params=params, **kw
        )
