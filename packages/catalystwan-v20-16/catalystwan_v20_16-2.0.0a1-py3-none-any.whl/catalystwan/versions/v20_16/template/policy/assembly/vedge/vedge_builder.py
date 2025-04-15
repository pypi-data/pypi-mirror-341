# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class VedgeBuilder:
    """
    Builds and executes requests for operations under /template/policy/assembly/vedge
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw) -> Any:
        """
        Get policy assembly preview
        POST /dataservice/template/policy/assembly/vedge

        :param payload: Policy assembly
        :returns: Any
        """
        return self._request_adapter.request(
            "POST", "/dataservice/template/policy/assembly/vedge", payload=payload, **kw
        )

    def get(self, id: str, **kw) -> Any:
        """
        Get policy assembly preview for feature policy
        GET /dataservice/template/policy/assembly/vedge/{id}

        :param id: Policy Id
        :returns: Any
        """
        params = {
            "id": id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/template/policy/assembly/vedge/{id}", params=params, **kw
        )
