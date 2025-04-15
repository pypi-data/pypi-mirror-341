# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List

from catalystwan.abc import RequestAdapterInterface


class RootcertchainsBuilder:
    """
    Builds and executes requests for operations under /certificate/rootcertchains
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, action: str, **kw) -> List[str]:
        """
        get root cert chain in the system
        GET /dataservice/certificate/rootcertchains

        :param action: Action Parameter to fetch root cert chains
        :returns: List[str]
        """
        params = {
            "action": action,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/certificate/rootcertchains",
            return_type=List[str],
            params=params,
            **kw,
        )

    def put(self, payload: str, **kw) -> str:
        """
        save root cert chain in the system
        PUT /dataservice/certificate/rootcertchains

        :param payload: JSON payload with RootCertChain and Certificate details.
        :returns: str
        """
        return self._request_adapter.request(
            "PUT", "/dataservice/certificate/rootcertchains", return_type=str, payload=payload, **kw
        )
