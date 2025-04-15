# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateIpv6TrackerGroupProfileParcelForTransportPostRequest,
    CreateIpv6TrackerGroupProfileParcelForTransportPostResponse,
    EditIpv6TrackerGroupProfileParcelForTransportPutRequest,
    EditIpv6TrackerGroupProfileParcelForTransportPutResponse,
    GetListSdwanTransportIpv6TrackergroupPayload,
    GetSingleSdwanTransportIpv6TrackergroupPayload,
)

if TYPE_CHECKING:
    from .schema.schema_builder import SchemaBuilder


class Ipv6TrackergroupBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/transport/ipv6-trackergroup
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        transport_id: str,
        payload: CreateIpv6TrackerGroupProfileParcelForTransportPostRequest,
        **kw,
    ) -> CreateIpv6TrackerGroupProfileParcelForTransportPostResponse:
        """
        Create a IPv6 TrackerGroup Profile Parcel for Transport feature profile
        POST /dataservice/v1/feature-profile/sdwan/transport/{transportId}/ipv6-trackergroup

        :param transport_id: Feature Profile ID
        :param payload: IPv6 TrackerGroup Profile Parcel
        :returns: CreateIpv6TrackerGroupProfileParcelForTransportPostResponse
        """
        params = {
            "transportId": transport_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/ipv6-trackergroup",
            return_type=CreateIpv6TrackerGroupProfileParcelForTransportPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        transport_id: str,
        ipv6_trackergroup_id: str,
        payload: EditIpv6TrackerGroupProfileParcelForTransportPutRequest,
        **kw,
    ) -> EditIpv6TrackerGroupProfileParcelForTransportPutResponse:
        """
        Update a IPv6 TrackerGroup Profile Parcel for Transport feature profile
        PUT /dataservice/v1/feature-profile/sdwan/transport/{transportId}/ipv6-trackergroup/{ipv6-trackergroupId}

        :param transport_id: Feature Profile ID
        :param ipv6_trackergroup_id: Profile Parcel ID
        :param payload: IPv6 TrackerGroup Profile Parcel
        :returns: EditIpv6TrackerGroupProfileParcelForTransportPutResponse
        """
        params = {
            "transportId": transport_id,
            "ipv6-trackergroupId": ipv6_trackergroup_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/ipv6-trackergroup/{ipv6-trackergroupId}",
            return_type=EditIpv6TrackerGroupProfileParcelForTransportPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, ipv6_trackergroup_id: str, **kw):
        """
        Delete a IPv6 TrackerGroup Profile Parcel for Transport feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/transport/{transportId}/ipv6-trackergroup/{ipv6-trackergroupId}

        :param transport_id: Feature Profile ID
        :param ipv6_trackergroup_id: IPv6 Tracker Group Profile Parcel ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "ipv6-trackergroupId": ipv6_trackergroup_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/ipv6-trackergroup/{ipv6-trackergroupId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, ipv6_trackergroup_id: str, **kw
    ) -> GetSingleSdwanTransportIpv6TrackergroupPayload:
        """
        Get IPv6 TrackerGroup Profile Parcel by parcelId for Transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/ipv6-trackergroup/{ipv6-trackergroupId}

        :param transport_id: Feature Profile ID
        :param ipv6_trackergroup_id: IPv6 Tracker Group Profile Parcel ID
        :returns: GetSingleSdwanTransportIpv6TrackergroupPayload
        """
        ...

    @overload
    def get(self, transport_id: str, **kw) -> GetListSdwanTransportIpv6TrackergroupPayload:
        """
        Get IPv6 TrackerGroup Profile Parcels for Transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/ipv6-trackergroup

        :param transport_id: Feature Profile ID
        :returns: GetListSdwanTransportIpv6TrackergroupPayload
        """
        ...

    def get(
        self, transport_id: str, ipv6_trackergroup_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdwanTransportIpv6TrackergroupPayload, GetSingleSdwanTransportIpv6TrackergroupPayload
    ]:
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/ipv6-trackergroup/{ipv6-trackergroupId}
        if self._request_adapter.param_checker(
            [(transport_id, str), (ipv6_trackergroup_id, str)], []
        ):
            params = {
                "transportId": transport_id,
                "ipv6-trackergroupId": ipv6_trackergroup_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/ipv6-trackergroup/{ipv6-trackergroupId}",
                return_type=GetSingleSdwanTransportIpv6TrackergroupPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/ipv6-trackergroup
        if self._request_adapter.param_checker([(transport_id, str)], [ipv6_trackergroup_id]):
            params = {
                "transportId": transport_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/ipv6-trackergroup",
                return_type=GetListSdwanTransportIpv6TrackergroupPayload,
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
