# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateEmbeddedSecurityFeaturePostRequest,
    CreateEmbeddedSecurityFeaturePostResponse,
    EditSecurityFeaturePutRequest,
    EditSecurityFeaturePutResponse,
    GetListSdRoutingEmbeddedSecurityPolicyPayload,
    GetSingleSdRoutingEmbeddedSecurityPolicyPayload,
)


class PolicyBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/embedded-security/{securityId}/policy
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, security_id: str, payload: CreateEmbeddedSecurityFeaturePostRequest, **kw
    ) -> CreateEmbeddedSecurityFeaturePostResponse:
        """
        Create Feature for Security Policy
        POST /dataservice/v1/feature-profile/sd-routing/embedded-security/{securityId}/policy

        :param security_id: Feature Profile ID
        :param payload: Security Feature
        :returns: CreateEmbeddedSecurityFeaturePostResponse
        """
        params = {
            "securityId": security_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/embedded-security/{securityId}/policy",
            return_type=CreateEmbeddedSecurityFeaturePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        security_id: str,
        security_profile_parcel_id: str,
        payload: EditSecurityFeaturePutRequest,
        **kw,
    ) -> EditSecurityFeaturePutResponse:
        """
        Update a Security Feature
        PUT /dataservice/v1/feature-profile/sd-routing/embedded-security/{securityId}/policy/{securityProfileParcelId}

        :param security_id: Feature Profile ID
        :param security_profile_parcel_id: Feature ID
        :param payload: Security Feature
        :returns: EditSecurityFeaturePutResponse
        """
        params = {
            "securityId": security_id,
            "securityProfileParcelId": security_profile_parcel_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/embedded-security/{securityId}/policy/{securityProfileParcelId}",
            return_type=EditSecurityFeaturePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, security_id: str, security_profile_parcel_id: str, **kw):
        """
        Delete a Security Feature
        DELETE /dataservice/v1/feature-profile/sd-routing/embedded-security/{securityId}/policy/{securityProfileParcelId}

        :param security_id: Feature Profile ID
        :param security_profile_parcel_id: Feature ID
        :returns: None
        """
        params = {
            "securityId": security_id,
            "securityProfileParcelId": security_profile_parcel_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/embedded-security/{securityId}/policy/{securityProfileParcelId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, security_id: str, security_profile_parcel_id: str, **kw
    ) -> GetSingleSdRoutingEmbeddedSecurityPolicyPayload:
        """
        Get Security Feature by FeatureId
        GET /dataservice/v1/feature-profile/sd-routing/embedded-security/{securityId}/policy/{securityProfileParcelId}

        :param security_id: Feature Profile ID
        :param security_profile_parcel_id: Feature ID
        :returns: GetSingleSdRoutingEmbeddedSecurityPolicyPayload
        """
        ...

    @overload
    def get(self, security_id: str, **kw) -> GetListSdRoutingEmbeddedSecurityPolicyPayload:
        """
        Get Security Features for a given FeatureType
        GET /dataservice/v1/feature-profile/sd-routing/embedded-security/{securityId}/policy

        :param security_id: Feature Profile ID
        :returns: GetListSdRoutingEmbeddedSecurityPolicyPayload
        """
        ...

    def get(
        self, security_id: str, security_profile_parcel_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdRoutingEmbeddedSecurityPolicyPayload,
        GetSingleSdRoutingEmbeddedSecurityPolicyPayload,
    ]:
        # /dataservice/v1/feature-profile/sd-routing/embedded-security/{securityId}/policy/{securityProfileParcelId}
        if self._request_adapter.param_checker(
            [(security_id, str), (security_profile_parcel_id, str)], []
        ):
            params = {
                "securityId": security_id,
                "securityProfileParcelId": security_profile_parcel_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/embedded-security/{securityId}/policy/{securityProfileParcelId}",
                return_type=GetSingleSdRoutingEmbeddedSecurityPolicyPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/embedded-security/{securityId}/policy
        if self._request_adapter.param_checker([(security_id, str)], [security_profile_parcel_id]):
            params = {
                "securityId": security_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/embedded-security/{securityId}/policy",
                return_type=GetListSdRoutingEmbeddedSecurityPolicyPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
