# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import VwanListResponse


class VwansBuilder:
    """
    Builds and executes requests for operations under /multicloud/cloudgateway/vwans
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        cloud_type: str,
        account_id: str,
        resource_group_name: str,
        resource_group_source: str,
        **kw,
    ) -> List[VwanListResponse]:
        """
        Discover Azure Virtual WANS
        GET /dataservice/multicloud/cloudgateway/vwans

        :param cloud_type: Cloud type
        :param account_id: Account id
        :param resource_group_name: Resource group name
        :param resource_group_source: Resource group source
        :returns: List[VwanListResponse]
        """
        params = {
            "cloudType": cloud_type,
            "accountId": account_id,
            "resourceGroupName": resource_group_name,
            "resourceGroupSource": resource_group_source,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/cloudgateway/vwans",
            return_type=List[VwanListResponse],
            params=params,
            **kw,
        )
