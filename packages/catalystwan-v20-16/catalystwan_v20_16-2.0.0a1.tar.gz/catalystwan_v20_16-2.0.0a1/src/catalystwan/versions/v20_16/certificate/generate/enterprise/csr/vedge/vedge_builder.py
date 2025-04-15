# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class VedgeBuilder:
    """
    Builds and executes requests for operations under /certificate/generate/enterprise/csr/vedge
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw) -> str:
        """
        generate CSR on hardware WAN edge device
        POST /dataservice/certificate/generate/enterprise/csr/vedge

        :param payload: Device UUID
        :returns: str
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/certificate/generate/enterprise/csr/vedge",
            return_type=str,
            payload=payload,
            **kw,
        )
