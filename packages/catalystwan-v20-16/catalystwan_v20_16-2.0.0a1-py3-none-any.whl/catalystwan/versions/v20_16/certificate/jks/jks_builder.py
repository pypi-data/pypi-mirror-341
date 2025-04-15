# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class JksBuilder:
    """
    Builds and executes requests for operations under /certificate/jks
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def put(self, payload: str, **kw) -> str:
        """
        update JKS
        PUT /dataservice/certificate/jks

        :param payload: JSON payload with encoded JKS.
        :returns: str
        """
        return self._request_adapter.request(
            "PUT", "/dataservice/certificate/jks", return_type=str, payload=payload, **kw
        )
