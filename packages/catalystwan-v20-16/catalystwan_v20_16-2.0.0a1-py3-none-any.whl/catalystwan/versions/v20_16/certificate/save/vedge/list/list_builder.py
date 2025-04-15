# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class ListBuilder:
    """
    Builds and executes requests for operations under /certificate/save/vedge/list
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: str, **kw) -> str:
        """
        change VedgeList Validity
        POST /dataservice/certificate/save/vedge/list

        :param payload: JSON payload with RootCertChain and Certificate details.
        :returns: str
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/certificate/save/vedge/list",
            return_type=str,
            payload=payload,
            **kw,
        )
