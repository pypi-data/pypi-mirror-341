# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateTrackerProfileParcelForTransport1PostRequest,
    CreateTrackerProfileParcelForTransport1PostResponse,
    EditTrackerProfileParcelForTransport1PutRequest,
    EditTrackerProfileParcelForTransport1PutResponse,
    GetListSdRoutingTransportTrackerPayload,
    GetSingleSdRoutingTransportTrackerPayload,
)


class TrackerBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/transport/{transportId}/tracker
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, transport_id: str, payload: CreateTrackerProfileParcelForTransport1PostRequest, **kw
    ) -> CreateTrackerProfileParcelForTransport1PostResponse:
        """
        Create a Tracker Profile Feature for Transport feature profile
        POST /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/tracker

        :param transport_id: Feature Profile ID
        :param payload: Tracker Profile Parcel
        :returns: CreateTrackerProfileParcelForTransport1PostResponse
        """
        params = {
            "transportId": transport_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/tracker",
            return_type=CreateTrackerProfileParcelForTransport1PostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        transport_id: str,
        tracker_id: str,
        payload: EditTrackerProfileParcelForTransport1PutRequest,
        **kw,
    ) -> EditTrackerProfileParcelForTransport1PutResponse:
        """
        Update a Tracker Profile Feature for Transport feature profile
        PUT /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/tracker/{trackerId}

        :param transport_id: Feature Profile ID
        :param tracker_id: Tracker Profile Parcel ID
        :param payload: Tracker Profile Parcel
        :returns: EditTrackerProfileParcelForTransport1PutResponse
        """
        params = {
            "transportId": transport_id,
            "trackerId": tracker_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/tracker/{trackerId}",
            return_type=EditTrackerProfileParcelForTransport1PutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, tracker_id: str, **kw):
        """
        Delete a Tracker Profile Feature for Transport feature profile
        DELETE /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/tracker/{trackerId}

        :param transport_id: Feature Profile ID
        :param tracker_id: Tracker Profile Parcel ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "trackerId": tracker_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/tracker/{trackerId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, tracker_id: str, **kw
    ) -> GetSingleSdRoutingTransportTrackerPayload:
        """
        Get Tracker Profile Feature by parcelId for Transport feature profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/tracker/{trackerId}

        :param transport_id: Feature Profile ID
        :param tracker_id: Tracker Profile Parcel ID
        :returns: GetSingleSdRoutingTransportTrackerPayload
        """
        ...

    @overload
    def get(self, transport_id: str, **kw) -> GetListSdRoutingTransportTrackerPayload:
        """
        Get Tracker Profile Features for Transport feature profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/tracker

        :param transport_id: Feature Profile ID
        :returns: GetListSdRoutingTransportTrackerPayload
        """
        ...

    def get(
        self, transport_id: str, tracker_id: Optional[str] = None, **kw
    ) -> Union[GetListSdRoutingTransportTrackerPayload, GetSingleSdRoutingTransportTrackerPayload]:
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/tracker/{trackerId}
        if self._request_adapter.param_checker([(transport_id, str), (tracker_id, str)], []):
            params = {
                "transportId": transport_id,
                "trackerId": tracker_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/tracker/{trackerId}",
                return_type=GetSingleSdRoutingTransportTrackerPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/tracker
        if self._request_adapter.param_checker([(transport_id, str)], [tracker_id]):
            params = {
                "transportId": transport_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/tracker",
                return_type=GetListSdRoutingTransportTrackerPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
