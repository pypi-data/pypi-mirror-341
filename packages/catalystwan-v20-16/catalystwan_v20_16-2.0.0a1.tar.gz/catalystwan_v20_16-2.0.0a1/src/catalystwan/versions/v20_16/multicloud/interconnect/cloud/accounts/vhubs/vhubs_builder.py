# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface


class VhubsBuilder:
    """
    Builds and executes requests for operations under /multicloud/interconnect/cloud/{cloud-type}/accounts/{cloud-account-id}/vhubs
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        cloud_type: str,
        cloud_account_id: str,
        resource_group: Optional[str] = None,
        refresh: Optional[str] = "false",
        vwan_name: Optional[str] = None,
        tag_name: Optional[str] = None,
        **kw,
    ) -> Any:
        """
        API to retrieve Azure Virtual Hubs.
        GET /dataservice/multicloud/interconnect/cloud/{cloud-type}/accounts/{cloud-account-id}/vhubs

        :param cloud_type: Cloud Provider Type
        :param cloud_account_id: Cloud account id
        :param resource_group: Azure cloud resource group name
        :param refresh: Refresh
        :param vwan_name: Vwan name
        :param tag_name: Tag name
        :returns: Any
        """
        params = {
            "cloud-type": cloud_type,
            "cloud-account-id": cloud_account_id,
            "resource-group": resource_group,
            "refresh": refresh,
            "vwan-name": vwan_name,
            "tag-name": tag_name,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/interconnect/cloud/{cloud-type}/accounts/{cloud-account-id}/vhubs",
            params=params,
            **kw,
        )
