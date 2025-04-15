# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import ApplyRecommendationRes


class ProcessBuilder:
    """
    Builds and executes requests for operations under /policy/wani/recommendation/process
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, key: str, **kw) -> ApplyRecommendationRes:
        """
        Applies recommendations to a centralized policy
        POST /dataservice/policy/wani/recommendation/process

        :param key: Key from vAnalytics to retrieve recommendation json
        :returns: ApplyRecommendationRes
        """
        params = {
            "key": key,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/policy/wani/recommendation/process",
            return_type=ApplyRecommendationRes,
            params=params,
            **kw,
        )
