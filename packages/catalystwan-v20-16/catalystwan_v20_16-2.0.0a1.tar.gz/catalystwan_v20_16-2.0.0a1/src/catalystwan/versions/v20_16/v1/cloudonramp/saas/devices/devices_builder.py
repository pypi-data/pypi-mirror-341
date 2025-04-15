# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class DevicesBuilder:
    """
    Builds and executes requests for operations under /v1/cloudonramp/saas/devices
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw):
        """
        Get site, apps and device role information for cloud on ramp devices
        GET /dataservice/v1/cloudonramp/saas/devices

        :returns: None
        """
        return self._request_adapter.request(
            "GET", "/dataservice/v1/cloudonramp/saas/devices", **kw
        )
