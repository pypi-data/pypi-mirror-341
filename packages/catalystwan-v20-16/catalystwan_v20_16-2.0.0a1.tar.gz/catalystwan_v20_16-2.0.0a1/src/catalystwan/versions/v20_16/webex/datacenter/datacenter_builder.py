# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import WebexDataCenter

if TYPE_CHECKING:
    from .sync.sync_builder import SyncBuilder
    from .syncstatus.syncstatus_builder import SyncstatusBuilder


class DatacenterBuilder:
    """
    Builds and executes requests for operations under /webex/datacenter
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: WebexDataCenter, **kw) -> bool:
        """
        TEMP-Insert webex data center details manually for test setup
        POST /dataservice/webex/datacenter

        :param payload: Webex Data Center
        :returns: bool
        """
        return self._request_adapter.request(
            "POST", "/dataservice/webex/datacenter", return_type=bool, payload=payload, **kw
        )

    def delete(self, **kw) -> bool:
        """
        Delete webex data center data in DB
        DELETE /dataservice/webex/datacenter

        :returns: bool
        """
        return self._request_adapter.request(
            "DELETE", "/dataservice/webex/datacenter", return_type=bool, **kw
        )

    @property
    def sync(self) -> SyncBuilder:
        """
        The sync property
        """
        from .sync.sync_builder import SyncBuilder

        return SyncBuilder(self._request_adapter)

    @property
    def syncstatus(self) -> SyncstatusBuilder:
        """
        The syncstatus property
        """
        from .syncstatus.syncstatus_builder import SyncstatusBuilder

        return SyncstatusBuilder(self._request_adapter)
