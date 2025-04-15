# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class WebexsyncstatusBuilder:
    """
    Builds and executes requests for operations under /v1/cloudonramp/saas/webexsyncstatus
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw):
        """
        Get Webex's sync Status for devices with COR Saas enabled via config group or device template
        GET /dataservice/v1/cloudonramp/saas/webexsyncstatus

        :returns: None
        """
        return self._request_adapter.request(
            "GET", "/dataservice/v1/cloudonramp/saas/webexsyncstatus", **kw
        )
