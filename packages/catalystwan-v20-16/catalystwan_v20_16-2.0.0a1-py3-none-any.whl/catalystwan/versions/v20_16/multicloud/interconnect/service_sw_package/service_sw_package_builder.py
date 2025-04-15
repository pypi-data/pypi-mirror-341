# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import InlineResponse20015


class ServiceSwPackageBuilder:
    """
    Builds and executes requests for operations under /multicloud/interconnect/service-sw-package
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        interconnect_provider_name: str,
        interconnect_account_id: str,
        interconnect_service_type: str,
        interconnect_service_vendor_name: str,
        region: Optional[str] = None,
        **kw,
    ) -> InlineResponse20015:
        """
        API to retrieve the Interconnect Services Sw Package Types Information from vManage.
        GET /dataservice/multicloud/interconnect/service-sw-package

        :param interconnect_provider_name: Interconnect provider name
        :param interconnect_account_id: Interconnect account id
        :param interconnect_service_type: Interconnect service type
        :param interconnect_service_vendor_name: Interconnect service vendor name
        :param region: Region
        :returns: InlineResponse20015
        """
        params = {
            "interconnect-provider-name": interconnect_provider_name,
            "interconnect-account-id": interconnect_account_id,
            "interconnect-service-type": interconnect_service_type,
            "interconnect-service-vendor-name": interconnect_service_vendor_name,
            "region": region,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/interconnect/service-sw-package",
            return_type=InlineResponse20015,
            params=params,
            **kw,
        )
