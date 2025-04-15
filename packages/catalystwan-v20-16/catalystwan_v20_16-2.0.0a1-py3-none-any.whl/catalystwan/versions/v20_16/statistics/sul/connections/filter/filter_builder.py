# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .policy_name.policy_name_builder import PolicyNameBuilder


class FilterBuilder:
    """
    Builds and executes requests for operations under /statistics/sul/connections/filter
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def policy_name(self) -> PolicyNameBuilder:
        """
        The policy_name property
        """
        from .policy_name.policy_name_builder import PolicyNameBuilder

        return PolicyNameBuilder(self._request_adapter)
