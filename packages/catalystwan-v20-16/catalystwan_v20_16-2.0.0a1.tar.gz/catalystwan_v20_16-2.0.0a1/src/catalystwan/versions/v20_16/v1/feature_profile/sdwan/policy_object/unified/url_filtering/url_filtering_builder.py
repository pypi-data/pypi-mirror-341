# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdwanSecurityFeaturePostRequest11,
    CreateSdwanSecurityFeaturePostRequest12,
    CreateSdwanSecurityFeaturePostRequest21,
    CreateSdwanSecurityFeaturePostRequest22,
    CreateSdwanSecurityFeaturePostRequest31,
    CreateSdwanSecurityFeaturePostRequest32,
    CreateSdwanSecurityFeaturePostRequest41,
    CreateSdwanSecurityFeaturePostRequest42,
    CreateSdwanSecurityFeaturePostRequest51,
    CreateSdwanSecurityFeaturePostRequest52,
    CreateSdwanSecurityFeaturePostRequest61,
    CreateSdwanSecurityFeaturePostRequest62,
    CreateSdwanSecurityFeaturePostRequest71,
    CreateSdwanSecurityFeaturePostRequest72,
    CreateSdwanSecurityFeaturePostResponse,
    GetSdwanSecurityFeatureGetResponse,
)


class UrlFilteringBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/policy-object/{policyObjectId}/unified/url-filtering
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        policy_object_id: str,
        payload: Union[
            Union[CreateSdwanSecurityFeaturePostRequest11, CreateSdwanSecurityFeaturePostRequest12],
            Union[CreateSdwanSecurityFeaturePostRequest21, CreateSdwanSecurityFeaturePostRequest22],
            Union[CreateSdwanSecurityFeaturePostRequest31, CreateSdwanSecurityFeaturePostRequest32],
            Union[CreateSdwanSecurityFeaturePostRequest41, CreateSdwanSecurityFeaturePostRequest42],
            Union[CreateSdwanSecurityFeaturePostRequest51, CreateSdwanSecurityFeaturePostRequest52],
            Union[CreateSdwanSecurityFeaturePostRequest61, CreateSdwanSecurityFeaturePostRequest62],
            Union[CreateSdwanSecurityFeaturePostRequest71, CreateSdwanSecurityFeaturePostRequest72],
        ],
        **kw,
    ) -> CreateSdwanSecurityFeaturePostResponse:
        """
        Create Feature for Security Policy
        POST /dataservice/v1/feature-profile/sdwan/policy-object/{policyObjectId}/unified/url-filtering

        :param policy_object_id: Feature Profile ID
        :param payload: Security Feature
        :returns: CreateSdwanSecurityFeaturePostResponse
        """
        params = {
            "policyObjectId": policy_object_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/policy-object/{policyObjectId}/unified/url-filtering",
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
        GET /dataservice/v1/feature-profile/sdwan/policy-object/{policyObjectId}/unified/url-filtering/{parcelId}

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
            "/dataservice/v1/feature-profile/sdwan/policy-object/{policyObjectId}/unified/url-filtering/{parcelId}",
            return_type=GetSdwanSecurityFeatureGetResponse,
            params=params,
            **kw,
        )
