# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class CancelBuilder:
    """
    Builds and executes requests for operations under /sdavc/protocol-pack/maintenance/upgrade/cancel
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, **kw) -> Any:
        """
        Cancel a Scheduled Deploy protocol pack job
        POST /dataservice/sdavc/protocol-pack/maintenance/upgrade/cancel

        :returns: Any
        """
        return self._request_adapter.request(
            "POST", "/dataservice/sdavc/protocol-pack/maintenance/upgrade/cancel", **kw
        )
