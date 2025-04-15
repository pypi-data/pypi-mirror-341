# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdroutingServiceObjectTrackerFeaturePostRequest,
    CreateSdroutingServiceObjectTrackerFeaturePostResponse,
    EditSdroutingServiceObjectTrackerFeaturePutRequest,
    EditSdroutingServiceObjectTrackerFeaturePutResponse,
    GetListSdRoutingServiceObjecttrackerPayload,
    GetSingleSdRoutingServiceObjecttrackerPayload,
)


class ObjecttrackerBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/service/{serviceId}/objecttracker
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, service_id: str, payload: CreateSdroutingServiceObjectTrackerFeaturePostRequest, **kw
    ) -> CreateSdroutingServiceObjectTrackerFeaturePostResponse:
        """
        Create a SD-Routing object tracker feature from a specific service feature profile
        POST /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/objecttracker

        :param service_id: Service Profile ID
        :param payload: SD-Routing object tracker feature from a specific service feature profile
        :returns: CreateSdroutingServiceObjectTrackerFeaturePostResponse
        """
        params = {
            "serviceId": service_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/objecttracker",
            return_type=CreateSdroutingServiceObjectTrackerFeaturePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        service_id: str,
        object_tracker_id: str,
        payload: EditSdroutingServiceObjectTrackerFeaturePutRequest,
        **kw,
    ) -> EditSdroutingServiceObjectTrackerFeaturePutResponse:
        """
        Edit the SD-Routing object tracker feature from a specific service feature profile
        PUT /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/objecttracker/{objectTrackerId}

        :param service_id: Service Profile ID
        :param object_tracker_id: Object Tracker Feature ID
        :param payload: SD-Routing object tracker feature from a specific service feature profile
        :returns: EditSdroutingServiceObjectTrackerFeaturePutResponse
        """
        params = {
            "serviceId": service_id,
            "objectTrackerId": object_tracker_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/objecttracker/{objectTrackerId}",
            return_type=EditSdroutingServiceObjectTrackerFeaturePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, service_id: str, object_tracker_id: str, **kw):
        """
        Delete the SD-Routing object tracker feature from a specific service feature profile
        DELETE /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/objecttracker/{objectTrackerId}

        :param service_id: Service Profile ID
        :param object_tracker_id: Object Tracker Feature ID
        :returns: None
        """
        params = {
            "serviceId": service_id,
            "objectTrackerId": object_tracker_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/objecttracker/{objectTrackerId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, service_id: str, object_tracker_id: str, **kw
    ) -> GetSingleSdRoutingServiceObjecttrackerPayload:
        """
        Get the SD-Routing object tracker feature from a specific service feature profile
        GET /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/objecttracker/{objectTrackerId}

        :param service_id: Service Profile ID
        :param object_tracker_id: Object Tracker Feature ID
        :returns: GetSingleSdRoutingServiceObjecttrackerPayload
        """
        ...

    @overload
    def get(self, service_id: str, **kw) -> GetListSdRoutingServiceObjecttrackerPayload:
        """
        Get all SD-Routing object tracker features from a specific service feature profile
        GET /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/objecttracker

        :param service_id: Service Profile ID
        :returns: GetListSdRoutingServiceObjecttrackerPayload
        """
        ...

    def get(
        self, service_id: str, object_tracker_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdRoutingServiceObjecttrackerPayload, GetSingleSdRoutingServiceObjecttrackerPayload
    ]:
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/objecttracker/{objectTrackerId}
        if self._request_adapter.param_checker([(service_id, str), (object_tracker_id, str)], []):
            params = {
                "serviceId": service_id,
                "objectTrackerId": object_tracker_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/objecttracker/{objectTrackerId}",
                return_type=GetSingleSdRoutingServiceObjecttrackerPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/objecttracker
        if self._request_adapter.param_checker([(service_id, str)], [object_tracker_id]):
            params = {
                "serviceId": service_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/objecttracker",
                return_type=GetListSdRoutingServiceObjecttrackerPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
