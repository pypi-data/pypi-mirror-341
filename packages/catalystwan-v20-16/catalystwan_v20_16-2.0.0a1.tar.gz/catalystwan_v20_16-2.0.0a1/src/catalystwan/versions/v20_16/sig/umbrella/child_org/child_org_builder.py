# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class ChildOrgBuilder:
    """
    Builds and executes requests for operations under /sig/umbrella/childOrg
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, type_: str, **kw):
        """
        Get the list of child org IDs given the type management or device
        GET /dataservice/sig/umbrella/childOrg/{type}

        :param type_: Type
        :returns: None
        """
        params = {
            "type": type_,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/sig/umbrella/childOrg/{type}", params=params, **kw
        )
