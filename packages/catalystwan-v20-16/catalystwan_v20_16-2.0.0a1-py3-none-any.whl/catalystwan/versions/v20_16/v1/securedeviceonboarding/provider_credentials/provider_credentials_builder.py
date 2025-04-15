# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class ProviderCredentialsBuilder:
    """
    Builds and executes requests for operations under /v1/securedeviceonboarding/{accountId}/providerCredentials
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def delete(self, account_id: str, **kw):
        """
        Delete provider credentials
        DELETE /dataservice/v1/securedeviceonboarding/{accountId}/providerCredentials

        :param account_id: Service User Account Id
        :returns: None
        """
        params = {
            "accountId": account_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/securedeviceonboarding/{accountId}/providerCredentials",
            params=params,
            **kw,
        )
