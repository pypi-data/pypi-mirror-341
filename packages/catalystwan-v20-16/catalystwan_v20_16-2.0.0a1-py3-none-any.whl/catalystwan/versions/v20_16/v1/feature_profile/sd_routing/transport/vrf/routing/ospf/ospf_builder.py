# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateTransportVrfAndRoutingOspfAssociationPostRequest,
    CreateTransportVrfAndRoutingOspfAssociationPostResponse,
    EditTransportVrfAndRoutingOspfFeatureAssociationPutRequest,
    EditTransportVrfAndRoutingOspfFeatureAssociationPutResponse,
    GetSingleSdRoutingTransportVrfRoutingOspfPayload,
    GetTransportVrfAssociatedRoutingOspfFeatures1GetResponse,
)


class OspfBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/routing/ospf
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        transport_id: str,
        vrf_id: str,
        payload: CreateTransportVrfAndRoutingOspfAssociationPostRequest,
        **kw,
    ) -> CreateTransportVrfAndRoutingOspfAssociationPostResponse:
        """
        Associate an OSPF feature with the WAN VRF feature for transport feature profile
        POST /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/routing/ospf

        :param transport_id: Transport Profile ID
        :param vrf_id: VRF Feature ID
        :param payload: OSPF feature ID
        :returns: CreateTransportVrfAndRoutingOspfAssociationPostResponse
        """
        params = {
            "transportId": transport_id,
            "vrfId": vrf_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/routing/ospf",
            return_type=CreateTransportVrfAndRoutingOspfAssociationPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        transport_id: str,
        vrf_id: str,
        ospf_id: str,
        payload: EditTransportVrfAndRoutingOspfFeatureAssociationPutRequest,
        **kw,
    ) -> EditTransportVrfAndRoutingOspfFeatureAssociationPutResponse:
        """
        Replace the OSPF feature for the WAN VRF feature in transport feature profile
        PUT /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/routing/ospf/{ospfId}

        :param transport_id: Transport Profile ID
        :param vrf_id: VRF Feature ID
        :param ospf_id: Old OSPF Feature ID
        :param payload: New OSPF Feature ID
        :returns: EditTransportVrfAndRoutingOspfFeatureAssociationPutResponse
        """
        params = {
            "transportId": transport_id,
            "vrfId": vrf_id,
            "ospfId": ospf_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/routing/ospf/{ospfId}",
            return_type=EditTransportVrfAndRoutingOspfFeatureAssociationPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, vrf_id: str, ospf_id: str, **kw):
        """
        Delete the VRF and OSPF feature association for transport feature profile
        DELETE /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/routing/ospf/{ospfId}

        :param transport_id: Transport Profile ID
        :param vrf_id: VRF Feature ID
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
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/routing/ospf/{ospfId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, vrf_id: str, ospf_id: str, **kw
    ) -> GetSingleSdRoutingTransportVrfRoutingOspfPayload:
        """
        Get the WAN VRF associated OSPF features by feature ID for transport feature profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/routing/ospf/{ospfId}

        :param transport_id: Transport Profile ID
        :param vrf_id: VRF Feature ID
        :param ospf_id: OSPF Feature ID
        :returns: GetSingleSdRoutingTransportVrfRoutingOspfPayload
        """
        ...

    @overload
    def get(
        self, transport_id: str, vrf_id: str, **kw
    ) -> List[GetTransportVrfAssociatedRoutingOspfFeatures1GetResponse]:
        """
        Get the WAN VRF associated OSPF features for transport feature profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/routing/ospf

        :param transport_id: Transport Profile ID
        :param vrf_id: VRF Feature ID
        :returns: List[GetTransportVrfAssociatedRoutingOspfFeatures1GetResponse]
        """
        ...

    def get(
        self, transport_id: str, vrf_id: str, ospf_id: Optional[str] = None, **kw
    ) -> Union[
        List[GetTransportVrfAssociatedRoutingOspfFeatures1GetResponse],
        GetSingleSdRoutingTransportVrfRoutingOspfPayload,
    ]:
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/routing/ospf/{ospfId}
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
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/routing/ospf/{ospfId}",
                return_type=GetSingleSdRoutingTransportVrfRoutingOspfPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/routing/ospf
        if self._request_adapter.param_checker([(transport_id, str), (vrf_id, str)], [ospf_id]):
            params = {
                "transportId": transport_id,
                "vrfId": vrf_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/routing/ospf",
                return_type=List[GetTransportVrfAssociatedRoutingOspfFeatures1GetResponse],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
