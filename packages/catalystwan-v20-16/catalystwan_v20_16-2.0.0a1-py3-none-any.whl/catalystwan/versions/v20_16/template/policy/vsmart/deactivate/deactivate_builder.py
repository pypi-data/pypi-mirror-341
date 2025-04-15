# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class DeactivateBuilder:
    """
    Builds and executes requests for operations under /template/policy/vsmart/deactivate
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, policy_id: str, **kw) -> Any:
        """
        Deactivate vsmart policy for a given policy id
        POST /dataservice/template/policy/vsmart/deactivate/{policyId}

        :param policy_id: Policy Id
        :returns: Any
        """
        params = {
            "policyId": policy_id,
        }
        return self._request_adapter.request(
            "POST", "/dataservice/template/policy/vsmart/deactivate/{policyId}", params=params, **kw
        )
