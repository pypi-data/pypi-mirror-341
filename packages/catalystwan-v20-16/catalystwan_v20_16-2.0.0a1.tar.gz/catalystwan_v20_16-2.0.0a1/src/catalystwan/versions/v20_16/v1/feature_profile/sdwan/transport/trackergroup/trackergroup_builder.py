# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateTrackerGroupProfileParcelForTransportPostRequest,
    CreateTrackerGroupProfileParcelForTransportPostResponse,
    EditTrackerGroupProfileParcelForTransportPutRequest,
    EditTrackerGroupProfileParcelForTransportPutResponse,
    GetListSdwanTransportTrackergroupPayload,
    GetSingleSdwanTransportTrackergroupPayload,
)

if TYPE_CHECKING:
    from .schema.schema_builder import SchemaBuilder


class TrackergroupBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/transport/trackergroup
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        transport_id: str,
        payload: CreateTrackerGroupProfileParcelForTransportPostRequest,
        **kw,
    ) -> CreateTrackerGroupProfileParcelForTransportPostResponse:
        """
        Create a TrackerGroup Profile Parcel for Transport feature profile
        POST /dataservice/v1/feature-profile/sdwan/transport/{transportId}/trackergroup

        :param transport_id: Feature Profile ID
        :param payload: TrackerGroup Profile Parcel
        :returns: CreateTrackerGroupProfileParcelForTransportPostResponse
        """
        params = {
            "transportId": transport_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/trackergroup",
            return_type=CreateTrackerGroupProfileParcelForTransportPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        transport_id: str,
        trackergroup_id: str,
        payload: EditTrackerGroupProfileParcelForTransportPutRequest,
        **kw,
    ) -> EditTrackerGroupProfileParcelForTransportPutResponse:
        """
        Update a TrackerGroup Profile Parcel for Transport feature profile
        PUT /dataservice/v1/feature-profile/sdwan/transport/{transportId}/trackergroup/{trackergroupId}

        :param transport_id: Feature Profile ID
        :param trackergroup_id: Profile Parcel ID
        :param payload: TrackerGroup Profile Parcel
        :returns: EditTrackerGroupProfileParcelForTransportPutResponse
        """
        params = {
            "transportId": transport_id,
            "trackergroupId": trackergroup_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/trackergroup/{trackergroupId}",
            return_type=EditTrackerGroupProfileParcelForTransportPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, trackergroup_id: str, **kw):
        """
        Delete a TrackerGroup Profile Parcel for Transport feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/transport/{transportId}/trackergroup/{trackergroupId}

        :param transport_id: Feature Profile ID
        :param trackergroup_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "trackergroupId": trackergroup_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/trackergroup/{trackergroupId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, trackergroup_id: str, **kw
    ) -> GetSingleSdwanTransportTrackergroupPayload:
        """
        Get TrackerGroup Profile Parcel by parcelId for Transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/trackergroup/{trackergroupId}

        :param transport_id: Feature Profile ID
        :param trackergroup_id: Profile Parcel ID
        :returns: GetSingleSdwanTransportTrackergroupPayload
        """
        ...

    @overload
    def get(self, transport_id: str, **kw) -> GetListSdwanTransportTrackergroupPayload:
        """
        Get TrackerGroup Profile Parcels for Transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/trackergroup

        :param transport_id: Feature Profile ID
        :returns: GetListSdwanTransportTrackergroupPayload
        """
        ...

    def get(
        self, transport_id: str, trackergroup_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdwanTransportTrackergroupPayload, GetSingleSdwanTransportTrackergroupPayload
    ]:
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/trackergroup/{trackergroupId}
        if self._request_adapter.param_checker([(transport_id, str), (trackergroup_id, str)], []):
            params = {
                "transportId": transport_id,
                "trackergroupId": trackergroup_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/trackergroup/{trackergroupId}",
                return_type=GetSingleSdwanTransportTrackergroupPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/trackergroup
        if self._request_adapter.param_checker([(transport_id, str)], [trackergroup_id]):
            params = {
                "transportId": transport_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/trackergroup",
                return_type=GetListSdwanTransportTrackergroupPayload,
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
