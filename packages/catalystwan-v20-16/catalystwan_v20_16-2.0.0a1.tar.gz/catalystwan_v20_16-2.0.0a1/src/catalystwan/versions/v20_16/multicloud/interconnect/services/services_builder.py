# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import InterconnectService


class ServicesBuilder:
    """
    Builds and executes requests for operations under /multicloud/interconnect/services
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        interconnect_service_vendor_name: str,
        interconnect_type: str,
        interconnect_service_type: str,
        **kw,
    ) -> List[InterconnectService]:
        """
        API to retrieve the Interconnect Services Information from vManage.
        GET /dataservice/multicloud/interconnect/services

        :param interconnect_service_vendor_name: Interconnect service vendor name
        :param interconnect_type: Interconnect provider type
        :param interconnect_service_type: Interconnect service type
        :returns: List[InterconnectService]
        """
        params = {
            "interconnect-service-vendor-name": interconnect_service_vendor_name,
            "interconnect-type": interconnect_type,
            "interconnect-service-type": interconnect_service_type,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/interconnect/services",
            return_type=List[InterconnectService],
            params=params,
            **kw,
        )
