# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import NvaRulesListRequest, NvaRulesResponse, Taskid


class NvaSecurityRulesBuilder:
    """
    Builds and executes requests for operations under /multicloud/cloudgateway/nvaSecurityRules
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, cloud_gateway_name: str, **kw) -> NvaRulesResponse:
        """
        Get NVA Security Rules
        GET /dataservice/multicloud/cloudgateway/nvaSecurityRules/{cloudGatewayName}

        :param cloud_gateway_name: Multicloud cloud gateway name
        :returns: NvaRulesResponse
        """
        params = {
            "cloudGatewayName": cloud_gateway_name,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/cloudgateway/nvaSecurityRules/{cloudGatewayName}",
            return_type=NvaRulesResponse,
            params=params,
            **kw,
        )

    def put(self, cloud_gateway_name: str, payload: NvaRulesListRequest, **kw) -> Taskid:
        """
        Update NVA Security Rules
        PUT /dataservice/multicloud/cloudgateway/nvaSecurityRules/{cloudGatewayName}

        :param cloud_gateway_name: Cloud gateway name
        :param payload: Update NVA security Rules
        :returns: Taskid
        """
        params = {
            "cloudGatewayName": cloud_gateway_name,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/multicloud/cloudgateway/nvaSecurityRules/{cloudGatewayName}",
            return_type=Taskid,
            params=params,
            payload=payload,
            **kw,
        )
