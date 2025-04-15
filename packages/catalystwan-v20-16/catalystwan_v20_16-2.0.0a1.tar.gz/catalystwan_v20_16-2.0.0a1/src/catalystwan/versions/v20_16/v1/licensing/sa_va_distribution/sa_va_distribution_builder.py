# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import SaVaDistributionRequest, SaVaDistributionResponse


class SaVaDistributionBuilder:
    """
    Builds and executes requests for operations under /v1/licensing/sa-va-distribution
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: SaVaDistributionRequest, **kw) -> SaVaDistributionResponse:
        """
        Get Smart account and virtual account distribution of selected licenses
        POST /dataservice/v1/licensing/sa-va-distribution

        :param payload: Payload
        :returns: SaVaDistributionResponse
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/licensing/sa-va-distribution",
            return_type=SaVaDistributionResponse,
            payload=payload,
            **kw,
        )
