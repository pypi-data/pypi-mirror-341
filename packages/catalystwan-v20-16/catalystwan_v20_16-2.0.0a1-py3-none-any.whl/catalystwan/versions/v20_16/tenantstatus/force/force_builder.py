# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class ForceBuilder:
    """
    Builds and executes requests for operations under /tenantstatus/force
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, **kw):
        """
        Force tenant status collection


        Note: In a multitenant vManage system, this API is only available in the Provider view.
        POST /dataservice/tenantstatus/force

        :returns: None
        """
        return self._request_adapter.request("POST", "/dataservice/tenantstatus/force", **kw)
