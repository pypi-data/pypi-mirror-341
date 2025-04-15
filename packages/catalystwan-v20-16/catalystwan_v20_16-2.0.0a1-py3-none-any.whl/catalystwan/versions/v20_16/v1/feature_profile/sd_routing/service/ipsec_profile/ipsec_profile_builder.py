# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdroutingServiceIpsecProfileFeaturePostRequest,
    CreateSdroutingServiceIpsecProfileFeaturePostResponse,
    EditSdroutingServiceIpsecProfileFeaturePutRequest,
    EditSdroutingServiceIpsecProfileFeaturePutResponse,
    GetListSdRoutingServiceIpsecProfilePayload,
    GetSingleSdRoutingServiceIpsecProfilePayload,
)


class IpsecProfileBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/service/{serviceId}/ipsec-profile
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, service_id: str, payload: CreateSdroutingServiceIpsecProfileFeaturePostRequest, **kw
    ) -> CreateSdroutingServiceIpsecProfileFeaturePostResponse:
        """
        Create a SD-Routing IPSec profile feature from a specific service feature profile
        POST /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/ipsec-profile

        :param service_id: Service Profile ID
        :param payload: SD-Routing IPSec profile feature from a specific service feature profile
        :returns: CreateSdroutingServiceIpsecProfileFeaturePostResponse
        """
        params = {
            "serviceId": service_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/ipsec-profile",
            return_type=CreateSdroutingServiceIpsecProfileFeaturePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        service_id: str,
        ipsec_profile_id: str,
        payload: EditSdroutingServiceIpsecProfileFeaturePutRequest,
        **kw,
    ) -> EditSdroutingServiceIpsecProfileFeaturePutResponse:
        """
        Edit the SD-Routing IPSec profile feature from a specific service feature profile
        PUT /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/ipsec-profile/{ipsecProfileId}

        :param service_id: Service Profile ID
        :param ipsec_profile_id: IPSec Profile Feature ID
        :param payload: SD-Routing IPSec profile feature from a specific service feature profile
        :returns: EditSdroutingServiceIpsecProfileFeaturePutResponse
        """
        params = {
            "serviceId": service_id,
            "ipsecProfileId": ipsec_profile_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/ipsec-profile/{ipsecProfileId}",
            return_type=EditSdroutingServiceIpsecProfileFeaturePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, service_id: str, ipsec_profile_id: str, **kw):
        """
        Delete the SD-Routing IPSec profile feature from a specific service feature profile
        DELETE /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/ipsec-profile/{ipsecProfileId}

        :param service_id: Service Profile ID
        :param ipsec_profile_id: IPSec Profile Feature ID
        :returns: None
        """
        params = {
            "serviceId": service_id,
            "ipsecProfileId": ipsec_profile_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/ipsec-profile/{ipsecProfileId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, service_id: str, ipsec_profile_id: str, **kw
    ) -> GetSingleSdRoutingServiceIpsecProfilePayload:
        """
        Get the SD-Routing IPSec profile feature from a specific service feature profile
        GET /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/ipsec-profile/{ipsecProfileId}

        :param service_id: Service Profile ID
        :param ipsec_profile_id: IPSec Profile Feature ID
        :returns: GetSingleSdRoutingServiceIpsecProfilePayload
        """
        ...

    @overload
    def get(self, service_id: str, **kw) -> GetListSdRoutingServiceIpsecProfilePayload:
        """
        Get all SD-Routing IPSec profile features from a specific service feature profile
        GET /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/ipsec-profile

        :param service_id: Service Profile ID
        :returns: GetListSdRoutingServiceIpsecProfilePayload
        """
        ...

    def get(
        self, service_id: str, ipsec_profile_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdRoutingServiceIpsecProfilePayload, GetSingleSdRoutingServiceIpsecProfilePayload
    ]:
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/ipsec-profile/{ipsecProfileId}
        if self._request_adapter.param_checker([(service_id, str), (ipsec_profile_id, str)], []):
            params = {
                "serviceId": service_id,
                "ipsecProfileId": ipsec_profile_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/ipsec-profile/{ipsecProfileId}",
                return_type=GetSingleSdRoutingServiceIpsecProfilePayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/ipsec-profile
        if self._request_adapter.param_checker([(service_id, str)], [ipsec_profile_id]):
            params = {
                "serviceId": service_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/ipsec-profile",
                return_type=GetListSdRoutingServiceIpsecProfilePayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
