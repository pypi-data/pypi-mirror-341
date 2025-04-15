# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdroutingServiceVrfOspfv3Ipv6FeaturePostRequest,
    CreateSdroutingServiceVrfOspfv3Ipv6FeaturePostResponse,
    EditSdroutingServiceVrfOspfv3Ipv6FeaturePutRequest,
    EditSdroutingServiceVrfOspfv3Ipv6FeaturePutResponse,
    GetListSdRoutingServiceRoutingOspfv3Ipv6Payload,
    GetSingleSdRoutingServiceRoutingOspfv3Ipv6Payload,
)


class Ipv6Builder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/service/{serviceId}/routing/ospfv3/ipv6
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, service_id: str, payload: CreateSdroutingServiceVrfOspfv3Ipv6FeaturePostRequest, **kw
    ) -> CreateSdroutingServiceVrfOspfv3Ipv6FeaturePostResponse:
        """
        Create a SD-Routing LAN OSPFv3 IPv6 feature from a specific service feature profile
        POST /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/routing/ospfv3/ipv6

        :param service_id: Service Profile ID
        :param payload: SD-Routing LAN OSPFv3 IPv6 feature from a specific service feature profile
        :returns: CreateSdroutingServiceVrfOspfv3Ipv6FeaturePostResponse
        """
        params = {
            "serviceId": service_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/routing/ospfv3/ipv6",
            return_type=CreateSdroutingServiceVrfOspfv3Ipv6FeaturePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        service_id: str,
        ospfv3_id: str,
        payload: EditSdroutingServiceVrfOspfv3Ipv6FeaturePutRequest,
        **kw,
    ) -> EditSdroutingServiceVrfOspfv3Ipv6FeaturePutResponse:
        """
        Edit the SD-Routing LAN OSPFv3 IPv6 feature from a specific service feature profile
        PUT /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/routing/ospfv3/ipv6/{ospfv3Id}

        :param service_id: Service Profile ID
        :param ospfv3_id: OSPFv3 IPv6 Feature ID
        :param payload: SD-Routing LAN OSPFv3 IPv6 feature from a specific service feature profile
        :returns: EditSdroutingServiceVrfOspfv3Ipv6FeaturePutResponse
        """
        params = {
            "serviceId": service_id,
            "ospfv3Id": ospfv3_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/routing/ospfv3/ipv6/{ospfv3Id}",
            return_type=EditSdroutingServiceVrfOspfv3Ipv6FeaturePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, service_id: str, ospfv3_id: str, **kw):
        """
        Delete the SD-Routing LAN OSPFv3 IPv6 feature from a specific service feature profile
        DELETE /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/routing/ospfv3/ipv6/{ospfv3Id}

        :param service_id: Service Profile ID
        :param ospfv3_id: OSPFv3 IPv6 Feature ID
        :returns: None
        """
        params = {
            "serviceId": service_id,
            "ospfv3Id": ospfv3_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/routing/ospfv3/ipv6/{ospfv3Id}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, service_id: str, ospfv3_id: str, **kw
    ) -> GetSingleSdRoutingServiceRoutingOspfv3Ipv6Payload:
        """
        Get the SD-Routing LAN OSPFv3 IPv6 feature from a specific service feature profile
        GET /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/routing/ospfv3/ipv6/{ospfv3Id}

        :param service_id: Service Profile ID
        :param ospfv3_id: OSPFv3 IPv6 Feature ID
        :returns: GetSingleSdRoutingServiceRoutingOspfv3Ipv6Payload
        """
        ...

    @overload
    def get(self, service_id: str, **kw) -> GetListSdRoutingServiceRoutingOspfv3Ipv6Payload:
        """
        Get all SD-Routing LAN OSPFv3 IPv6 features from a specific service feature profile
        GET /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/routing/ospfv3/ipv6

        :param service_id: Service Profile ID
        :returns: GetListSdRoutingServiceRoutingOspfv3Ipv6Payload
        """
        ...

    def get(
        self, service_id: str, ospfv3_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdRoutingServiceRoutingOspfv3Ipv6Payload,
        GetSingleSdRoutingServiceRoutingOspfv3Ipv6Payload,
    ]:
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/routing/ospfv3/ipv6/{ospfv3Id}
        if self._request_adapter.param_checker([(service_id, str), (ospfv3_id, str)], []):
            params = {
                "serviceId": service_id,
                "ospfv3Id": ospfv3_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/routing/ospfv3/ipv6/{ospfv3Id}",
                return_type=GetSingleSdRoutingServiceRoutingOspfv3Ipv6Payload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/routing/ospfv3/ipv6
        if self._request_adapter.param_checker([(service_id, str)], [ospfv3_id]):
            params = {
                "serviceId": service_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/routing/ospfv3/ipv6",
                return_type=GetListSdRoutingServiceRoutingOspfv3Ipv6Payload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
