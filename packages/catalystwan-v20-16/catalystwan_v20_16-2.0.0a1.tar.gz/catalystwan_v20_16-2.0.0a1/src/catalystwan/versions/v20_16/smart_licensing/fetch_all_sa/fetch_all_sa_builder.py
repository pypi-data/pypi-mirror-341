# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface


class FetchAllSaBuilder:
    """
    Builds and executes requests for operations under /smartLicensing/fetchAllSa
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, payload: Optional[Any] = None, **kw) -> Any:
        """
        fetch reports offline for sle
        GET /dataservice/smartLicensing/fetchAllSa

        :param payload: Partner
        :returns: Any
        """
        return self._request_adapter.request(
            "GET", "/dataservice/smartLicensing/fetchAllSa", payload=payload, **kw
        )
