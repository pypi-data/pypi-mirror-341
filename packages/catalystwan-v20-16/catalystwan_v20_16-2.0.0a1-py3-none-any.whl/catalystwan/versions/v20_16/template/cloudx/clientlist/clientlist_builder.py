# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class ClientlistBuilder:
    """
    Builds and executes requests for operations under /template/cloudx/clientlist
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[Any]:
        """
        Get site list
        GET /dataservice/template/cloudx/clientlist

        :returns: List[Any]
        """
        return self._request_adapter.request(
            "GET", "/dataservice/template/cloudx/clientlist", return_type=List[Any], **kw
        )
