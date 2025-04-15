# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import ProviderInfo


class RegisteredprovidersBuilder:
    """
    Builds and executes requests for operations under /v1/securedeviceonboarding/registeredproviders
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> ProviderInfo:
        """
        Get Registered Providers Info
        GET /dataservice/v1/securedeviceonboarding/registeredproviders

        :returns: ProviderInfo
        """
        return self._request_adapter.request(
            "GET",
            "/dataservice/v1/securedeviceonboarding/registeredproviders",
            return_type=ProviderInfo,
            **kw,
        )
