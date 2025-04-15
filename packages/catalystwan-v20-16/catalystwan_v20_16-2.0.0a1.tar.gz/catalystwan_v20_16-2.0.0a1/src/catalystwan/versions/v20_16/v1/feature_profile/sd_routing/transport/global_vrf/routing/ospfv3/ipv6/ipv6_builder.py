# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateTransportGlobalVrfAndRoutingOspfv3Ipv6ParcelAssociationPostRequest,
    CreateTransportGlobalVrfAndRoutingOspfv3Ipv6ParcelAssociationPostResponse,
    EditTransportGlobalVrfAndRoutingOspfv3Ipv6FeatureAssociationPutRequest,
    EditTransportGlobalVrfAndRoutingOspfv3Ipv6FeatureAssociationPutResponse,
    GetSingleSdRoutingTransportGlobalVrfRoutingOspfv3Ipv6Payload,
    GetTransportVrfAssociatedRoutingOspfv3Ipv6FeaturesGetResponse,
)


class Ipv6Builder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/routing/ospfv3/ipv6
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        transport_id: str,
        vrf_id: str,
        payload: CreateTransportGlobalVrfAndRoutingOspfv3Ipv6ParcelAssociationPostRequest,
        **kw,
    ) -> CreateTransportGlobalVrfAndRoutingOspfv3Ipv6ParcelAssociationPostResponse:
        """
        Associate an OSPFv3 IPv6 feature with the global VRF feature for transport feature profile
        POST /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/routing/ospfv3/ipv6

        :param transport_id: Transport Profile ID
        :param vrf_id: Global VRF Feature ID
        :param payload: New OSPFv3 IPv6 feature ID
        :returns: CreateTransportGlobalVrfAndRoutingOspfv3Ipv6ParcelAssociationPostResponse
        """
        params = {
            "transportId": transport_id,
            "vrfId": vrf_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/routing/ospfv3/ipv6",
            return_type=CreateTransportGlobalVrfAndRoutingOspfv3Ipv6ParcelAssociationPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        transport_id: str,
        vrf_id: str,
        ospfv3_id: str,
        payload: EditTransportGlobalVrfAndRoutingOspfv3Ipv6FeatureAssociationPutRequest,
        **kw,
    ) -> EditTransportGlobalVrfAndRoutingOspfv3Ipv6FeatureAssociationPutResponse:
        """
        Replace the OSPFv3 IPv6 feature for the global VRF feature in transport feature profile
        PUT /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/routing/ospfv3/ipv6/{ospfv3Id}

        :param transport_id: Transport Profile ID
        :param vrf_id: Global VRF Feature ID
        :param ospfv3_id: Old OSPFv3 IPv6 Feature ID
        :param payload: New OSPFv3 IPv6 Feature ID
        :returns: EditTransportGlobalVrfAndRoutingOspfv3Ipv6FeatureAssociationPutResponse
        """
        params = {
            "transportId": transport_id,
            "vrfId": vrf_id,
            "ospfv3Id": ospfv3_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/routing/ospfv3/ipv6/{ospfv3Id}",
            return_type=EditTransportGlobalVrfAndRoutingOspfv3Ipv6FeatureAssociationPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, vrf_id: str, ospfv3_id: str, **kw):
        """
        Delete the global VRF feature and the OSPFv3 IPv6 feature association for transport feature profile
        DELETE /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/routing/ospfv3/ipv6/{ospfv3Id}

        :param transport_id: Transport Profile ID
        :param vrf_id: Global VRF Parcel ID
        :param ospfv3_id: OSPFv3 IPv6 Feature ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "vrfId": vrf_id,
            "ospfv3Id": ospfv3_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/routing/ospfv3/ipv6/{ospfv3Id}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, vrf_id: str, ospfv3_id: str, **kw
    ) -> GetSingleSdRoutingTransportGlobalVrfRoutingOspfv3Ipv6Payload:
        """
        Get the Global VRF associated OSPFv3 IPv6 feature by ID for transport feature profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/routing/ospfv3/ipv6/{ospfv3Id}

        :param transport_id: Transport Profile ID
        :param vrf_id: Global VRF Parcel ID
        :param ospfv3_id: OSPFv3 IPv6 Feature ID
        :returns: GetSingleSdRoutingTransportGlobalVrfRoutingOspfv3Ipv6Payload
        """
        ...

    @overload
    def get(
        self, transport_id: str, vrf_id: str, **kw
    ) -> List[GetTransportVrfAssociatedRoutingOspfv3Ipv6FeaturesGetResponse]:
        """
        Get the global VRF associated OSPFv3 IPv6 features for transport feature profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/routing/ospfv3/ipv6

        :param transport_id: Transport Profile ID
        :param vrf_id: Global VRF Parcel ID
        :returns: List[GetTransportVrfAssociatedRoutingOspfv3Ipv6FeaturesGetResponse]
        """
        ...

    def get(
        self, transport_id: str, vrf_id: str, ospfv3_id: Optional[str] = None, **kw
    ) -> Union[
        List[GetTransportVrfAssociatedRoutingOspfv3Ipv6FeaturesGetResponse],
        GetSingleSdRoutingTransportGlobalVrfRoutingOspfv3Ipv6Payload,
    ]:
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/routing/ospfv3/ipv6/{ospfv3Id}
        if self._request_adapter.param_checker(
            [(transport_id, str), (vrf_id, str), (ospfv3_id, str)], []
        ):
            params = {
                "transportId": transport_id,
                "vrfId": vrf_id,
                "ospfv3Id": ospfv3_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/routing/ospfv3/ipv6/{ospfv3Id}",
                return_type=GetSingleSdRoutingTransportGlobalVrfRoutingOspfv3Ipv6Payload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/routing/ospfv3/ipv6
        if self._request_adapter.param_checker([(transport_id, str), (vrf_id, str)], [ospfv3_id]):
            params = {
                "transportId": transport_id,
                "vrfId": vrf_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/routing/ospfv3/ipv6",
                return_type=List[GetTransportVrfAssociatedRoutingOspfv3Ipv6FeaturesGetResponse],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
