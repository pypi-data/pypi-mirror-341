# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface


class UsernamesBuilder:
    """
    Builds and executes requests for operations under /disasterrecovery/usernames
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, payload: Optional[Any] = None, **kw) -> Any:
        """
        Fetch data centers and vBonds usernames for disaster recovery
        GET /dataservice/disasterrecovery/usernames

        :param payload: Datacenter/vBond password update request
        :returns: Any
        """
        return self._request_adapter.request(
            "GET", "/dataservice/disasterrecovery/usernames", payload=payload, **kw
        )
