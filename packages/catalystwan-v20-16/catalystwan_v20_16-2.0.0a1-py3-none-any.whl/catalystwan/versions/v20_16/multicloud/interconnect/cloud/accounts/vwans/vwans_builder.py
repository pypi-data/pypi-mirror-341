# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import AzureVirtualWan, CloudTypeParam, InlineResponse2009


class VwansBuilder:
    """
    Builds and executes requests for operations under /multicloud/interconnect/cloud/{cloud-type}/accounts/{cloud-account-id}/vwans
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        cloud_type: str,
        cloud_account_id: str,
        resource_group: str,
        refresh: Optional[str] = "false",
        vwan_name: Optional[str] = None,
        **kw,
    ) -> InlineResponse2009:
        """
        API to retrieve Azure Virtual Wans.
        GET /dataservice/multicloud/interconnect/cloud/{cloud-type}/accounts/{cloud-account-id}/vwans

        :param cloud_type: Cloud Provider Type
        :param cloud_account_id: Cloud account id
        :param resource_group: Azure cloud resource group name
        :param refresh: Refresh
        :param vwan_name: Vwan Name
        :returns: InlineResponse2009
        """
        params = {
            "cloud-type": cloud_type,
            "cloud-account-id": cloud_account_id,
            "resource-group": resource_group,
            "refresh": refresh,
            "vwan-name": vwan_name,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/interconnect/cloud/{cloud-type}/accounts/{cloud-account-id}/vwans",
            return_type=InlineResponse2009,
            params=params,
            **kw,
        )

    def post(
        self, cloud_type: str, cloud_account_id: str, payload: AzureVirtualWan, **kw
    ) -> InlineResponse2009:
        """
        API to create an Azure Virtual Wan..
        POST /dataservice/multicloud/interconnect/cloud/{cloud-type}/accounts/{cloud-account-id}/vwans

        :param cloud_type: Cloud Provider Type
        :param cloud_account_id: Cloud account id
        :param payload: Request Payload for Multicloud Interconnect Azure Vwan
        :returns: InlineResponse2009
        """
        params = {
            "cloud-type": cloud_type,
            "cloud-account-id": cloud_account_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/multicloud/interconnect/cloud/{cloud-type}/accounts/{cloud-account-id}/vwans",
            return_type=InlineResponse2009,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(
        self,
        cloud_type: CloudTypeParam,
        cloud_account_id: str,
        vwan_name: str,
        resource_group: Optional[str] = None,
        **kw,
    ) -> Any:
        """
        API to delete an Azure Virtual Wan.
        DELETE /dataservice/multicloud/interconnect/cloud/{cloud-type}/accounts/{cloud-account-id}/vwans/{vwan-name}

        :param cloud_type: Cloud Provider Type
        :param cloud_account_id: Cloud account id
        :param vwan_name: Vwan name
        :param resource_group: Azure cloud resource group name
        :returns: Any
        """
        params = {
            "cloud-type": cloud_type,
            "cloud-account-id": cloud_account_id,
            "vwan-name": vwan_name,
            "resource-group": resource_group,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/multicloud/interconnect/cloud/{cloud-type}/accounts/{cloud-account-id}/vwans/{vwan-name}",
            params=params,
            **kw,
        )
