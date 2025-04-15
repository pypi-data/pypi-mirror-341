# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import CgwResourceResponse


class ResourceBuilder:
    """
    Builds and executes requests for operations under /multicloud/cloudgateway/resource
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, cloud_gateway_name: str, **kw) -> List[CgwResourceResponse]:
        """
        Discover Resource of CGW
        GET /dataservice/multicloud/cloudgateway/resource

        :param cloud_gateway_name: Multicloud cloud gateway name
        :returns: List[CgwResourceResponse]
        """
        params = {
            "cloudGatewayName": cloud_gateway_name,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/cloudgateway/resource",
            return_type=List[CgwResourceResponse],
            params=params,
            **kw,
        )
