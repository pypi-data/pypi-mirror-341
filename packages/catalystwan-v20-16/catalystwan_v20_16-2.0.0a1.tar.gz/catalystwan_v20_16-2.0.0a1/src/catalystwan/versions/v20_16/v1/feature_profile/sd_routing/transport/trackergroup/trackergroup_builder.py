# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateTrackerGroupProfileParcelForTransport1PostRequest,
    CreateTrackerGroupProfileParcelForTransport1PostResponse,
    EditTrackerGroupProfileParcelForTransport1PutRequest,
    EditTrackerGroupProfileParcelForTransport1PutResponse,
    GetListSdRoutingTransportTrackergroupPayload,
    GetSingleSdRoutingTransportTrackergroupPayload,
)


class TrackergroupBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/transport/{transportId}/trackergroup
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        transport_id: str,
        payload: CreateTrackerGroupProfileParcelForTransport1PostRequest,
        **kw,
    ) -> CreateTrackerGroupProfileParcelForTransport1PostResponse:
        """
        Create a TrackerGroup Profile Feature for Transport feature profile
        POST /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/trackergroup

        :param transport_id: Feature Profile ID
        :param payload: TrackerGroup Profile Parcel
        :returns: CreateTrackerGroupProfileParcelForTransport1PostResponse
        """
        params = {
            "transportId": transport_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/trackergroup",
            return_type=CreateTrackerGroupProfileParcelForTransport1PostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        transport_id: str,
        trackergroup_id: str,
        payload: EditTrackerGroupProfileParcelForTransport1PutRequest,
        **kw,
    ) -> EditTrackerGroupProfileParcelForTransport1PutResponse:
        """
        Update a TrackerGroup Profile Feature for Transport feature profile
        PUT /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/trackergroup/{trackergroupId}

        :param transport_id: Feature Profile ID
        :param trackergroup_id: Tracker Group Profile Parcel ID
        :param payload: TrackerGroup Profile Parcel
        :returns: EditTrackerGroupProfileParcelForTransport1PutResponse
        """
        params = {
            "transportId": transport_id,
            "trackergroupId": trackergroup_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/trackergroup/{trackergroupId}",
            return_type=EditTrackerGroupProfileParcelForTransport1PutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, trackergroup_id: str, **kw):
        """
        Delete a TrackerGroup Profile Feature for Transport feature profile
        DELETE /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/trackergroup/{trackergroupId}

        :param transport_id: Feature Profile ID
        :param trackergroup_id: Tracker Group Profile Parcel ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "trackergroupId": trackergroup_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/trackergroup/{trackergroupId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, trackergroup_id: str, **kw
    ) -> GetSingleSdRoutingTransportTrackergroupPayload:
        """
        Get TrackerGroup Profile Feature by parcelId for Transport feature profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/trackergroup/{trackergroupId}

        :param transport_id: Feature Profile ID
        :param trackergroup_id: Tracker Group Profile Parcel ID
        :returns: GetSingleSdRoutingTransportTrackergroupPayload
        """
        ...

    @overload
    def get(self, transport_id: str, **kw) -> GetListSdRoutingTransportTrackergroupPayload:
        """
        Get TrackerGroup Profile Features for Transport feature profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/trackergroup

        :param transport_id: Feature Profile ID
        :returns: GetListSdRoutingTransportTrackergroupPayload
        """
        ...

    def get(
        self, transport_id: str, trackergroup_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdRoutingTransportTrackergroupPayload, GetSingleSdRoutingTransportTrackergroupPayload
    ]:
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/trackergroup/{trackergroupId}
        if self._request_adapter.param_checker([(transport_id, str), (trackergroup_id, str)], []):
            params = {
                "transportId": transport_id,
                "trackergroupId": trackergroup_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/trackergroup/{trackergroupId}",
                return_type=GetSingleSdRoutingTransportTrackergroupPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/trackergroup
        if self._request_adapter.param_checker([(transport_id, str)], [trackergroup_id]):
            params = {
                "transportId": transport_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/trackergroup",
                return_type=GetListSdRoutingTransportTrackergroupPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
