# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class LinksBuilder:
    """
    Builds and executes requests for operations under /device/bfd/links
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, state: str, **kw) -> List[Any]:
        """
        Get list of BFD connections
        GET /dataservice/device/bfd/links

        :param state: Device state
        :returns: List[Any]
        """
        params = {
            "state": state,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/bfd/links", return_type=List[Any], params=params, **kw
        )
