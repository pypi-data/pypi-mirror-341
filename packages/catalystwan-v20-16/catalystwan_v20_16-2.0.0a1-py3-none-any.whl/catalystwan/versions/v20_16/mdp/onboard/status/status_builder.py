# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class StatusBuilder:
    """
    Builds and executes requests for operations under /mdp/onboard/status
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[Any]:
        """
        Get MDP onboarding status
        GET /dataservice/mdp/onboard/status

        :returns: List[Any]
        """
        return self._request_adapter.request(
            "GET", "/dataservice/mdp/onboard/status", return_type=List[Any], **kw
        )
