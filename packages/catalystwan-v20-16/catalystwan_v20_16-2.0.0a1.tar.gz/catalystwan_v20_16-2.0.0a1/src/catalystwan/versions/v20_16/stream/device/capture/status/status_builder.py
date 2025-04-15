# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import GetFileDownloadStatusRes


class StatusBuilder:
    """
    Builds and executes requests for operations under /stream/device/capture/status
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, session_id: str, **kw) -> GetFileDownloadStatusRes:
        """
        Get packet capture session status
        GET /dataservice/stream/device/capture/status/{sessionId}

        :param session_id: Session id
        :returns: GetFileDownloadStatusRes
        """
        params = {
            "sessionId": session_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/stream/device/capture/status/{sessionId}",
            return_type=GetFileDownloadStatusRes,
            params=params,
            **kw,
        )
