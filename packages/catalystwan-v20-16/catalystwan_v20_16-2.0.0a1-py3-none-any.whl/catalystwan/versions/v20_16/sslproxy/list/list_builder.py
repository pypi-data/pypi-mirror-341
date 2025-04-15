# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class ListBuilder:
    """
    Builds and executes requests for operations under /sslproxy/list
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[Any]:
        """
        Get SSL proxy certificate list
        GET /dataservice/sslproxy/list

        :returns: List[Any]
        """
        return self._request_adapter.request(
            "GET", "/dataservice/sslproxy/list", return_type=List[Any], **kw
        )
