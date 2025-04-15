# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class CustomappsBuilder:
    """
    Builds and executes requests for operations under /sdavc/customapps
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[Any]:
        """
        Displays the user-defined applications
        GET /dataservice/sdavc/customapps

        :returns: List[Any]
        """
        return self._request_adapter.request(
            "GET", "/dataservice/sdavc/customapps", return_type=List[Any], **kw
        )
