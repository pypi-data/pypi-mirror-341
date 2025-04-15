# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateTransportGlobalVrfAndRoutingOspfParcelAssociationPostRequest,
    CreateTransportGlobalVrfAndRoutingOspfParcelAssociationPostResponse,
    EditTransportGlobalVrfAndRoutingOspfFeatureAssociationPutRequest,
    EditTransportGlobalVrfAndRoutingOspfFeatureAssociationPutResponse,
    GetSingleSdRoutingTransportGlobalVrfRoutingOspfPayload,
    GetTransportVrfAssociatedRoutingOspfFeaturesGetResponse,
)


class OspfBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/routing/ospf
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        transport_id: str,
        vrf_id: str,
        payload: CreateTransportGlobalVrfAndRoutingOspfParcelAssociationPostRequest,
        **kw,
    ) -> CreateTransportGlobalVrfAndRoutingOspfParcelAssociationPostResponse:
        """
        Associate an OSPF feature with the global VRF feature for transport feature profile
        POST /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/routing/ospf

        :param transport_id: Transport Profile ID
        :param vrf_id: Global VRF Profile Parcel ID
        :param payload: New OSPF feature ID
        :returns: CreateTransportGlobalVrfAndRoutingOspfParcelAssociationPostResponse
        """
        params = {
            "transportId": transport_id,
            "vrfId": vrf_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/routing/ospf",
            return_type=CreateTransportGlobalVrfAndRoutingOspfParcelAssociationPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        transport_id: str,
        vrf_id: str,
        ospf_id: str,
        payload: EditTransportGlobalVrfAndRoutingOspfFeatureAssociationPutRequest,
        **kw,
    ) -> EditTransportGlobalVrfAndRoutingOspfFeatureAssociationPutResponse:
        """
        Replace the OSPF feature for the global VRF feature in transport feature profile
        PUT /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/routing/ospf/{ospfId}

        :param transport_id: Transport Profile ID
        :param vrf_id: Profile Parcel ID
        :param ospf_id: Routing OSPF ID
        :param payload: New OSPF Feature ID
        :returns: EditTransportGlobalVrfAndRoutingOspfFeatureAssociationPutResponse
        """
        params = {
            "transportId": transport_id,
            "vrfId": vrf_id,
            "ospfId": ospf_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/routing/ospf/{ospfId}",
            return_type=EditTransportGlobalVrfAndRoutingOspfFeatureAssociationPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, vrf_id: str, ospf_id: str, **kw):
        """
        Delete the global VRF and the OSPF feature association for transport feature profile
        DELETE /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/routing/ospf/{ospfId}

        :param transport_id: Transport Profile ID
        :param vrf_id: Global VRF Feature ID
        :param ospf_id: OSPF Feature ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "vrfId": vrf_id,
            "ospfId": ospf_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/routing/ospf/{ospfId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, vrf_id: str, ospf_id: str, **kw
    ) -> GetSingleSdRoutingTransportGlobalVrfRoutingOspfPayload:
        """
        Get the Global VRF feature associated OSPF feature by ID for transport feature profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/routing/ospf/{ospfId}

        :param transport_id: Transport Profile ID
        :param vrf_id: Global VRF Feature ID
        :param ospf_id: OSPF Feature ID
        :returns: GetSingleSdRoutingTransportGlobalVrfRoutingOspfPayload
        """
        ...

    @overload
    def get(
        self, transport_id: str, vrf_id: str, **kw
    ) -> List[GetTransportVrfAssociatedRoutingOspfFeaturesGetResponse]:
        """
        Get the global VRF associated OSPF features for transport feature profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/routing/ospf

        :param transport_id: Transport Profile ID
        :param vrf_id: Global VRF Feature ID
        :returns: List[GetTransportVrfAssociatedRoutingOspfFeaturesGetResponse]
        """
        ...

    def get(
        self, transport_id: str, vrf_id: str, ospf_id: Optional[str] = None, **kw
    ) -> Union[
        List[GetTransportVrfAssociatedRoutingOspfFeaturesGetResponse],
        GetSingleSdRoutingTransportGlobalVrfRoutingOspfPayload,
    ]:
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/routing/ospf/{ospfId}
        if self._request_adapter.param_checker(
            [(transport_id, str), (vrf_id, str), (ospf_id, str)], []
        ):
            params = {
                "transportId": transport_id,
                "vrfId": vrf_id,
                "ospfId": ospf_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/routing/ospf/{ospfId}",
                return_type=GetSingleSdRoutingTransportGlobalVrfRoutingOspfPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/routing/ospf
        if self._request_adapter.param_checker([(transport_id, str), (vrf_id, str)], [ospf_id]):
            params = {
                "transportId": transport_id,
                "vrfId": vrf_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/routing/ospf",
                return_type=List[GetTransportVrfAssociatedRoutingOspfFeaturesGetResponse],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
