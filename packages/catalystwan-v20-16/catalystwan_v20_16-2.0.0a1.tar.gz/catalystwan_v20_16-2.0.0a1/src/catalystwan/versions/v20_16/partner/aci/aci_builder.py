# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .policy.policy_builder import PolicyBuilder


class AciBuilder:
    """
    Builds and executes requests for operations under /partner/aci
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def policy(self) -> PolicyBuilder:
        """
        The policy property
        """
        from .policy.policy_builder import PolicyBuilder

        return PolicyBuilder(self._request_adapter)
