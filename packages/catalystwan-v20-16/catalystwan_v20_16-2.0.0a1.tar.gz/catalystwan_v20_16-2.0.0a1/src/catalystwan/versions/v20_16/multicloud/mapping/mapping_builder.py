# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import CgwVpnsResponse


class MappingBuilder:
    """
    Builds and executes requests for operations under /multicloud/mapping
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self, cloud_type: str, cloud_gateway_name: str, site_uuid: Optional[str] = None, **kw
    ) -> CgwVpnsResponse:
        """
        Get associated mappings to the CGW
        GET /dataservice/multicloud/mapping/{cloudType}

        :param cloud_type: Multicloud provider type
        :param cloud_gateway_name: Cloud gateway name
        :param site_uuid: Site uuid
        :returns: CgwVpnsResponse
        """
        params = {
            "cloudType": cloud_type,
            "cloudGatewayName": cloud_gateway_name,
            "siteUuid": site_uuid,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/mapping/{cloudType}",
            return_type=CgwVpnsResponse,
            params=params,
            **kw,
        )
