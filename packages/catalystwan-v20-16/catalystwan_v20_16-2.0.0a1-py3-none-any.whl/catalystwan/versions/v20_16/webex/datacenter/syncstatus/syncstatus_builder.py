# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import SyncStatusResponse


class SyncstatusBuilder:
    """
    Builds and executes requests for operations under /webex/datacenter/syncstatus
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> SyncStatusResponse:
        """
        Get webex data center sync status from DB
        GET /dataservice/webex/datacenter/syncstatus

        :returns: SyncStatusResponse
        """
        return self._request_adapter.request(
            "GET", "/dataservice/webex/datacenter/syncstatus", return_type=SyncStatusResponse, **kw
        )

    def put(self, **kw) -> bool:
        """
        Set webex data center sync needed            to false
        PUT /dataservice/webex/datacenter/syncstatus

        :returns: bool
        """
        return self._request_adapter.request(
            "PUT", "/dataservice/webex/datacenter/syncstatus", return_type=bool, **kw
        )
