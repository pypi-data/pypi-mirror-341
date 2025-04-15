# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class VsessionidBuilder:
    """
    Builds and executes requests for operations under /tenant/{tenantId}/vsessionid
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, tenant_id: str, **kw) -> Any:
        """
        Get VSessionId for a specific tenant


        Note: In a multitenant vManage system, this API is only available in the Provider view.
        POST /dataservice/tenant/{tenantId}/vsessionid

        :param tenant_id: Tenant Id
        :returns: Any
        """
        params = {
            "tenantId": tenant_id,
        }
        return self._request_adapter.request(
            "POST", "/dataservice/tenant/{tenantId}/vsessionid", params=params, **kw
        )
