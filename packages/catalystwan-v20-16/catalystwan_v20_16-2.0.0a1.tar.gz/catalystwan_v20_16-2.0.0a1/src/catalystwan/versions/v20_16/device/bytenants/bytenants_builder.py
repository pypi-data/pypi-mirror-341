# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional

from catalystwan.abc import RequestAdapterInterface


class BytenantsBuilder:
    """
    Builds and executes requests for operations under /device/bytenants
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, tenant: Optional[List[str]] = None, **kw):
        """
        Gets devices and sites for all tenants
        GET /dataservice/device/bytenants

        :param tenant: Tenant
        :returns: None
        """
        params = {
            "tenant": tenant,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/device/bytenants", params=params, **kw
        )
