# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .recommendation.recommendation_builder import RecommendationBuilder


class WaniBuilder:
    """
    Builds and executes requests for operations under /policy/wani
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def recommendation(self) -> RecommendationBuilder:
        """
        The recommendation property
        """
        from .recommendation.recommendation_builder import RecommendationBuilder

        return RecommendationBuilder(self._request_adapter)
