# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdroutingTransportGlobalVrfBgpFeaturePostRequest,
    CreateSdroutingTransportGlobalVrfBgpFeaturePostResponse,
    CreateTransportGlobalVrfAndRoutingBgpFeatureAssociationPostRequest,
    CreateTransportGlobalVrfAndRoutingBgpFeatureAssociationPostResponse,
    EditSdroutingTransportGlobalVrfBgpFeaturePutRequest,
    EditSdroutingTransportGlobalVrfBgpFeaturePutResponse,
    EditTransportGlobalVrfAndRoutingBgpFeatureAssociationPutRequest,
    EditTransportGlobalVrfAndRoutingBgpFeatureAssociationPutResponse,
    GetListSdRoutingTransportGlobalVrfRoutingBgpPayload,
    GetSingleSdRoutingTransportGlobalVrfGlobalVrfRoutingBgpPayload,
    GetSingleSdRoutingTransportGlobalVrfRoutingBgpPayload,
    GetTransportVrfAssociatedRoutingBgpFeaturesGetResponse,
)


class BgpBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/routing/bgp
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @overload
    def get(
        self, *, transport_id: str, vrf_id: str, bgp_id: str, **kw
    ) -> GetSingleSdRoutingTransportGlobalVrfGlobalVrfRoutingBgpPayload:
        """
        Get Global VRF parcel associated BGP feature by ID for transport feature profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/routing/bgp/{bgpId}

        :param transport_id: Transport Profile ID
        :param vrf_id: Global VRF Feature ID
        :param bgp_id: BGP Feature ID
        :returns: GetSingleSdRoutingTransportGlobalVrfGlobalVrfRoutingBgpPayload
        """
        ...

    @overload
    def get(
        self, *, transport_id: str, bgp_id: str, **kw
    ) -> GetSingleSdRoutingTransportGlobalVrfRoutingBgpPayload:
        """
        Get the SD-Routing WAN BGP feature for global VRF from a specific transport feature profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/routing/bgp/{bgpId}

        :param transport_id: Transport Profile ID
        :param bgp_id: BGP Feature ID
        :returns: GetSingleSdRoutingTransportGlobalVrfRoutingBgpPayload
        """
        ...

    @overload
    def get(
        self, *, transport_id: str, vrf_id: str, **kw
    ) -> List[GetTransportVrfAssociatedRoutingBgpFeaturesGetResponse]:
        """
        Get the global VRF associated BGP features for transport feature profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/routing/bgp

        :param transport_id: Transport Profile ID
        :param vrf_id: Global VRF Feature ID
        :returns: List[GetTransportVrfAssociatedRoutingBgpFeaturesGetResponse]
        """
        ...

    @overload
    def get(
        self, *, transport_id: str, **kw
    ) -> GetListSdRoutingTransportGlobalVrfRoutingBgpPayload:
        """
        Get all SD-Routing WAN BGP features for global VRF from a specific transport feature profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/routing/bgp

        :param transport_id: Transport Profile ID
        :returns: GetListSdRoutingTransportGlobalVrfRoutingBgpPayload
        """
        ...

    def get(
        self, *, transport_id: str, bgp_id: Optional[str] = None, vrf_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdRoutingTransportGlobalVrfRoutingBgpPayload,
        GetSingleSdRoutingTransportGlobalVrfRoutingBgpPayload,
        List[GetTransportVrfAssociatedRoutingBgpFeaturesGetResponse],
        GetSingleSdRoutingTransportGlobalVrfGlobalVrfRoutingBgpPayload,
    ]:
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/routing/bgp/{bgpId}
        if self._request_adapter.param_checker(
            [(transport_id, str), (vrf_id, str), (bgp_id, str)], []
        ):
            params = {
                "transportId": transport_id,
                "vrfId": vrf_id,
                "bgpId": bgp_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/routing/bgp/{bgpId}",
                return_type=GetSingleSdRoutingTransportGlobalVrfGlobalVrfRoutingBgpPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/routing/bgp/{bgpId}
        if self._request_adapter.param_checker([(transport_id, str), (bgp_id, str)], [vrf_id]):
            params = {
                "transportId": transport_id,
                "bgpId": bgp_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/routing/bgp/{bgpId}",
                return_type=GetSingleSdRoutingTransportGlobalVrfRoutingBgpPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/routing/bgp
        if self._request_adapter.param_checker([(transport_id, str), (vrf_id, str)], [bgp_id]):
            params = {
                "transportId": transport_id,
                "vrfId": vrf_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/routing/bgp",
                return_type=List[GetTransportVrfAssociatedRoutingBgpFeaturesGetResponse],
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/routing/bgp
        if self._request_adapter.param_checker([(transport_id, str)], [bgp_id, vrf_id]):
            params = {
                "transportId": transport_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/routing/bgp",
                return_type=GetListSdRoutingTransportGlobalVrfRoutingBgpPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @overload
    def post(
        self,
        transport_id: str,
        payload: CreateTransportGlobalVrfAndRoutingBgpFeatureAssociationPostRequest,
        vrf_id: str,
        **kw,
    ) -> CreateTransportGlobalVrfAndRoutingBgpFeatureAssociationPostResponse:
        """
        Associate a BGP feature with the global VRF feature for transport feature profile
        POST /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/routing/bgp

        :param transport_id: Transport Profile ID
        :param payload: New BGP Feature ID
        :param vrf_id: Global VRF Feature ID
        :returns: CreateTransportGlobalVrfAndRoutingBgpFeatureAssociationPostResponse
        """
        ...

    @overload
    def post(
        self,
        transport_id: str,
        payload: CreateSdroutingTransportGlobalVrfBgpFeaturePostRequest,
        **kw,
    ) -> CreateSdroutingTransportGlobalVrfBgpFeaturePostResponse:
        """
        Create a SD-Routing WAN BGP feature for global VRF from a specific transport feature profile
        POST /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/routing/bgp

        :param transport_id: Transport Profile ID
        :param payload: SD-Routing WAN BGP feature for global VRF from a specific transport feature profile
        :returns: CreateSdroutingTransportGlobalVrfBgpFeaturePostResponse
        """
        ...

    def post(
        self,
        transport_id: str,
        payload: Union[
            CreateSdroutingTransportGlobalVrfBgpFeaturePostRequest,
            CreateTransportGlobalVrfAndRoutingBgpFeatureAssociationPostRequest,
        ],
        vrf_id: Optional[str] = None,
        **kw,
    ) -> Union[
        CreateSdroutingTransportGlobalVrfBgpFeaturePostResponse,
        CreateTransportGlobalVrfAndRoutingBgpFeatureAssociationPostResponse,
    ]:
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/routing/bgp
        if self._request_adapter.param_checker(
            [
                (transport_id, str),
                (payload, CreateTransportGlobalVrfAndRoutingBgpFeatureAssociationPostRequest),
                (vrf_id, str),
            ],
            [],
        ):
            params = {
                "transportId": transport_id,
                "vrfId": vrf_id,
            }
            return self._request_adapter.request(
                "POST",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/routing/bgp",
                return_type=CreateTransportGlobalVrfAndRoutingBgpFeatureAssociationPostResponse,
                params=params,
                payload=payload,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/routing/bgp
        if self._request_adapter.param_checker(
            [
                (transport_id, str),
                (payload, CreateSdroutingTransportGlobalVrfBgpFeaturePostRequest),
            ],
            [vrf_id],
        ):
            params = {
                "transportId": transport_id,
            }
            return self._request_adapter.request(
                "POST",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/routing/bgp",
                return_type=CreateSdroutingTransportGlobalVrfBgpFeaturePostResponse,
                params=params,
                payload=payload,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @overload
    def put(
        self,
        transport_id: str,
        bgp_id: str,
        payload: EditTransportGlobalVrfAndRoutingBgpFeatureAssociationPutRequest,
        vrf_id: str,
        **kw,
    ) -> EditTransportGlobalVrfAndRoutingBgpFeatureAssociationPutResponse:
        """
        Replace the BGP feature for the global VRF feature in transport feature profile
        PUT /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/routing/bgp/{bgpId}

        :param transport_id: Transport Profile ID
        :param bgp_id: BGP Feature ID
        :param payload: New BGP feature ID
        :param vrf_id: Global VRF Feature ID
        :returns: EditTransportGlobalVrfAndRoutingBgpFeatureAssociationPutResponse
        """
        ...

    @overload
    def put(
        self,
        transport_id: str,
        bgp_id: str,
        payload: EditSdroutingTransportGlobalVrfBgpFeaturePutRequest,
        **kw,
    ) -> EditSdroutingTransportGlobalVrfBgpFeaturePutResponse:
        """
        Edit the SD-Routing WAN BGP feature for global VRF from a specific transport feature profile
        PUT /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/routing/bgp/{bgpId}

        :param transport_id: Transport Profile ID
        :param bgp_id: BGP Feature ID
        :param payload: SD-Routing WAN BGP feature for global VRF from a specific transport feature profile
        :returns: EditSdroutingTransportGlobalVrfBgpFeaturePutResponse
        """
        ...

    def put(
        self,
        transport_id: str,
        bgp_id: str,
        payload: Union[
            EditTransportGlobalVrfAndRoutingBgpFeatureAssociationPutRequest,
            EditSdroutingTransportGlobalVrfBgpFeaturePutRequest,
        ],
        vrf_id: Optional[str] = None,
        **kw,
    ) -> Union[
        EditSdroutingTransportGlobalVrfBgpFeaturePutResponse,
        EditTransportGlobalVrfAndRoutingBgpFeatureAssociationPutResponse,
    ]:
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/routing/bgp/{bgpId}
        if self._request_adapter.param_checker(
            [
                (transport_id, str),
                (bgp_id, str),
                (payload, EditTransportGlobalVrfAndRoutingBgpFeatureAssociationPutRequest),
                (vrf_id, str),
            ],
            [],
        ):
            params = {
                "transportId": transport_id,
                "bgpId": bgp_id,
                "vrfId": vrf_id,
            }
            return self._request_adapter.request(
                "PUT",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/routing/bgp/{bgpId}",
                return_type=EditTransportGlobalVrfAndRoutingBgpFeatureAssociationPutResponse,
                params=params,
                payload=payload,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/routing/bgp/{bgpId}
        if self._request_adapter.param_checker(
            [
                (transport_id, str),
                (bgp_id, str),
                (payload, EditSdroutingTransportGlobalVrfBgpFeaturePutRequest),
            ],
            [vrf_id],
        ):
            params = {
                "transportId": transport_id,
                "bgpId": bgp_id,
            }
            return self._request_adapter.request(
                "PUT",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/routing/bgp/{bgpId}",
                return_type=EditSdroutingTransportGlobalVrfBgpFeaturePutResponse,
                params=params,
                payload=payload,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @overload
    def delete(self, transport_id: str, bgp_id: str, vrf_id: str, **kw):
        """
        Delete the global VRF and BGP feature association for transport feature profile
        DELETE /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/routing/bgp/{bgpId}

        :param transport_id: Transport Profile ID
        :param bgp_id: BGP Feature ID
        :param vrf_id: Global VRF Feature ID
        :returns: None
        """
        ...

    @overload
    def delete(self, transport_id: str, bgp_id: str, **kw):
        """
        Delete the SD-Routing WAN BGP feature for global VRF from a specific transport feature profile
        DELETE /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/routing/bgp/{bgpId}

        :param transport_id: Transport Profile ID
        :param bgp_id: BGP Feature ID
        :returns: None
        """
        ...

    def delete(self, transport_id: str, bgp_id: str, vrf_id: Optional[str] = None, **kw):
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/routing/bgp/{bgpId}
        if self._request_adapter.param_checker(
            [(transport_id, str), (bgp_id, str), (vrf_id, str)], []
        ):
            params = {
                "transportId": transport_id,
                "bgpId": bgp_id,
                "vrfId": vrf_id,
            }
            return self._request_adapter.request(
                "DELETE",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}/routing/bgp/{bgpId}",
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/routing/bgp/{bgpId}
        if self._request_adapter.param_checker([(transport_id, str), (bgp_id, str)], [vrf_id]):
            params = {
                "transportId": transport_id,
                "bgpId": bgp_id,
            }
            return self._request_adapter.request(
                "DELETE",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/routing/bgp/{bgpId}",
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
