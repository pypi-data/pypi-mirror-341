# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import RatePlansResponse


class RateplansBuilder:
    """
    Builds and executes requests for operations under /v1/securedeviceonboarding/rateplans
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, account_id: str, **kw) -> RatePlansResponse:
        """
        Get rate plans by account Id
        GET /dataservice/v1/securedeviceonboarding/rateplans

        :param account_id: Account id
        :returns: RatePlansResponse
        """
        params = {
            "accountId": account_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/v1/securedeviceonboarding/rateplans",
            return_type=RatePlansResponse,
            params=params,
            **kw,
        )
