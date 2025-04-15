# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateServiceVrfAndRoutingOspfv3Ipv6FeatureAssociationPostRequest,
    CreateServiceVrfAndRoutingOspfv3Ipv6FeatureAssociationPostResponse,
    EditServiceVrfAndRoutingOspfv3Ipv6FeatureAssociationPutRequest,
    EditServiceVrfAndRoutingOspfv3Ipv6FeatureAssociationPutResponse,
    GetServiceVrfAssociatedRoutingOspfv3Ipv6ParcelsGetResponse,
    GetSingleSdRoutingServiceVrfRoutingOspfv3Ipv6Payload,
)


class Ipv6Builder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/ospfv3/ipv6
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        service_id: str,
        vrf_id: str,
        payload: CreateServiceVrfAndRoutingOspfv3Ipv6FeatureAssociationPostRequest,
        **kw,
    ) -> CreateServiceVrfAndRoutingOspfv3Ipv6FeatureAssociationPostResponse:
        """
        Associate an OSPFv3 IPv6 feature with the LAN VRF feature for service feature profile
        POST /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/ospfv3/ipv6

        :param service_id: Service Profile ID
        :param vrf_id: VRF Feature ID
        :param payload: New OSPFv3 IPv6 Feature ID
        :returns: CreateServiceVrfAndRoutingOspfv3Ipv6FeatureAssociationPostResponse
        """
        params = {
            "serviceId": service_id,
            "vrfId": vrf_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/ospfv3/ipv6",
            return_type=CreateServiceVrfAndRoutingOspfv3Ipv6FeatureAssociationPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        service_id: str,
        vrf_id: str,
        ospfv3_id: str,
        payload: EditServiceVrfAndRoutingOspfv3Ipv6FeatureAssociationPutRequest,
        **kw,
    ) -> EditServiceVrfAndRoutingOspfv3Ipv6FeatureAssociationPutResponse:
        """
        Replace the OSPFv3 IPv6 feature for LAN VRF feature in service feature profile
        PUT /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/ospfv3/ipv6/{ospfv3Id}

        :param service_id: Service Profile ID
        :param vrf_id: VRF Feature ID
        :param ospfv3_id: Old OSPFv3 IPv6 Feature ID
        :param payload: New OSPFv3 IPv6 feature ID
        :returns: EditServiceVrfAndRoutingOspfv3Ipv6FeatureAssociationPutResponse
        """
        params = {
            "serviceId": service_id,
            "vrfId": vrf_id,
            "ospfv3Id": ospfv3_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/ospfv3/ipv6/{ospfv3Id}",
            return_type=EditServiceVrfAndRoutingOspfv3Ipv6FeatureAssociationPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, service_id: str, vrf_id: str, ospfv3_id: str, **kw):
        """
        Delete the VRF feature and OSPFv3 IPv6 feature association for service feature profile
        DELETE /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/ospfv3/ipv6/{ospfv3Id}

        :param service_id: Service Profile ID
        :param vrf_id: VRF Feature ID
        :param ospfv3_id: OSPFv3 IPv6 Feature ID
        :returns: None
        """
        params = {
            "serviceId": service_id,
            "vrfId": vrf_id,
            "ospfv3Id": ospfv3_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/ospfv3/ipv6/{ospfv3Id}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, service_id: str, vrf_id: str, ospfv3_id: str, **kw
    ) -> GetSingleSdRoutingServiceVrfRoutingOspfv3Ipv6Payload:
        """
        Get LAN VRF associated OSPFv3 IPv6 feature by feature ID for service feature profile
        GET /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/ospfv3/ipv6/{ospfv3Id}

        :param service_id: Service Profile ID
        :param vrf_id: VRF Feature ID
        :param ospfv3_id: OSPFv3 IPv6 Feature ID
        :returns: GetSingleSdRoutingServiceVrfRoutingOspfv3Ipv6Payload
        """
        ...

    @overload
    def get(
        self, service_id: str, vrf_id: str, **kw
    ) -> List[GetServiceVrfAssociatedRoutingOspfv3Ipv6ParcelsGetResponse]:
        """
        Get the LAN VRF associated OSPFv3 IPv6 features for service feature profile
        GET /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/ospfv3/ipv6

        :param service_id: Service Profile ID
        :param vrf_id: VRF Feature ID
        :returns: List[GetServiceVrfAssociatedRoutingOspfv3Ipv6ParcelsGetResponse]
        """
        ...

    def get(
        self, service_id: str, vrf_id: str, ospfv3_id: Optional[str] = None, **kw
    ) -> Union[
        List[GetServiceVrfAssociatedRoutingOspfv3Ipv6ParcelsGetResponse],
        GetSingleSdRoutingServiceVrfRoutingOspfv3Ipv6Payload,
    ]:
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/ospfv3/ipv6/{ospfv3Id}
        if self._request_adapter.param_checker(
            [(service_id, str), (vrf_id, str), (ospfv3_id, str)], []
        ):
            params = {
                "serviceId": service_id,
                "vrfId": vrf_id,
                "ospfv3Id": ospfv3_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/ospfv3/ipv6/{ospfv3Id}",
                return_type=GetSingleSdRoutingServiceVrfRoutingOspfv3Ipv6Payload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/ospfv3/ipv6
        if self._request_adapter.param_checker([(service_id, str), (vrf_id, str)], [ospfv3_id]):
            params = {
                "serviceId": service_id,
                "vrfId": vrf_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/ospfv3/ipv6",
                return_type=List[GetServiceVrfAssociatedRoutingOspfv3Ipv6ParcelsGetResponse],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
