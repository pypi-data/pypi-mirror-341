# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import FetchAccounts1PostRequest, SmartLicensingfetchAccountsResp


class FetchaccountsBuilder:
    """
    Builds and executes requests for operations under /hsec/fetchaccounts
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        username: Optional[str] = None,
        pwd: Optional[str] = None,
        mode: Optional[str] = None,
        **kw,
    ) -> SmartLicensingfetchAccountsResp:
        """
        Authenticate User and Sync Licenses
        GET /dataservice/hsec/fetchaccounts

        :param username: Username
        :param pwd: Pwd
        :param mode: Mode
        :returns: SmartLicensingfetchAccountsResp
        """
        params = {
            "username": username,
            "pwd": pwd,
            "mode": mode,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/hsec/fetchaccounts",
            return_type=SmartLicensingfetchAccountsResp,
            params=params,
            **kw,
        )

    def post(self, payload: FetchAccounts1PostRequest, **kw) -> SmartLicensingfetchAccountsResp:
        """
        Authenticate User and Sync Licenses
        POST /dataservice/hsec/fetchaccounts

        :param payload: Hsec License sync request payload
        :returns: SmartLicensingfetchAccountsResp
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/hsec/fetchaccounts",
            return_type=SmartLicensingfetchAccountsResp,
            payload=payload,
            **kw,
        )
