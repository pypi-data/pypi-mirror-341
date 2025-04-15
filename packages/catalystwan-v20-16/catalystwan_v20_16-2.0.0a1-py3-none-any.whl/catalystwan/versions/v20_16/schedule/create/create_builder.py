# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class CreateBuilder:
    """
    Builds and executes requests for operations under /schedule/create
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw) -> Any:
        """
        create  backup scheduler config-db and statstics database with startDateTime and persist to config-db
        POST /dataservice/schedule/create

        :param payload: schedule request information
        :returns: Any
        """
        return self._request_adapter.request(
            "POST", "/dataservice/schedule/create", payload=payload, **kw
        )
