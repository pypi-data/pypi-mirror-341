# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class LinksBuilder:
    """
    Builds and executes requests for operations under /device/control/links
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, state: str, **kw) -> List[Any]:
        """
        Get connections list
        GET /dataservice/device/control/links

        :param state: Device State
        :returns: List[Any]
        """
        params = {
            "state": state,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/control/links", return_type=List[Any], params=params, **kw
        )
