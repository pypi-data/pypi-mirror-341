# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdroutingServiceObjectTrackerGroupFeaturePostRequest,
    CreateSdroutingServiceObjectTrackerGroupFeaturePostResponse,
    EditSdroutingServiceObjectTrackerGroupFeaturePutRequest,
    EditSdroutingServiceObjectTrackerGroupFeaturePutResponse,
    GetListSdRoutingServiceObjecttrackergroupPayload,
    GetSingleSdRoutingServiceObjecttrackergroupPayload,
)


class ObjecttrackergroupBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/service/{serviceId}/objecttrackergroup
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        service_id: str,
        payload: CreateSdroutingServiceObjectTrackerGroupFeaturePostRequest,
        **kw,
    ) -> CreateSdroutingServiceObjectTrackerGroupFeaturePostResponse:
        """
        Create a SD-Routing object tracker group feature from a specific service feature profile
        POST /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/objecttrackergroup

        :param service_id: Service Profile ID
        :param payload: SD-Routing object tracker group feature from a specific service feature profile
        :returns: CreateSdroutingServiceObjectTrackerGroupFeaturePostResponse
        """
        params = {
            "serviceId": service_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/objecttrackergroup",
            return_type=CreateSdroutingServiceObjectTrackerGroupFeaturePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        service_id: str,
        object_tracker_group_id: str,
        payload: EditSdroutingServiceObjectTrackerGroupFeaturePutRequest,
        **kw,
    ) -> EditSdroutingServiceObjectTrackerGroupFeaturePutResponse:
        """
        Edit the SD-Routing object tracker group feature from a specific service feature profile
        PUT /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/objecttrackergroup/{objectTrackerGroupId}

        :param service_id: Service Profile ID
        :param object_tracker_group_id: Object Tracker Group Feature ID
        :param payload: SD-Routing object tracker group feature from a specific service feature profile
        :returns: EditSdroutingServiceObjectTrackerGroupFeaturePutResponse
        """
        params = {
            "serviceId": service_id,
            "objectTrackerGroupId": object_tracker_group_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/objecttrackergroup/{objectTrackerGroupId}",
            return_type=EditSdroutingServiceObjectTrackerGroupFeaturePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, service_id: str, object_tracker_group_id: str, **kw):
        """
        Delete the SD-Routing object tracker group feature from a specific service feature profile
        DELETE /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/objecttrackergroup/{objectTrackerGroupId}

        :param service_id: Service Profile ID
        :param object_tracker_group_id: Object Tracker Group Feature ID
        :returns: None
        """
        params = {
            "serviceId": service_id,
            "objectTrackerGroupId": object_tracker_group_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/objecttrackergroup/{objectTrackerGroupId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, service_id: str, object_tracker_group_id: str, **kw
    ) -> GetSingleSdRoutingServiceObjecttrackergroupPayload:
        """
        Get the SD-Routing object tracker group feature from a specific service feature profile
        GET /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/objecttrackergroup/{objectTrackerGroupId}

        :param service_id: Service Profile ID
        :param object_tracker_group_id: Object Tracker Group Feature ID
        :returns: GetSingleSdRoutingServiceObjecttrackergroupPayload
        """
        ...

    @overload
    def get(self, service_id: str, **kw) -> GetListSdRoutingServiceObjecttrackergroupPayload:
        """
        Get all SD-Routing object tracker group features from a specific service feature profile
        GET /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/objecttrackergroup

        :param service_id: Service Profile ID
        :returns: GetListSdRoutingServiceObjecttrackergroupPayload
        """
        ...

    def get(
        self, service_id: str, object_tracker_group_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdRoutingServiceObjecttrackergroupPayload,
        GetSingleSdRoutingServiceObjecttrackergroupPayload,
    ]:
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/objecttrackergroup/{objectTrackerGroupId}
        if self._request_adapter.param_checker(
            [(service_id, str), (object_tracker_group_id, str)], []
        ):
            params = {
                "serviceId": service_id,
                "objectTrackerGroupId": object_tracker_group_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/objecttrackergroup/{objectTrackerGroupId}",
                return_type=GetSingleSdRoutingServiceObjecttrackergroupPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/objecttrackergroup
        if self._request_adapter.param_checker([(service_id, str)], [object_tracker_group_id]):
            params = {
                "serviceId": service_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/objecttrackergroup",
                return_type=GetListSdRoutingServiceObjecttrackergroupPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
