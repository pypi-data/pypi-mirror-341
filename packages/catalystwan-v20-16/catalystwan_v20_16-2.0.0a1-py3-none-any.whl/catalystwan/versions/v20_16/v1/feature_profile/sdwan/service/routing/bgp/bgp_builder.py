# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateRoutingBgpProfileParcelForServicePostRequest,
    CreateRoutingBgpProfileParcelForServicePostResponse,
    EditRoutingBgpProfileParcelForServicePutRequest,
    EditRoutingBgpProfileParcelForServicePutResponse,
    GetListSdwanServiceRoutingBgpPayload,
    GetSingleSdwanServiceRoutingBgpPayload,
)

if TYPE_CHECKING:
    from .schema.schema_builder import SchemaBuilder


class BgpBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/service/routing/bgp
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, service_id: str, payload: CreateRoutingBgpProfileParcelForServicePostRequest, **kw
    ) -> CreateRoutingBgpProfileParcelForServicePostResponse:
        """
        Create a Routing Bgp Profile Parcel for Service feature profile
        POST /dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/bgp

        :param service_id: Feature Profile ID
        :param payload: Routing Bgp Profile Parcel
        :returns: CreateRoutingBgpProfileParcelForServicePostResponse
        """
        params = {
            "serviceId": service_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/bgp",
            return_type=CreateRoutingBgpProfileParcelForServicePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        service_id: str,
        bgp_id: str,
        payload: EditRoutingBgpProfileParcelForServicePutRequest,
        **kw,
    ) -> EditRoutingBgpProfileParcelForServicePutResponse:
        """
        Update a Routing Bgp Profile Parcel for Service feature profile
        PUT /dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/bgp/{bgpId}

        :param service_id: Feature Profile ID
        :param bgp_id: Profile Parcel ID
        :param payload: Routing Bgp Profile Parcel
        :returns: EditRoutingBgpProfileParcelForServicePutResponse
        """
        params = {
            "serviceId": service_id,
            "bgpId": bgp_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/bgp/{bgpId}",
            return_type=EditRoutingBgpProfileParcelForServicePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, service_id: str, bgp_id: str, **kw):
        """
        Delete a Routing Bgp Profile Parcel for Service feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/bgp/{bgpId}

        :param service_id: Feature Profile ID
        :param bgp_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "serviceId": service_id,
            "bgpId": bgp_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/bgp/{bgpId}",
            params=params,
            **kw,
        )

    @overload
    def get(self, service_id: str, bgp_id: str, **kw) -> GetSingleSdwanServiceRoutingBgpPayload:
        """
        Get Routing Bgp Profile Parcel by parcelId for Service feature profile
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/bgp/{bgpId}

        :param service_id: Feature Profile ID
        :param bgp_id: Profile Parcel ID
        :returns: GetSingleSdwanServiceRoutingBgpPayload
        """
        ...

    @overload
    def get(self, service_id: str, **kw) -> GetListSdwanServiceRoutingBgpPayload:
        """
        Get Routing Bgp Profile Parcels for Service feature profile
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/bgp

        :param service_id: Feature Profile ID
        :returns: GetListSdwanServiceRoutingBgpPayload
        """
        ...

    def get(
        self, service_id: str, bgp_id: Optional[str] = None, **kw
    ) -> Union[GetListSdwanServiceRoutingBgpPayload, GetSingleSdwanServiceRoutingBgpPayload]:
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/bgp/{bgpId}
        if self._request_adapter.param_checker([(service_id, str), (bgp_id, str)], []):
            params = {
                "serviceId": service_id,
                "bgpId": bgp_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/bgp/{bgpId}",
                return_type=GetSingleSdwanServiceRoutingBgpPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/bgp
        if self._request_adapter.param_checker([(service_id, str)], [bgp_id]):
            params = {
                "serviceId": service_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/bgp",
                return_type=GetListSdwanServiceRoutingBgpPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def schema(self) -> SchemaBuilder:
        """
        The schema property
        """
        from .schema.schema_builder import SchemaBuilder

        return SchemaBuilder(self._request_adapter)
