# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class RoleBuilder:
    """
    Builds and executes requests for operations under /admin/user/role
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> Any:
        """
        Check whether a user has admin role
        GET /dataservice/admin/user/role

        :returns: Any
        """
        return self._request_adapter.request("GET", "/dataservice/admin/user/role", **kw)
