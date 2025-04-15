# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateTrackerProfileParcelForTransportPostRequest,
    CreateTrackerProfileParcelForTransportPostResponse,
    EditTrackerProfileParcelForTransportPutRequest,
    EditTrackerProfileParcelForTransportPutResponse,
    GetListSdwanTransportTrackerPayload,
    GetSingleSdwanTransportTrackerPayload,
)

if TYPE_CHECKING:
    from .schema.schema_builder import SchemaBuilder


class TrackerBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/transport/tracker
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, transport_id: str, payload: CreateTrackerProfileParcelForTransportPostRequest, **kw
    ) -> CreateTrackerProfileParcelForTransportPostResponse:
        """
        Create a Tracker Profile Parcel for Transport feature profile
        POST /dataservice/v1/feature-profile/sdwan/transport/{transportId}/tracker

        :param transport_id: Feature Profile ID
        :param payload: Tracker Profile Parcel
        :returns: CreateTrackerProfileParcelForTransportPostResponse
        """
        params = {
            "transportId": transport_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/tracker",
            return_type=CreateTrackerProfileParcelForTransportPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        transport_id: str,
        tracker_id: str,
        payload: EditTrackerProfileParcelForTransportPutRequest,
        **kw,
    ) -> EditTrackerProfileParcelForTransportPutResponse:
        """
        Update a Tracker Profile Parcel for Transport feature profile
        PUT /dataservice/v1/feature-profile/sdwan/transport/{transportId}/tracker/{trackerId}

        :param transport_id: Feature Profile ID
        :param tracker_id: Profile Parcel ID
        :param payload: Tracker Profile Parcel
        :returns: EditTrackerProfileParcelForTransportPutResponse
        """
        params = {
            "transportId": transport_id,
            "trackerId": tracker_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/tracker/{trackerId}",
            return_type=EditTrackerProfileParcelForTransportPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, tracker_id: str, **kw):
        """
        Delete a Tracker Profile Parcel for Transport feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/transport/{transportId}/tracker/{trackerId}

        :param transport_id: Feature Profile ID
        :param tracker_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "trackerId": tracker_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/tracker/{trackerId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, tracker_id: str, **kw
    ) -> GetSingleSdwanTransportTrackerPayload:
        """
        Get Tracker Profile Parcel by parcelId for Transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/tracker/{trackerId}

        :param transport_id: Feature Profile ID
        :param tracker_id: Profile Parcel ID
        :returns: GetSingleSdwanTransportTrackerPayload
        """
        ...

    @overload
    def get(self, transport_id: str, **kw) -> GetListSdwanTransportTrackerPayload:
        """
        Get Tracker Profile Parcels for Transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/tracker

        :param transport_id: Feature Profile ID
        :returns: GetListSdwanTransportTrackerPayload
        """
        ...

    def get(
        self, transport_id: str, tracker_id: Optional[str] = None, **kw
    ) -> Union[GetListSdwanTransportTrackerPayload, GetSingleSdwanTransportTrackerPayload]:
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/tracker/{trackerId}
        if self._request_adapter.param_checker([(transport_id, str), (tracker_id, str)], []):
            params = {
                "transportId": transport_id,
                "trackerId": tracker_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/tracker/{trackerId}",
                return_type=GetSingleSdwanTransportTrackerPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/tracker
        if self._request_adapter.param_checker([(transport_id, str)], [tracker_id]):
            params = {
                "transportId": transport_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/tracker",
                return_type=GetListSdwanTransportTrackerPayload,
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
