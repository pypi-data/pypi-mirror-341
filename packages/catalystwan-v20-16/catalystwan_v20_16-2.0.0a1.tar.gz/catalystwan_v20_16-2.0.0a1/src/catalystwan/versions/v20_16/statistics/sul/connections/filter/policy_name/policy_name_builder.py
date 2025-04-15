# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import PolicyTypeParam


class PolicyNameBuilder:
    """
    Builds and executes requests for operations under /statistics/sul/connections/filter/policy_name
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, policy_type: PolicyTypeParam, query: str, **kw) -> List[Any]:
        """
        Get filter Policy Name list
        GET /dataservice/statistics/sul/connections/filter/policy_name/{policyType}

        :param policy_type: Policy type
        :param query: query string
        :returns: List[Any]
        """
        params = {
            "policyType": policy_type,
            "query": query,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/statistics/sul/connections/filter/policy_name/{policyType}",
            return_type=List[Any],
            params=params,
            **kw,
        )
