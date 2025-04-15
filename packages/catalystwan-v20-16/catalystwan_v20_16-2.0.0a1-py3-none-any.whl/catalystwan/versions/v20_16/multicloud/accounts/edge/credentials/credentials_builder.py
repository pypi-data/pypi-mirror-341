# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any

from catalystwan.abc import RequestAdapterInterface


class CredentialsBuilder:
    """
    Builds and executes requests for operations under /multicloud/accounts/edge/{accountId}/credentials
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def put(self, account_id: str, payload: Any, **kw):
        """
        Update Multicloud edge account credential
        PUT /dataservice/multicloud/accounts/edge/{accountId}/credentials

        :param account_id: Multicloud Edge Account Id
        :param payload: Multicloud edge account info
        :returns: None
        """
        logging.warning("Operation: %s is deprecated", "validateEdgeAccountUpdateCredentials")
        params = {
            "accountId": account_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/multicloud/accounts/edge/{accountId}/credentials",
            params=params,
            payload=payload,
            **kw,
        )
