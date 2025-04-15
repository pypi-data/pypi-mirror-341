# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import TypeParam


class DcaBuilder:
    """
    Builds and executes requests for operations under /dca/settings/configuration/{type}/dca
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, type_: TypeParam, payload: Any, **kw) -> Any:
        """
        Create analytics config data
        POST /dataservice/dca/settings/configuration/{type}/dca

        :param type_: Data type
        :param payload: Query string
        :returns: Any
        """
        params = {
            "type": type_,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/dca/settings/configuration/{type}/dca",
            params=params,
            payload=payload,
            **kw,
        )
