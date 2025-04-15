# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class CsrBuilder:
    """
    Builds and executes requests for operations under /certificate/vedge/csr
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, uuid: str, **kw) -> str:
        """
        get device CSR
        GET /dataservice/certificate/vedge/csr

        :param uuid: UUID param to fetch installed CSR
        :returns: str
        """
        params = {
            "uuid": uuid,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/certificate/vedge/csr", return_type=str, params=params, **kw
        )
