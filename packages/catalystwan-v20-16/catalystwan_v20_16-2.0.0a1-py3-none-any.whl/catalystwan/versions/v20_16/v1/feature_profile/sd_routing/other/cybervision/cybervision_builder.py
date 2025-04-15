# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateCybervisionProfileFeatureForOtherPostRequest,
    CreateCybervisionProfileFeatureForOtherPostResponse,
    EditCybervisionProfileFeatureForOtherPutRequest,
    EditCybervisionProfileFeatureForOtherPutResponse,
    GetListSdRoutingOtherCybervisionPayload,
    GetSingleSdRoutingOtherCybervisionPayload,
)


class CybervisionBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/other/{otherId}/cybervision
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, other_id: str, payload: CreateCybervisionProfileFeatureForOtherPostRequest, **kw
    ) -> CreateCybervisionProfileFeatureForOtherPostResponse:
        """
        Create a Cybervision Profile feature for Other feature profile
        POST /dataservice/v1/feature-profile/sd-routing/other/{otherId}/cybervision

        :param other_id: Feature Profile ID
        :param payload: Cybervision Profile feature
        :returns: CreateCybervisionProfileFeatureForOtherPostResponse
        """
        params = {
            "otherId": other_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/other/{otherId}/cybervision",
            return_type=CreateCybervisionProfileFeatureForOtherPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        other_id: str,
        cybervision_id: str,
        payload: EditCybervisionProfileFeatureForOtherPutRequest,
        **kw,
    ) -> EditCybervisionProfileFeatureForOtherPutResponse:
        """
        Update a Cybervision Profile feature for Other feature profile
        PUT /dataservice/v1/feature-profile/sd-routing/other/{otherId}/cybervision/{cybervisionId}

        :param other_id: Feature Profile ID
        :param cybervision_id: Profile feature ID
        :param payload: Cybervision Profile feature
        :returns: EditCybervisionProfileFeatureForOtherPutResponse
        """
        params = {
            "otherId": other_id,
            "cybervisionId": cybervision_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/other/{otherId}/cybervision/{cybervisionId}",
            return_type=EditCybervisionProfileFeatureForOtherPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, other_id: str, cybervision_id: str, **kw):
        """
        Delete a Cybervision Profile feature for Other feature profile
        DELETE /dataservice/v1/feature-profile/sd-routing/other/{otherId}/cybervision/{cybervisionId}

        :param other_id: Feature Profile ID
        :param cybervision_id: Profile feature ID
        :returns: None
        """
        params = {
            "otherId": other_id,
            "cybervisionId": cybervision_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/other/{otherId}/cybervision/{cybervisionId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, other_id: str, cybervision_id: str, **kw
    ) -> GetSingleSdRoutingOtherCybervisionPayload:
        """
        Get Cybervision Profile feature by FeatureId for Other feature profile
        GET /dataservice/v1/feature-profile/sd-routing/other/{otherId}/cybervision/{cybervisionId}

        :param other_id: Feature Profile ID
        :param cybervision_id: Profile feature ID
        :returns: GetSingleSdRoutingOtherCybervisionPayload
        """
        ...

    @overload
    def get(self, other_id: str, **kw) -> GetListSdRoutingOtherCybervisionPayload:
        """
        Get Cybervision Profile feature for Other feature profile
        GET /dataservice/v1/feature-profile/sd-routing/other/{otherId}/cybervision

        :param other_id: Feature Profile ID
        :returns: GetListSdRoutingOtherCybervisionPayload
        """
        ...

    def get(
        self, other_id: str, cybervision_id: Optional[str] = None, **kw
    ) -> Union[GetListSdRoutingOtherCybervisionPayload, GetSingleSdRoutingOtherCybervisionPayload]:
        # /dataservice/v1/feature-profile/sd-routing/other/{otherId}/cybervision/{cybervisionId}
        if self._request_adapter.param_checker([(other_id, str), (cybervision_id, str)], []):
            params = {
                "otherId": other_id,
                "cybervisionId": cybervision_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/other/{otherId}/cybervision/{cybervisionId}",
                return_type=GetSingleSdRoutingOtherCybervisionPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/other/{otherId}/cybervision
        if self._request_adapter.param_checker([(other_id, str)], [cybervision_id]):
            params = {
                "otherId": other_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/other/{otherId}/cybervision",
                return_type=GetListSdRoutingOtherCybervisionPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
