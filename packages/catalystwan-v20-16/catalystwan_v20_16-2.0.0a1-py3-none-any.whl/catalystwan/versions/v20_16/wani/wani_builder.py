# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .list_activation_status.list_activation_status_builder import ListActivationStatusBuilder
    from .policy_activation_status.policy_activation_status_builder import (
        PolicyActivationStatusBuilder,
    )
    from .recommendations.recommendations_builder import RecommendationsBuilder


class WaniBuilder:
    """
    Builds and executes requests for operations under /wani
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def list_activation_status(self) -> ListActivationStatusBuilder:
        """
        The listActivationStatus property
        """
        from .list_activation_status.list_activation_status_builder import (
            ListActivationStatusBuilder,
        )

        return ListActivationStatusBuilder(self._request_adapter)

    @property
    def policy_activation_status(self) -> PolicyActivationStatusBuilder:
        """
        The policyActivationStatus property
        """
        from .policy_activation_status.policy_activation_status_builder import (
            PolicyActivationStatusBuilder,
        )

        return PolicyActivationStatusBuilder(self._request_adapter)

    @property
    def recommendations(self) -> RecommendationsBuilder:
        """
        The recommendations property
        """
        from .recommendations.recommendations_builder import RecommendationsBuilder

        return RecommendationsBuilder(self._request_adapter)
