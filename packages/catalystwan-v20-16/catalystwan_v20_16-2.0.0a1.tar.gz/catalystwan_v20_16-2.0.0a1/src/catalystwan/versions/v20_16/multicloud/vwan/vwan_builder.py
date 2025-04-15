# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

import logging
from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface


class VwanBuilder:
    """
    Builds and executes requests for operations under /multicloud/vwan
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw) -> Any:
        """
        Create Virtual WAN
        POST /dataservice/multicloud/vwan

        :param payload: Virtual WAN
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "createVirtualWan")
        return self._request_adapter.request(
            "POST", "/dataservice/multicloud/vwan", payload=payload, **kw
        )

    def delete(
        self,
        cloud_provider: str,
        v_wan_name: str,
        account_id: Optional[str] = None,
        resource_group: Optional[str] = None,
        **kw,
    ) -> Any:
        """
        Delete Virtual Wan
        DELETE /dataservice/multicloud/vwan/{cloudProvider}/{vWanName}

        :param cloud_provider: Cloud Provider
        :param v_wan_name: Virtual Wan name
        :param account_id: Account Id
        :param resource_group: Resource Group
        :returns: Any
        """
        logging.warning("Operation: %s is deprecated", "deleteVirtualWan")
        params = {
            "cloudProvider": cloud_provider,
            "vWanName": v_wan_name,
            "accountId": account_id,
            "resourceGroup": resource_group,
        }
        return self._request_adapter.request(
            "DELETE", "/dataservice/multicloud/vwan/{cloudProvider}/{vWanName}", params=params, **kw
        )
