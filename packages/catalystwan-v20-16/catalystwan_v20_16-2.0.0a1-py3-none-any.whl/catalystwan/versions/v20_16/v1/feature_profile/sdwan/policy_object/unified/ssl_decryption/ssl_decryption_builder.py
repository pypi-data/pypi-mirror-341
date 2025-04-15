# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdwanSecurityFeaturePostRequest1,
    CreateSdwanSecurityFeaturePostRequest2,
    CreateSdwanSecurityFeaturePostResponse,
    GetSdwanSecurityFeatureGetResponse,
)


class SslDecryptionBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/policy-object/{policyObjectId}/unified/ssl-decryption
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        policy_object_id: str,
        payload: Union[
            CreateSdwanSecurityFeaturePostRequest1, CreateSdwanSecurityFeaturePostRequest2
        ],
        **kw,
    ) -> CreateSdwanSecurityFeaturePostResponse:
        """
        Create Feature for Security Policy
        POST /dataservice/v1/feature-profile/sdwan/policy-object/{policyObjectId}/unified/ssl-decryption

        :param policy_object_id: Feature Profile ID
        :param payload: Security Feature
        :returns: CreateSdwanSecurityFeaturePostResponse
        """
        params = {
            "policyObjectId": policy_object_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/policy-object/{policyObjectId}/unified/ssl-decryption",
            return_type=CreateSdwanSecurityFeaturePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def get(
        self, policy_object_id: str, parcel_id: str, reference_count: Optional[bool] = False, **kw
    ) -> GetSdwanSecurityFeatureGetResponse:
        """
        Get Security Features for a given ParcelType
        GET /dataservice/v1/feature-profile/sdwan/policy-object/{policyObjectId}/unified/ssl-decryption/{parcelId}

        :param policy_object_id: Feature Profile ID
        :param reference_count: get reference count
        :param parcel_id: Parcel ID
        :returns: GetSdwanSecurityFeatureGetResponse
        """
        params = {
            "policyObjectId": policy_object_id,
            "referenceCount": reference_count,
            "parcelId": parcel_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/v1/feature-profile/sdwan/policy-object/{policyObjectId}/unified/ssl-decryption/{parcelId}",
            return_type=GetSdwanSecurityFeatureGetResponse,
            params=params,
            **kw,
        )
