# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class ConfigBuilder:
    """
    Builds and executes requests for operations under /fedramp/dnssec/config
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw):
        """
        Configure DNS-Sec
        POST /dataservice/fedramp/dnssec/config

        :param payload: DNS sec config request
        :returns: None
        """
        return self._request_adapter.request(
            "POST", "/dataservice/fedramp/dnssec/config", payload=payload, **kw
        )
