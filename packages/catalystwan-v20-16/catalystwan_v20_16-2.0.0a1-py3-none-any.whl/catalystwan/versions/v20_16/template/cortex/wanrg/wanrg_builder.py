# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface


class WanrgBuilder:
    """
    Builds and executes requests for operations under /template/cortex/wanrg
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, accountid: str, **kw) -> Any:
        """
        Get WAN Resource Groups
        GET /dataservice/template/cortex/wanrg

        :param accountid: Account Id
        :returns: Any
        """
        params = {
            "accountid": accountid,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/template/cortex/wanrg", params=params, **kw
        )

    def put(self, payload: Any, **kw):
        """
        Edit WAN Resource Groups
        PUT /dataservice/template/cortex/wanrg

        :param payload: WAN resource group
        :returns: None
        """
        return self._request_adapter.request(
            "PUT", "/dataservice/template/cortex/wanrg", payload=payload, **kw
        )

    def post(self, payload: Any, **kw) -> Any:
        """
        Create WAN Resource Groups
        POST /dataservice/template/cortex/wanrg

        :param payload: WAN resource group
        :returns: Any
        """
        return self._request_adapter.request(
            "POST", "/dataservice/template/cortex/wanrg", payload=payload, **kw
        )

    def delete(self, payload: Optional[Any] = None, **kw) -> Any:
        """
        Delete WAN Resource Groups
        DELETE /dataservice/template/cortex/wanrg

        :param payload: WAN resource group
        :returns: Any
        """
        return self._request_adapter.request(
            "DELETE", "/dataservice/template/cortex/wanrg", payload=payload, **kw
        )
