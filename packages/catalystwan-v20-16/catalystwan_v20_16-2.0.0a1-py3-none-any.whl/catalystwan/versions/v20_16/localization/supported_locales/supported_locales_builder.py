# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class SupportedLocalesBuilder:
    """
    Builds and executes requests for operations under /localization/supportedLocales
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[Any]:
        """
        Get Supported locales
        GET /dataservice/localization/supportedLocales

        :returns: List[Any]
        """
        return self._request_adapter.request(
            "GET", "/dataservice/localization/supportedLocales", return_type=List[Any], **kw
        )
