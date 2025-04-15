# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class PasswordBuilder:
    """
    Builds and executes requests for operations under /disasterrecovery/password
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw) -> Any:
        """
        Update data centers and vBonds passwords for disaster recovery
        POST /dataservice/disasterrecovery/password

        :param payload: Datacenter/vBond password update request
        :returns: Any
        """
        return self._request_adapter.request(
            "POST", "/dataservice/disasterrecovery/password", payload=payload, **kw
        )
