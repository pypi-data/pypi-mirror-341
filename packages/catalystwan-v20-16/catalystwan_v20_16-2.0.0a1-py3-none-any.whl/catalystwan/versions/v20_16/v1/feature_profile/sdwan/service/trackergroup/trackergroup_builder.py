# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateTrackerGroupProfileParcelForServicePostRequest,
    CreateTrackerGroupProfileParcelForServicePostResponse,
    EditTrackerGroupProfileParcelForServicePutRequest,
    EditTrackerGroupProfileParcelForServicePutResponse,
    GetListSdwanServiceTrackergroupPayload,
    GetSingleSdwanServiceTrackergroupPayload,
)

if TYPE_CHECKING:
    from .schema.schema_builder import SchemaBuilder


class TrackergroupBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/service/trackergroup
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, service_id: str, payload: CreateTrackerGroupProfileParcelForServicePostRequest, **kw
    ) -> CreateTrackerGroupProfileParcelForServicePostResponse:
        """
        Create a TrackerGroup Profile Parcel for Service feature profile
        POST /dataservice/v1/feature-profile/sdwan/service/{serviceId}/trackergroup

        :param service_id: Feature Profile ID
        :param payload: TrackerGroup Profile Parcel
        :returns: CreateTrackerGroupProfileParcelForServicePostResponse
        """
        params = {
            "serviceId": service_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/trackergroup",
            return_type=CreateTrackerGroupProfileParcelForServicePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        service_id: str,
        trackergroup_id: str,
        payload: EditTrackerGroupProfileParcelForServicePutRequest,
        **kw,
    ) -> EditTrackerGroupProfileParcelForServicePutResponse:
        """
        Update a TrackerGroup Profile Parcel for Service feature profile
        PUT /dataservice/v1/feature-profile/sdwan/service/{serviceId}/trackergroup/{trackergroupId}

        :param service_id: Feature Profile ID
        :param trackergroup_id: Profile Parcel ID
        :param payload: TrackerGroup Profile Parcel
        :returns: EditTrackerGroupProfileParcelForServicePutResponse
        """
        params = {
            "serviceId": service_id,
            "trackergroupId": trackergroup_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/trackergroup/{trackergroupId}",
            return_type=EditTrackerGroupProfileParcelForServicePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, service_id: str, trackergroup_id: str, **kw):
        """
        Delete a TrackerGroup Profile Parcel for Service feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/service/{serviceId}/trackergroup/{trackergroupId}

        :param service_id: Feature Profile ID
        :param trackergroup_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "serviceId": service_id,
            "trackergroupId": trackergroup_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/trackergroup/{trackergroupId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, service_id: str, trackergroup_id: str, **kw
    ) -> GetSingleSdwanServiceTrackergroupPayload:
        """
        Get TrackerGroup Profile Parcel by parcelId for Service feature profile
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/trackergroup/{trackergroupId}

        :param service_id: Feature Profile ID
        :param trackergroup_id: Profile Parcel ID
        :returns: GetSingleSdwanServiceTrackergroupPayload
        """
        ...

    @overload
    def get(self, service_id: str, **kw) -> GetListSdwanServiceTrackergroupPayload:
        """
        Get TrackerGroup Profile Parcels for Service feature profile
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/trackergroup

        :param service_id: Feature Profile ID
        :returns: GetListSdwanServiceTrackergroupPayload
        """
        ...

    def get(
        self, service_id: str, trackergroup_id: Optional[str] = None, **kw
    ) -> Union[GetListSdwanServiceTrackergroupPayload, GetSingleSdwanServiceTrackergroupPayload]:
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/trackergroup/{trackergroupId}
        if self._request_adapter.param_checker([(service_id, str), (trackergroup_id, str)], []):
            params = {
                "serviceId": service_id,
                "trackergroupId": trackergroup_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/trackergroup/{trackergroupId}",
                return_type=GetSingleSdwanServiceTrackergroupPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/trackergroup
        if self._request_adapter.param_checker([(service_id, str)], [trackergroup_id]):
            params = {
                "serviceId": service_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/trackergroup",
                return_type=GetListSdwanServiceTrackergroupPayload,
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
