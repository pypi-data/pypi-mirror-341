# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class ActionsBuilder:
    """
    Builds and executes requests for operations under /fedramp/dnssec/actions
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, action: str, **kw) -> Any:
        """
        Request DNS-Sec actions
        GET /dataservice/fedramp/dnssec/actions

        :param action: DNS-Sec action
        :returns: Any
        """
        params = {
            "action": action,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/fedramp/dnssec/actions", params=params, **kw
        )
