# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import CloudTypeParam, InlineResponse2008


class TransitGatewaysBuilder:
    """
    Builds and executes requests for operations under /multicloud/interconnect/cloud/{cloud-type}/accounts/{cloud-account-id}/transit-gateways
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        cloud_type: CloudTypeParam,
        cloud_account_id: str,
        transit_gateway_name: Optional[str] = None,
        region: Optional[str] = None,
        tag_name: Optional[str] = None,
        refresh: Optional[str] = "false",
        **kw,
    ) -> InlineResponse2008:
        """
        API to retrieve AWS Transit Gateways.
        GET /dataservice/multicloud/interconnect/cloud/{cloud-type}/accounts/{cloud-account-id}/transit-gateways

        :param cloud_type: Cloud Provider Type
        :param cloud_account_id: Cloud account id
        :param transit_gateway_name: Transit gateway name
        :param region: Region
        :param tag_name: Tag name
        :param refresh: Refresh
        :returns: InlineResponse2008
        """
        params = {
            "cloud-type": cloud_type,
            "cloud-account-id": cloud_account_id,
            "transit-gateway-name": transit_gateway_name,
            "region": region,
            "tag-name": tag_name,
            "refresh": refresh,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/interconnect/cloud/{cloud-type}/accounts/{cloud-account-id}/transit-gateways",
            return_type=InlineResponse2008,
            params=params,
            **kw,
        )
