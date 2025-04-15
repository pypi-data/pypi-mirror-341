# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class DefinitionBuilder:
    """
    Builds and executes requests for operations under /template/policy/vedge/definition
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, policy_id: str, **kw) -> Any:
        """
        Get template
        GET /dataservice/template/policy/vedge/definition/{policyId}

        :param policy_id: Policy Id
        :returns: Any
        """
        params = {
            "policyId": policy_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/template/policy/vedge/definition/{policyId}", params=params, **kw
        )
