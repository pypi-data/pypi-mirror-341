# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import VpnGatewayResponse


class VpnGatewaysBuilder:
    """
    Builds and executes requests for operations under /multicloud/cloudgateway/vpn-gateways
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        cloud_type: str,
        account_id: str,
        region: str,
        resource_group_name: str,
        resource_group_source: str,
        vhub_name: str,
        vhub_source: str,
        **kw,
    ) -> List[VpnGatewayResponse]:
        """
        Discover Azure Vpn Gateways
        GET /dataservice/multicloud/cloudgateway/vpn-gateways

        :param cloud_type: Cloud type
        :param account_id: Account id
        :param region: Region
        :param resource_group_name: Resource group name
        :param resource_group_source: Resource group source
        :param vhub_name: Vhub name
        :param vhub_source: Vhub source
        :returns: List[VpnGatewayResponse]
        """
        params = {
            "cloudType": cloud_type,
            "accountId": account_id,
            "region": region,
            "resourceGroupName": resource_group_name,
            "resourceGroupSource": resource_group_source,
            "vhubName": vhub_name,
            "vhubSource": vhub_source,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/cloudgateway/vpn-gateways",
            return_type=List[VpnGatewayResponse],
            params=params,
            **kw,
        )
