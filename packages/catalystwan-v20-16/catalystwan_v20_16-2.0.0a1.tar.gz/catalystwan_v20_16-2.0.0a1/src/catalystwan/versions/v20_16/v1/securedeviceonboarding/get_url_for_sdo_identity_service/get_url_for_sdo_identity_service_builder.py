# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class GetUrlForSdoIdentityServiceBuilder:
    """
    Builds and executes requests for operations under /v1/securedeviceonboarding/getUrlForSdoIdentityService
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> str:
        """
        Get URL for Secure Device Onboarding Identity Service that generates Session ID required for authentication to get Secure Device Onboarding token
        GET /dataservice/v1/securedeviceonboarding/getUrlForSdoIdentityService

        :returns: str
        """
        return self._request_adapter.request(
            "GET",
            "/dataservice/v1/securedeviceonboarding/getUrlForSdoIdentityService",
            return_type=str,
            **kw,
        )
