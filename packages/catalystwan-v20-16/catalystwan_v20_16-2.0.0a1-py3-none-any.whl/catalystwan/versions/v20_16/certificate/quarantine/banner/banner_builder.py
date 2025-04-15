# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List

from catalystwan.abc import RequestAdapterInterface


class BannerBuilder:
    """
    Builds and executes requests for operations under /certificate/quarantine/banner
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[str]:
        """
        get quarantine banner data
        GET /dataservice/certificate/quarantine/banner

        :returns: List[str]
        """
        return self._request_adapter.request(
            "GET", "/dataservice/certificate/quarantine/banner", return_type=List[str], **kw
        )
