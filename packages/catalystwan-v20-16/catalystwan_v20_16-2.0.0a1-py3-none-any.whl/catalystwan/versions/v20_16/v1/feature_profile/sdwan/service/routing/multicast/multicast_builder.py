# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateRoutingMulticastProfileParcelForServicePostRequest,
    CreateRoutingMulticastProfileParcelForServicePostResponse,
    EditRoutingMulticastProfileParcelForServicePutRequest,
    EditRoutingMulticastProfileParcelForServicePutResponse,
    GetListSdwanServiceRoutingMulticastPayload,
    GetSingleSdwanServiceRoutingMulticastPayload,
)

if TYPE_CHECKING:
    from .schema.schema_builder import SchemaBuilder


class MulticastBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/service/routing/multicast
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        service_id: str,
        payload: CreateRoutingMulticastProfileParcelForServicePostRequest,
        **kw,
    ) -> CreateRoutingMulticastProfileParcelForServicePostResponse:
        """
        Create a Routing Multicast Profile Parcel for Service feature profile
        POST /dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/multicast

        :param service_id: Feature Profile ID
        :param payload: Routing Multicast Profile Parcel
        :returns: CreateRoutingMulticastProfileParcelForServicePostResponse
        """
        params = {
            "serviceId": service_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/multicast",
            return_type=CreateRoutingMulticastProfileParcelForServicePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        service_id: str,
        multicast_id: str,
        payload: EditRoutingMulticastProfileParcelForServicePutRequest,
        **kw,
    ) -> EditRoutingMulticastProfileParcelForServicePutResponse:
        """
        Update a Routing Multicast Profile Parcel for Service feature profile
        PUT /dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/multicast/{multicastId}

        :param service_id: Feature Profile ID
        :param multicast_id: Profile Parcel ID
        :param payload: Routing Multicast Profile Parcel
        :returns: EditRoutingMulticastProfileParcelForServicePutResponse
        """
        params = {
            "serviceId": service_id,
            "multicastId": multicast_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/multicast/{multicastId}",
            return_type=EditRoutingMulticastProfileParcelForServicePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, service_id: str, multicast_id: str, **kw):
        """
        Delete a Routing Multicast Profile Parcel for Service feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/multicast/{multicastId}

        :param service_id: Feature Profile ID
        :param multicast_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "serviceId": service_id,
            "multicastId": multicast_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/multicast/{multicastId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, service_id: str, multicast_id: str, **kw
    ) -> GetSingleSdwanServiceRoutingMulticastPayload:
        """
        Get Routing Multicast Profile Parcel by parcelId for Service feature profile
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/multicast/{multicastId}

        :param service_id: Feature Profile ID
        :param multicast_id: Profile Parcel ID
        :returns: GetSingleSdwanServiceRoutingMulticastPayload
        """
        ...

    @overload
    def get(self, service_id: str, **kw) -> GetListSdwanServiceRoutingMulticastPayload:
        """
        Get Routing Multicast Profile Parcels for Service feature profile
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/multicast

        :param service_id: Feature Profile ID
        :returns: GetListSdwanServiceRoutingMulticastPayload
        """
        ...

    def get(
        self, service_id: str, multicast_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdwanServiceRoutingMulticastPayload, GetSingleSdwanServiceRoutingMulticastPayload
    ]:
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/multicast/{multicastId}
        if self._request_adapter.param_checker([(service_id, str), (multicast_id, str)], []):
            params = {
                "serviceId": service_id,
                "multicastId": multicast_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/multicast/{multicastId}",
                return_type=GetSingleSdwanServiceRoutingMulticastPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/multicast
        if self._request_adapter.param_checker([(service_id, str)], [multicast_id]):
            params = {
                "serviceId": service_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/multicast",
                return_type=GetListSdwanServiceRoutingMulticastPayload,
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
