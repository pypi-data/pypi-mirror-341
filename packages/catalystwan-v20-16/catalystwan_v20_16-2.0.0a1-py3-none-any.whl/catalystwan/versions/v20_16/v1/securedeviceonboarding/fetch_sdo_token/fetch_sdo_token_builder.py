# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DetailsForIdentityVerificationForSdoToken


class FetchSdoTokenBuilder:
    """
    Builds and executes requests for operations under /v1/securedeviceonboarding/fetchSdoToken
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: DetailsForIdentityVerificationForSdoToken, **kw):
        """
        POST for fetching Secure Device Onboarding Token needed for Secure Device Onboarding APIs for eSim
        POST /dataservice/v1/securedeviceonboarding/fetchSdoToken

        :param payload: Fetch SDO Token
        :returns: None
        """
        return self._request_adapter.request(
            "POST", "/dataservice/v1/securedeviceonboarding/fetchSdoToken", payload=payload, **kw
        )
