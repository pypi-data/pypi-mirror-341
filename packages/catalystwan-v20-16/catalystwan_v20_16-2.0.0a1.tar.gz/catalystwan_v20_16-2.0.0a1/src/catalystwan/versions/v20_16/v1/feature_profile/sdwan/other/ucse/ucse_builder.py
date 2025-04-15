# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateUcseProfileFeatureForOtherPostRequest,
    CreateUcseProfileFeatureForOtherPostResponse,
    EditUcseProfileFeatureForOtherPutRequest,
    EditUcseProfileFeatureForOtherPutResponse,
    GetListSdwanOtherUcsePayload,
    GetSingleSdwanOtherUcsePayload,
)


class UcseBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/other/{otherId}/ucse
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, other_id: str, payload: CreateUcseProfileFeatureForOtherPostRequest, **kw
    ) -> CreateUcseProfileFeatureForOtherPostResponse:
        """
        Create a Ucse Profile feature for Other feature profile
        POST /dataservice/v1/feature-profile/sdwan/other/{otherId}/ucse

        :param other_id: Feature Profile ID
        :param payload: Ucse Profile feature
        :returns: CreateUcseProfileFeatureForOtherPostResponse
        """
        params = {
            "otherId": other_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/other/{otherId}/ucse",
            return_type=CreateUcseProfileFeatureForOtherPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self, other_id: str, ucse_id: str, payload: EditUcseProfileFeatureForOtherPutRequest, **kw
    ) -> EditUcseProfileFeatureForOtherPutResponse:
        """
        Update a Ucse Profile feature for Other feature profile
        PUT /dataservice/v1/feature-profile/sdwan/other/{otherId}/ucse/{ucseId}

        :param other_id: Feature Profile ID
        :param ucse_id: Profile feature ID
        :param payload: Ucse Profile feature
        :returns: EditUcseProfileFeatureForOtherPutResponse
        """
        params = {
            "otherId": other_id,
            "ucseId": ucse_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/other/{otherId}/ucse/{ucseId}",
            return_type=EditUcseProfileFeatureForOtherPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, other_id: str, ucse_id: str, **kw):
        """
        Delete a Ucse Profile feature for Other feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/other/{otherId}/ucse/{ucseId}

        :param other_id: Feature Profile ID
        :param ucse_id: Profile feature ID
        :returns: None
        """
        params = {
            "otherId": other_id,
            "ucseId": ucse_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/other/{otherId}/ucse/{ucseId}",
            params=params,
            **kw,
        )

    @overload
    def get(self, other_id: str, ucse_id: str, **kw) -> GetSingleSdwanOtherUcsePayload:
        """
        Get Ucse Profile feature by FeatureId for Other feature profile
        GET /dataservice/v1/feature-profile/sdwan/other/{otherId}/ucse/{ucseId}

        :param other_id: Feature Profile ID
        :param ucse_id: Profile feature ID
        :returns: GetSingleSdwanOtherUcsePayload
        """
        ...

    @overload
    def get(self, other_id: str, **kw) -> GetListSdwanOtherUcsePayload:
        """
        Get Ucse Profile feature for Other feature profile
        GET /dataservice/v1/feature-profile/sdwan/other/{otherId}/ucse

        :param other_id: Feature Profile ID
        :returns: GetListSdwanOtherUcsePayload
        """
        ...

    def get(
        self, other_id: str, ucse_id: Optional[str] = None, **kw
    ) -> Union[GetListSdwanOtherUcsePayload, GetSingleSdwanOtherUcsePayload]:
        # /dataservice/v1/feature-profile/sdwan/other/{otherId}/ucse/{ucseId}
        if self._request_adapter.param_checker([(other_id, str), (ucse_id, str)], []):
            params = {
                "otherId": other_id,
                "ucseId": ucse_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/other/{otherId}/ucse/{ucseId}",
                return_type=GetSingleSdwanOtherUcsePayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/other/{otherId}/ucse
        if self._request_adapter.param_checker([(other_id, str)], [ucse_id]):
            params = {
                "otherId": other_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/other/{otherId}/ucse",
                return_type=GetListSdwanOtherUcsePayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
