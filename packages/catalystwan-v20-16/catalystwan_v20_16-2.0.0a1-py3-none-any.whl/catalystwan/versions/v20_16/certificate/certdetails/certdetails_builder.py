# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class CertdetailsBuilder:
    """
    Builds and executes requests for operations under /certificate/certdetails
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: str, **kw) -> str:
        """
        get certificaate details
        POST /dataservice/certificate/certdetails

        :param payload: Single certificate provided as string in a json formatted request body.
        :returns: str
        """
        return self._request_adapter.request(
            "POST", "/dataservice/certificate/certdetails", return_type=str, payload=payload, **kw
        )
