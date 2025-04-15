# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class ConfigurationBuilder:
    """
    Builds and executes requests for operations under /v1/cloudonramp/saas/configuration
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw):
        """
        Get Policy Groups that are deployed with Cloud on Ramp for Saas intent
        GET /dataservice/v1/cloudonramp/saas/configuration

        :returns: None
        """
        return self._request_adapter.request(
            "GET", "/dataservice/v1/cloudonramp/saas/configuration", **kw
        )
