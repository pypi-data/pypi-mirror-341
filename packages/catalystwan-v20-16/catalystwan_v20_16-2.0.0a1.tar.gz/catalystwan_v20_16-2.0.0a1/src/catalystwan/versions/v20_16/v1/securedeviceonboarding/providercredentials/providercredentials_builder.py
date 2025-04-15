# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import ProviderAccountDetails, ProviderAccountDetailsList


class ProvidercredentialsBuilder:
    """
    Builds and executes requests for operations under /v1/securedeviceonboarding/providercredentials
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: None, **kw):
        """
        Create service provider credentials
        POST /dataservice/v1/securedeviceonboarding/providercredentials

        :param payload: Create Provider Credentials
        :returns: None
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/securedeviceonboarding/providercredentials",
            payload=payload,
            **kw,
        )

    def get(self, account_id: str, **kw) -> ProviderAccountDetailsList:
        """
        Get provider credentials by account id
        GET /dataservice/v1/securedeviceonboarding/{accountId}/providercredentials

        :param account_id: Service User Account ID
        :returns: ProviderAccountDetailsList
        """
        params = {
            "accountId": account_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/v1/securedeviceonboarding/{accountId}/providercredentials",
            return_type=ProviderAccountDetailsList,
            params=params,
            **kw,
        )

    def put(self, account_id: str, payload: ProviderAccountDetails, **kw):
        """
        Edit service provider credentials
        PUT /dataservice/v1/securedeviceonboarding/{accountId}/providercredentials

        :param account_id: Service User Account ID
        :param payload: Provider Credentials
        :returns: None
        """
        params = {
            "accountId": account_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/securedeviceonboarding/{accountId}/providercredentials",
            params=params,
            payload=payload,
            **kw,
        )
