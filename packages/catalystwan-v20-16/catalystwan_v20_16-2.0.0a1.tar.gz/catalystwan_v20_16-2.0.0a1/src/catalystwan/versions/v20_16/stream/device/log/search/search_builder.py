# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class SearchBuilder:
    """
    Builds and executes requests for operations under /stream/device/log/search
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, session_id: str, payload: str, **kw):
        """
        Post
        POST /dataservice/stream/device/log/search/{sessionId}

        :param session_id: Session Id
        :param payload: Payload
        :returns: None
        """
        params = {
            "sessionId": session_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/stream/device/log/search/{sessionId}",
            params=params,
            payload=payload,
            **kw,
        )
