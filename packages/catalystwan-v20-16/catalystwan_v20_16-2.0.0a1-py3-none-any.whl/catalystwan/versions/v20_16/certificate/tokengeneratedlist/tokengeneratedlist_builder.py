# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class TokengeneratedlistBuilder:
    """
    Builds and executes requests for operations under /certificate/tokengeneratedlist
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> str:
        """
        get token generated list
        GET /dataservice/certificate/tokengeneratedlist

        :returns: str
        """
        return self._request_adapter.request(
            "GET", "/dataservice/certificate/tokengeneratedlist", return_type=str, **kw
        )
