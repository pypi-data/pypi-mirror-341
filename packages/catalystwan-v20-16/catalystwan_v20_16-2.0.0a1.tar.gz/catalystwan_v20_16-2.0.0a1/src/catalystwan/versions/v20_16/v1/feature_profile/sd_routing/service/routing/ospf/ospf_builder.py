# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdroutingServiceVrfOspfFeaturePostRequest,
    CreateSdroutingServiceVrfOspfFeaturePostResponse,
    EditSdroutingServiceVrfOspfFeaturePutRequest,
    EditSdroutingServiceVrfOspfFeaturePutResponse,
    GetListSdRoutingServiceRoutingOspfPayload,
    GetSingleSdRoutingServiceRoutingOspfPayload,
)


class OspfBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/service/{serviceId}/routing/ospf
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, service_id: str, payload: CreateSdroutingServiceVrfOspfFeaturePostRequest, **kw
    ) -> CreateSdroutingServiceVrfOspfFeaturePostResponse:
        """
        Create a SD-Routing LAN OSPF feature for service VRF from a specific service feature profile
        POST /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/routing/ospf

        :param service_id: Service Profile ID
        :param payload: SD-Routing LAN OSPF feature for service VRF from a specific service feature profile
        :returns: CreateSdroutingServiceVrfOspfFeaturePostResponse
        """
        params = {
            "serviceId": service_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/routing/ospf",
            return_type=CreateSdroutingServiceVrfOspfFeaturePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        service_id: str,
        ospf_id: str,
        payload: EditSdroutingServiceVrfOspfFeaturePutRequest,
        **kw,
    ) -> EditSdroutingServiceVrfOspfFeaturePutResponse:
        """
        Edit the SD-Routing LAN OSPF feature for service VRF from a specific service feature profile
        PUT /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/routing/ospf/{ospfId}

        :param service_id: Service Profile ID
        :param ospf_id: OSPF Feature ID
        :param payload: SD-Routing LAN OSPF feature for service VRF from a specific service feature profile
        :returns: EditSdroutingServiceVrfOspfFeaturePutResponse
        """
        params = {
            "serviceId": service_id,
            "ospfId": ospf_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/routing/ospf/{ospfId}",
            return_type=EditSdroutingServiceVrfOspfFeaturePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, service_id: str, ospf_id: str, **kw):
        """
        Delete the SD-Routing LAN OSPF feature for service VRF from a specific service feature profile
        DELETE /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/routing/ospf/{ospfId}

        :param service_id: Service Profile ID
        :param ospf_id: OSPF Feature ID
        :returns: None
        """
        params = {
            "serviceId": service_id,
            "ospfId": ospf_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/routing/ospf/{ospfId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, service_id: str, ospf_id: str, **kw
    ) -> GetSingleSdRoutingServiceRoutingOspfPayload:
        """
        Get the SD-Routing LAN OSPF feature for service VRF from a specific service feature profile
        GET /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/routing/ospf/{ospfId}

        :param service_id: Service Profile ID
        :param ospf_id: OSPF Feature ID
        :returns: GetSingleSdRoutingServiceRoutingOspfPayload
        """
        ...

    @overload
    def get(self, service_id: str, **kw) -> GetListSdRoutingServiceRoutingOspfPayload:
        """
        Get all SD-Routing LAN OSPF features for service VRF from a specific service feature profile
        GET /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/routing/ospf

        :param service_id: Service Profile ID
        :returns: GetListSdRoutingServiceRoutingOspfPayload
        """
        ...

    def get(
        self, service_id: str, ospf_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdRoutingServiceRoutingOspfPayload, GetSingleSdRoutingServiceRoutingOspfPayload
    ]:
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/routing/ospf/{ospfId}
        if self._request_adapter.param_checker([(service_id, str), (ospf_id, str)], []):
            params = {
                "serviceId": service_id,
                "ospfId": ospf_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/routing/ospf/{ospfId}",
                return_type=GetSingleSdRoutingServiceRoutingOspfPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/routing/ospf
        if self._request_adapter.param_checker([(service_id, str)], [ospf_id]):
            params = {
                "serviceId": service_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/routing/ospf",
                return_type=GetListSdRoutingServiceRoutingOspfPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
