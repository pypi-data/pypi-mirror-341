# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import RecommendationsResponse

if TYPE_CHECKING:
    from .applied.applied_builder import AppliedBuilder


class RecommendationsBuilder:
    """
    Builds and executes requests for operations under /wani/recommendations
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, site_id: Optional[str] = None, **kw) -> RecommendationsResponse:
        """
        API to get the recommendations obtained from WANI for a given tenant. This returns only valid recommendations based on expiry. It filters out recommendations that are inactive.
        GET /dataservice/wani/recommendations

        :param site_id: The specific site id to get recommendations for, if empty get recommendations for all sites
        :returns: RecommendationsResponse
        """
        params = {
            "siteId": site_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/wani/recommendations",
            return_type=RecommendationsResponse,
            params=params,
            **kw,
        )

    @property
    def applied(self) -> AppliedBuilder:
        """
        The applied property
        """
        from .applied.applied_builder import AppliedBuilder

        return AppliedBuilder(self._request_adapter)
