# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class RmaupdateBuilder:
    """
    Builds and executes requests for operations under /template/config/rmaupdate
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def put(self, payload: Any, **kw):
        """
        Update new device
        PUT /dataservice/template/config/rmaupdate

        :param payload: Template config
        :returns: None
        """
        return self._request_adapter.request(
            "PUT", "/dataservice/template/config/rmaupdate", payload=payload, **kw
        )
