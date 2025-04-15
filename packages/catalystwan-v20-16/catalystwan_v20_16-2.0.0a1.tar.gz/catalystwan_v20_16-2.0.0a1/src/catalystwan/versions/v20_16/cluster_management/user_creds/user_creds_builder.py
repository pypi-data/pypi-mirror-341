# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class UserCredsBuilder:
    """
    Builds and executes requests for operations under /clusterManagement/userCreds
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw):
        """
        Add or update user credentials for cluster operations


        Note: In a multitenant vManage system, this API is only available in the Provider view.
        POST /dataservice/clusterManagement/userCreds

        :param payload: User credential
        :returns: None
        """
        return self._request_adapter.request(
            "POST", "/dataservice/clusterManagement/userCreds", payload=payload, **kw
        )
