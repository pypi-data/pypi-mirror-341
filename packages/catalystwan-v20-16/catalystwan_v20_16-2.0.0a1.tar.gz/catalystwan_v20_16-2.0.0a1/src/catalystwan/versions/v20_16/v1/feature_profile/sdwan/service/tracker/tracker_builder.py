# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateTrackerProfileParcelForServicePostRequest,
    CreateTrackerProfileParcelForServicePostResponse,
    EditTrackerProfileParcelForServicePutRequest,
    EditTrackerProfileParcelForServicePutResponse,
    GetListSdwanServiceTrackerPayload,
    GetSingleSdwanServiceTrackerPayload,
)

if TYPE_CHECKING:
    from .schema.schema_builder import SchemaBuilder


class TrackerBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/service/tracker
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, service_id: str, payload: CreateTrackerProfileParcelForServicePostRequest, **kw
    ) -> CreateTrackerProfileParcelForServicePostResponse:
        """
        Create a Tracker Profile Parcel for Service feature profile
        POST /dataservice/v1/feature-profile/sdwan/service/{serviceId}/tracker

        :param service_id: Feature Profile ID
        :param payload: Tracker Profile Parcel
        :returns: CreateTrackerProfileParcelForServicePostResponse
        """
        params = {
            "serviceId": service_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/tracker",
            return_type=CreateTrackerProfileParcelForServicePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        service_id: str,
        tracker_id: str,
        payload: EditTrackerProfileParcelForServicePutRequest,
        **kw,
    ) -> EditTrackerProfileParcelForServicePutResponse:
        """
        Update a Tracker Profile Parcel for Service feature profile
        PUT /dataservice/v1/feature-profile/sdwan/service/{serviceId}/tracker/{trackerId}

        :param service_id: Feature Profile ID
        :param tracker_id: Profile Parcel ID
        :param payload: Tracker Profile Parcel
        :returns: EditTrackerProfileParcelForServicePutResponse
        """
        params = {
            "serviceId": service_id,
            "trackerId": tracker_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/tracker/{trackerId}",
            return_type=EditTrackerProfileParcelForServicePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, service_id: str, tracker_id: str, **kw):
        """
        Delete a Tracker Profile Parcel for Service feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/service/{serviceId}/tracker/{trackerId}

        :param service_id: Feature Profile ID
        :param tracker_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "serviceId": service_id,
            "trackerId": tracker_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/tracker/{trackerId}",
            params=params,
            **kw,
        )

    @overload
    def get(self, service_id: str, tracker_id: str, **kw) -> GetSingleSdwanServiceTrackerPayload:
        """
        Get Tracker Profile Parcel by parcelId for Service feature profile
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/tracker/{trackerId}

        :param service_id: Feature Profile ID
        :param tracker_id: Profile Parcel ID
        :returns: GetSingleSdwanServiceTrackerPayload
        """
        ...

    @overload
    def get(self, service_id: str, **kw) -> GetListSdwanServiceTrackerPayload:
        """
        Get Tracker Profile Parcels for Service feature profile
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/tracker

        :param service_id: Feature Profile ID
        :returns: GetListSdwanServiceTrackerPayload
        """
        ...

    def get(
        self, service_id: str, tracker_id: Optional[str] = None, **kw
    ) -> Union[GetListSdwanServiceTrackerPayload, GetSingleSdwanServiceTrackerPayload]:
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/tracker/{trackerId}
        if self._request_adapter.param_checker([(service_id, str), (tracker_id, str)], []):
            params = {
                "serviceId": service_id,
                "trackerId": tracker_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/tracker/{trackerId}",
                return_type=GetSingleSdwanServiceTrackerPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/tracker
        if self._request_adapter.param_checker([(service_id, str)], [tracker_id]):
            params = {
                "serviceId": service_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/tracker",
                return_type=GetListSdwanServiceTrackerPayload,
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
