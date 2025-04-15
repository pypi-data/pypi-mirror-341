# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class AutoBuilder:
    """
    Builds and executes requests for operations under /device/action/software/package/utdsignature/{type}/mode/auto
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, type_: str, payload: Any, **kw):
        """
        add Utd remote image
        POST /dataservice/device/action/software/package/utdsignature/{type}/mode/auto

        :param type_: Type
        :param payload: Request body
        :returns: None
        """
        params = {
            "type": type_,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/device/action/software/package/utdsignature/{type}/mode/auto",
            params=params,
            payload=payload,
            **kw,
        )
