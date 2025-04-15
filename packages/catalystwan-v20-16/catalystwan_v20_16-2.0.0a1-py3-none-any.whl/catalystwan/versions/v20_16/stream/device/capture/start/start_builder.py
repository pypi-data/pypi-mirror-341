# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import PacketCaptureInfo


class StartBuilder:
    """
    Builds and executes requests for operations under /stream/device/capture/start
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, session_id: str, **kw) -> PacketCaptureInfo:
        """
        Start packet capture session
        GET /dataservice/stream/device/capture/start/{sessionId}

        :param session_id: Session id
        :returns: PacketCaptureInfo
        """
        params = {
            "sessionId": session_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/stream/device/capture/start/{sessionId}",
            return_type=PacketCaptureInfo,
            params=params,
            **kw,
        )
