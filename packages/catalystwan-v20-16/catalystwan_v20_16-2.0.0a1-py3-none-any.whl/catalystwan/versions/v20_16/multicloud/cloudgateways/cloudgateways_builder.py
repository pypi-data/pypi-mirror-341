# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import CloudGatewayListResponse, CloudTypeParam


class CloudgatewaysBuilder:
    """
    Builds and executes requests for operations under /multicloud/cloudgateways
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, cloud_type: CloudTypeParam, **kw) -> List[CloudGatewayListResponse]:
        """
        Get sites with connectivity to the cloud by cloud type
        GET /dataservice/multicloud/cloudgateways/{cloudType}

        :param cloud_type: Cloud type
        :returns: List[CloudGatewayListResponse]
        """
        params = {
            "cloudType": cloud_type,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/cloudgateways/{cloudType}",
            return_type=List[CloudGatewayListResponse],
            params=params,
            **kw,
        )
