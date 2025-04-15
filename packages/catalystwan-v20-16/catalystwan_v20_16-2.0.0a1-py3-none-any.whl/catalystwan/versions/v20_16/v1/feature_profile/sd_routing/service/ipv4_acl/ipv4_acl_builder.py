# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdroutingServiceIpv4AclFeaturePostRequest,
    CreateSdroutingServiceIpv4AclFeaturePostResponse,
    EditSdroutingServiceIpv4AclFeaturePutRequest,
    EditSdroutingServiceIpv4AclFeaturePutResponse,
    GetListSdRoutingServiceIpv4AclPayload,
    GetSingleSdRoutingServiceIpv4AclPayload,
)


class Ipv4AclBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/service/{serviceId}/ipv4-acl
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, service_id: str, payload: CreateSdroutingServiceIpv4AclFeaturePostRequest, **kw
    ) -> CreateSdroutingServiceIpv4AclFeaturePostResponse:
        """
        Create a SD-Routing IPv4 ACL feature from a specific service feature profile
        POST /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/ipv4-acl

        :param service_id: Service Profile ID
        :param payload: SD-Routing IPv4 ACL feature from a specific service feature profile
        :returns: CreateSdroutingServiceIpv4AclFeaturePostResponse
        """
        params = {
            "serviceId": service_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/ipv4-acl",
            return_type=CreateSdroutingServiceIpv4AclFeaturePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        service_id: str,
        ipv4_acl_id: str,
        payload: EditSdroutingServiceIpv4AclFeaturePutRequest,
        **kw,
    ) -> EditSdroutingServiceIpv4AclFeaturePutResponse:
        """
        Edit the SD-Routing IPv4 ACL feature from a specific service feature profile
        PUT /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/ipv4-acl/{ipv4AclId}

        :param service_id: Service Profile ID
        :param ipv4_acl_id: IPv4 ACL Feature ID
        :param payload: SD-Routing IPv4 ACL feature from a specific service feature profile
        :returns: EditSdroutingServiceIpv4AclFeaturePutResponse
        """
        params = {
            "serviceId": service_id,
            "ipv4AclId": ipv4_acl_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/ipv4-acl/{ipv4AclId}",
            return_type=EditSdroutingServiceIpv4AclFeaturePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, service_id: str, ipv4_acl_id: str, **kw):
        """
        Delete the SD-Routing IPv4 ACL feature from a specific service feature profile
        DELETE /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/ipv4-acl/{ipv4AclId}

        :param service_id: Service Profile ID
        :param ipv4_acl_id: IPv4 ACL Feature ID
        :returns: None
        """
        params = {
            "serviceId": service_id,
            "ipv4AclId": ipv4_acl_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/ipv4-acl/{ipv4AclId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, service_id: str, ipv4_acl_id: str, **kw
    ) -> GetSingleSdRoutingServiceIpv4AclPayload:
        """
        Get the SD-Routing IPv4 ACL feature from a specific service feature profile
        GET /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/ipv4-acl/{ipv4AclId}

        :param service_id: Service Profile ID
        :param ipv4_acl_id: IPv4 ACL Feature ID
        :returns: GetSingleSdRoutingServiceIpv4AclPayload
        """
        ...

    @overload
    def get(self, service_id: str, **kw) -> GetListSdRoutingServiceIpv4AclPayload:
        """
        Get all SD-Routing IPv4 ACL features from a specific service feature profile
        GET /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/ipv4-acl

        :param service_id: Service Profile ID
        :returns: GetListSdRoutingServiceIpv4AclPayload
        """
        ...

    def get(
        self, service_id: str, ipv4_acl_id: Optional[str] = None, **kw
    ) -> Union[GetListSdRoutingServiceIpv4AclPayload, GetSingleSdRoutingServiceIpv4AclPayload]:
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/ipv4-acl/{ipv4AclId}
        if self._request_adapter.param_checker([(service_id, str), (ipv4_acl_id, str)], []):
            params = {
                "serviceId": service_id,
                "ipv4AclId": ipv4_acl_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/ipv4-acl/{ipv4AclId}",
                return_type=GetSingleSdRoutingServiceIpv4AclPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/ipv4-acl
        if self._request_adapter.param_checker([(service_id, str)], [ipv4_acl_id]):
            params = {
                "serviceId": service_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/ipv4-acl",
                return_type=GetListSdRoutingServiceIpv4AclPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
