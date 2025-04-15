# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdroutingServiceVrfBgpFeaturePostRequest,
    CreateSdroutingServiceVrfBgpFeaturePostResponse,
    CreateServiceVrfAndRoutingBgpFeatureAssociationPostRequest,
    CreateServiceVrfAndRoutingBgpFeatureAssociationPostResponse,
    EditSdroutingServiceVrfBgpFeaturePutRequest,
    EditSdroutingServiceVrfBgpFeaturePutResponse,
    EditServiceVrfAndRoutingBgpFeatureAssociationPutRequest,
    EditServiceVrfAndRoutingBgpFeatureAssociationPutResponse,
    GetListSdRoutingServiceVrfRoutingBgpPayload,
    GetServiceVrfAssociatedRoutingBgpFeaturesGetResponse,
    GetSingleSdRoutingServiceVrfRoutingBgpPayload,
    GetSingleSdRoutingServiceVrfVrfRoutingBgpPayload,
)


class BgpBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/service/{serviceId}/vrf/routing/bgp
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @overload
    def get(
        self, *, service_id: str, vrf_id: str, bgp_id: str, **kw
    ) -> GetSingleSdRoutingServiceVrfVrfRoutingBgpPayload:
        """
        Get VRF parcel associated RoutingBGP Parcel by bgpId for service feature profile
        GET /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/bgp/{bgpId}

        :param service_id: Service Profile ID
        :param vrf_id: VRF Feature ID
        :param bgp_id: BGP Feature ID
        :returns: GetSingleSdRoutingServiceVrfVrfRoutingBgpPayload
        """
        ...

    @overload
    def get(
        self, *, service_id: str, bgp_id: str, **kw
    ) -> GetSingleSdRoutingServiceVrfRoutingBgpPayload:
        """
        Get the SD-Routing LAN BGP feature from a specific service feature profile
        GET /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/routing/bgp/{bgpId}

        :param service_id: Service Profile ID
        :param bgp_id: BGP Feature ID
        :returns: GetSingleSdRoutingServiceVrfRoutingBgpPayload
        """
        ...

    @overload
    def get(
        self, *, service_id: str, vrf_id: str, **kw
    ) -> List[GetServiceVrfAssociatedRoutingBgpFeaturesGetResponse]:
        """
        Get the LAN VRF associated BGP Features for service feature profile
        GET /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/bgp

        :param service_id: Service Profile ID
        :param vrf_id: VRF Feature ID
        :returns: List[GetServiceVrfAssociatedRoutingBgpFeaturesGetResponse]
        """
        ...

    @overload
    def get(self, *, service_id: str, **kw) -> GetListSdRoutingServiceVrfRoutingBgpPayload:
        """
        Get all SD-Routing LAN BGP features from a specific service feature profile
        GET /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/routing/bgp

        :param service_id: Service Profile ID
        :returns: GetListSdRoutingServiceVrfRoutingBgpPayload
        """
        ...

    def get(
        self, *, service_id: str, bgp_id: Optional[str] = None, vrf_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdRoutingServiceVrfRoutingBgpPayload,
        GetSingleSdRoutingServiceVrfRoutingBgpPayload,
        List[GetServiceVrfAssociatedRoutingBgpFeaturesGetResponse],
        GetSingleSdRoutingServiceVrfVrfRoutingBgpPayload,
    ]:
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/bgp/{bgpId}
        if self._request_adapter.param_checker(
            [(service_id, str), (vrf_id, str), (bgp_id, str)], []
        ):
            params = {
                "serviceId": service_id,
                "vrfId": vrf_id,
                "bgpId": bgp_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/bgp/{bgpId}",
                return_type=GetSingleSdRoutingServiceVrfVrfRoutingBgpPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/routing/bgp/{bgpId}
        if self._request_adapter.param_checker([(service_id, str), (bgp_id, str)], [vrf_id]):
            params = {
                "serviceId": service_id,
                "bgpId": bgp_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/routing/bgp/{bgpId}",
                return_type=GetSingleSdRoutingServiceVrfRoutingBgpPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/bgp
        if self._request_adapter.param_checker([(service_id, str), (vrf_id, str)], [bgp_id]):
            params = {
                "serviceId": service_id,
                "vrfId": vrf_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/bgp",
                return_type=List[GetServiceVrfAssociatedRoutingBgpFeaturesGetResponse],
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/routing/bgp
        if self._request_adapter.param_checker([(service_id, str)], [bgp_id, vrf_id]):
            params = {
                "serviceId": service_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/routing/bgp",
                return_type=GetListSdRoutingServiceVrfRoutingBgpPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @overload
    def post(
        self,
        service_id: str,
        payload: CreateServiceVrfAndRoutingBgpFeatureAssociationPostRequest,
        vrf_id: str,
        **kw,
    ) -> CreateServiceVrfAndRoutingBgpFeatureAssociationPostResponse:
        """
        Associate a BGP feature with the LAN VRF feature for service feature profile
        POST /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/bgp

        :param service_id: Service Profile ID
        :param payload: New BGP feature ID
        :param vrf_id: VRF Feature ID
        :returns: CreateServiceVrfAndRoutingBgpFeatureAssociationPostResponse
        """
        ...

    @overload
    def post(
        self, service_id: str, payload: CreateSdroutingServiceVrfBgpFeaturePostRequest, **kw
    ) -> CreateSdroutingServiceVrfBgpFeaturePostResponse:
        """
        Create a SD-Routing LAN BGP feature from a specific service feature profile
        POST /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/routing/bgp

        :param service_id: Service Profile ID
        :param payload: SD-Routing LAN BGP feature from a specific service feature profile
        :returns: CreateSdroutingServiceVrfBgpFeaturePostResponse
        """
        ...

    def post(
        self,
        service_id: str,
        payload: Union[
            CreateServiceVrfAndRoutingBgpFeatureAssociationPostRequest,
            CreateSdroutingServiceVrfBgpFeaturePostRequest,
        ],
        vrf_id: Optional[str] = None,
        **kw,
    ) -> Union[
        CreateSdroutingServiceVrfBgpFeaturePostResponse,
        CreateServiceVrfAndRoutingBgpFeatureAssociationPostResponse,
    ]:
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/bgp
        if self._request_adapter.param_checker(
            [
                (service_id, str),
                (payload, CreateServiceVrfAndRoutingBgpFeatureAssociationPostRequest),
                (vrf_id, str),
            ],
            [],
        ):
            params = {
                "serviceId": service_id,
                "vrfId": vrf_id,
            }
            return self._request_adapter.request(
                "POST",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/bgp",
                return_type=CreateServiceVrfAndRoutingBgpFeatureAssociationPostResponse,
                params=params,
                payload=payload,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/routing/bgp
        if self._request_adapter.param_checker(
            [(service_id, str), (payload, CreateSdroutingServiceVrfBgpFeaturePostRequest)], [vrf_id]
        ):
            params = {
                "serviceId": service_id,
            }
            return self._request_adapter.request(
                "POST",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/routing/bgp",
                return_type=CreateSdroutingServiceVrfBgpFeaturePostResponse,
                params=params,
                payload=payload,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @overload
    def put(
        self,
        service_id: str,
        bgp_id: str,
        payload: EditServiceVrfAndRoutingBgpFeatureAssociationPutRequest,
        vrf_id: str,
        **kw,
    ) -> EditServiceVrfAndRoutingBgpFeatureAssociationPutResponse:
        """
        Replace the BGP feature for LAN VRF feature in service feature profile
        PUT /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/bgp/{bgpId}

        :param service_id: Service Profile ID
        :param bgp_id: Old BGP Feature ID
        :param payload: New BGP feature ID
        :param vrf_id: VRF Feature ID
        :returns: EditServiceVrfAndRoutingBgpFeatureAssociationPutResponse
        """
        ...

    @overload
    def put(
        self,
        service_id: str,
        bgp_id: str,
        payload: EditSdroutingServiceVrfBgpFeaturePutRequest,
        **kw,
    ) -> EditSdroutingServiceVrfBgpFeaturePutResponse:
        """
        Edit the SD-Routing LAN BGP feature from a specific service feature profile
        PUT /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/routing/bgp/{bgpId}

        :param service_id: Service Profile ID
        :param bgp_id: BGP Feature ID
        :param payload: SD-Routing LAN BGP feature from a specific service feature profile
        :returns: EditSdroutingServiceVrfBgpFeaturePutResponse
        """
        ...

    def put(
        self,
        service_id: str,
        bgp_id: str,
        payload: Union[
            EditServiceVrfAndRoutingBgpFeatureAssociationPutRequest,
            EditSdroutingServiceVrfBgpFeaturePutRequest,
        ],
        vrf_id: Optional[str] = None,
        **kw,
    ) -> Union[
        EditSdroutingServiceVrfBgpFeaturePutResponse,
        EditServiceVrfAndRoutingBgpFeatureAssociationPutResponse,
    ]:
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/bgp/{bgpId}
        if self._request_adapter.param_checker(
            [
                (service_id, str),
                (bgp_id, str),
                (payload, EditServiceVrfAndRoutingBgpFeatureAssociationPutRequest),
                (vrf_id, str),
            ],
            [],
        ):
            params = {
                "serviceId": service_id,
                "bgpId": bgp_id,
                "vrfId": vrf_id,
            }
            return self._request_adapter.request(
                "PUT",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/bgp/{bgpId}",
                return_type=EditServiceVrfAndRoutingBgpFeatureAssociationPutResponse,
                params=params,
                payload=payload,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/routing/bgp/{bgpId}
        if self._request_adapter.param_checker(
            [
                (service_id, str),
                (bgp_id, str),
                (payload, EditSdroutingServiceVrfBgpFeaturePutRequest),
            ],
            [vrf_id],
        ):
            params = {
                "serviceId": service_id,
                "bgpId": bgp_id,
            }
            return self._request_adapter.request(
                "PUT",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/routing/bgp/{bgpId}",
                return_type=EditSdroutingServiceVrfBgpFeaturePutResponse,
                params=params,
                payload=payload,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @overload
    def delete(self, service_id: str, bgp_id: str, vrf_id: str, **kw):
        """
        Delete the LAN VRF feature and BGP feature association for service feature profile
        DELETE /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/bgp/{bgpId}

        :param service_id: Service Profile ID
        :param bgp_id: BGP Feature ID
        :param vrf_id: VRF Feature ID
        :returns: None
        """
        ...

    @overload
    def delete(self, service_id: str, bgp_id: str, **kw):
        """
        Delete the SD-Routing LAN BGP feature from a specific service feature profile
        DELETE /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/routing/bgp/{bgpId}

        :param service_id: Service Profile ID
        :param bgp_id: BGP Feature ID
        :returns: None
        """
        ...

    def delete(self, service_id: str, bgp_id: str, vrf_id: Optional[str] = None, **kw):
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/bgp/{bgpId}
        if self._request_adapter.param_checker(
            [(service_id, str), (bgp_id, str), (vrf_id, str)], []
        ):
            params = {
                "serviceId": service_id,
                "bgpId": bgp_id,
                "vrfId": vrf_id,
            }
            return self._request_adapter.request(
                "DELETE",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/routing/bgp/{bgpId}",
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/routing/bgp/{bgpId}
        if self._request_adapter.param_checker([(service_id, str), (bgp_id, str)], [vrf_id]):
            params = {
                "serviceId": service_id,
                "bgpId": bgp_id,
            }
            return self._request_adapter.request(
                "DELETE",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/routing/bgp/{bgpId}",
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
