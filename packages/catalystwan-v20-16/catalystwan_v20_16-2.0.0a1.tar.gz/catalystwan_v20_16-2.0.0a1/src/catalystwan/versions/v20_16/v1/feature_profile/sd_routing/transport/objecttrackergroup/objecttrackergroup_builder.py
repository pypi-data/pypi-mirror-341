# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdroutingTransportObjectTrackerGroupFeaturePostRequest,
    CreateSdroutingTransportObjectTrackerGroupFeaturePostResponse,
    EditSdroutingTransportObjectTrackerGroupFeaturePutRequest,
    EditSdroutingTransportObjectTrackerGroupFeaturePutResponse,
    GetListSdRoutingTransportObjecttrackergroupPayload,
    GetSingleSdRoutingTransportObjecttrackergroupPayload,
)


class ObjecttrackergroupBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/transport/{transportId}/objecttrackergroup
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        transport_id: str,
        payload: CreateSdroutingTransportObjectTrackerGroupFeaturePostRequest,
        **kw,
    ) -> CreateSdroutingTransportObjectTrackerGroupFeaturePostResponse:
        """
        Create a SD-Routing object tracker group feature from a specific transport feature profile
        POST /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/objecttrackergroup

        :param transport_id: Transport Profile ID
        :param payload: SD-Routing object tracker group feature from a specific transport feature profile
        :returns: CreateSdroutingTransportObjectTrackerGroupFeaturePostResponse
        """
        params = {
            "transportId": transport_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/objecttrackergroup",
            return_type=CreateSdroutingTransportObjectTrackerGroupFeaturePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        transport_id: str,
        object_tracker_group_id: str,
        payload: EditSdroutingTransportObjectTrackerGroupFeaturePutRequest,
        **kw,
    ) -> EditSdroutingTransportObjectTrackerGroupFeaturePutResponse:
        """
        Edit the SD-Routing object tracker group feature from a specific transport feature profile
        PUT /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/objecttrackergroup/{objectTrackerGroupId}

        :param transport_id: Transport Profile ID
        :param object_tracker_group_id: Object Tracker Group ID
        :param payload: SD-Routing object tracker group feature from a specific transport feature profile
        :returns: EditSdroutingTransportObjectTrackerGroupFeaturePutResponse
        """
        params = {
            "transportId": transport_id,
            "objectTrackerGroupId": object_tracker_group_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/objecttrackergroup/{objectTrackerGroupId}",
            return_type=EditSdroutingTransportObjectTrackerGroupFeaturePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, object_tracker_group_id: str, **kw):
        """
        Delete the SD-Routing object tracker group feature from a specific transport feature profile
        DELETE /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/objecttrackergroup/{objectTrackerGroupId}

        :param transport_id: Transport Profile ID
        :param object_tracker_group_id: Object Tracker Group ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "objectTrackerGroupId": object_tracker_group_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/objecttrackergroup/{objectTrackerGroupId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, object_tracker_group_id: str, **kw
    ) -> GetSingleSdRoutingTransportObjecttrackergroupPayload:
        """
        Get the SD-Routing object tracker group feature from a specific transport feature profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/objecttrackergroup/{objectTrackerGroupId}

        :param transport_id: Transport Profile ID
        :param object_tracker_group_id: Object Tracker Group ID
        :returns: GetSingleSdRoutingTransportObjecttrackergroupPayload
        """
        ...

    @overload
    def get(self, transport_id: str, **kw) -> GetListSdRoutingTransportObjecttrackergroupPayload:
        """
        Get all SD-Routing object tracker group features from a specific transport feature profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/objecttrackergroup

        :param transport_id: Transport Profile ID
        :returns: GetListSdRoutingTransportObjecttrackergroupPayload
        """
        ...

    def get(
        self, transport_id: str, object_tracker_group_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdRoutingTransportObjecttrackergroupPayload,
        GetSingleSdRoutingTransportObjecttrackergroupPayload,
    ]:
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/objecttrackergroup/{objectTrackerGroupId}
        if self._request_adapter.param_checker(
            [(transport_id, str), (object_tracker_group_id, str)], []
        ):
            params = {
                "transportId": transport_id,
                "objectTrackerGroupId": object_tracker_group_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/objecttrackergroup/{objectTrackerGroupId}",
                return_type=GetSingleSdRoutingTransportObjecttrackergroupPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/objecttrackergroup
        if self._request_adapter.param_checker([(transport_id, str)], [object_tracker_group_id]):
            params = {
                "transportId": transport_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/objecttrackergroup",
                return_type=GetListSdRoutingTransportObjecttrackergroupPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
