# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class CentralBuilder:
    """
    Builds and executes requests for operations under /template/policy/vsmart/activate/central
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, policy_id: str, payload: Any, **kw) -> Any:
        """
        Activate vsmart policy for a given policy id
        POST /dataservice/template/policy/vsmart/activate/central/{policyId}

        :param policy_id: Policy Id
        :param payload: Template policy
        :returns: Any
        """
        params = {
            "policyId": policy_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/template/policy/vsmart/activate/central/{policyId}",
            params=params,
            payload=payload,
            **kw,
        )
