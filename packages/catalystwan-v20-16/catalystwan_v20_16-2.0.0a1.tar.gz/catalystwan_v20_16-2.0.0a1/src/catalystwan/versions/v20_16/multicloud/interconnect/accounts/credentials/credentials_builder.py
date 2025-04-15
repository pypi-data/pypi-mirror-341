# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import InterconnectAccount


class CredentialsBuilder:
    """
    Builds and executes requests for operations under /multicloud/interconnect/accounts/{interconnect-account-id}/credentials
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def put(
        self, interconnect_account_id: str, payload: InterconnectAccount, **kw
    ) -> InterconnectAccount:
        """
        API to edit associated Interconnect provider account credentials.
        PUT /dataservice/multicloud/interconnect/accounts/{interconnect-account-id}/credentials

        :param interconnect_account_id: Interconnect provider account id
        :param payload: Request Payload for Multicloud Interconnect Accounts
        :returns: InterconnectAccount
        """
        params = {
            "interconnect-account-id": interconnect_account_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/multicloud/interconnect/accounts/{interconnect-account-id}/credentials",
            return_type=InterconnectAccount,
            params=params,
            payload=payload,
            **kw,
        )
