# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateMultiCloudConnectionPostRequest,
    CreateMultiCloudConnectionPostResponse,
    EditMultiCloudConnectionPutRequest,
    EditMultiCloudConnectionPutResponse,
    GetListSdRoutingServiceVrfLanMulticloudConnectionPayload,
    GetSingleSdRoutingServiceVrfLanMulticloudConnectionPayload,
)


class MulticloudConnectionBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/service/{serviceId}/multicloud-connection
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, service_id: str, payload: CreateMultiCloudConnectionPostRequest, **kw
    ) -> CreateMultiCloudConnectionPostResponse:
        """
        Associate a MultiCloudConnection Parcel for service feature profile
        POST /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/multicloud-connection

        :param service_id: Feature Profile ID
        :param payload: MultiConnection Extension Payload for defining the multicloud connection to the cloud gateway
        :returns: CreateMultiCloudConnectionPostResponse
        """
        params = {
            "serviceId": service_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/multicloud-connection",
            return_type=CreateMultiCloudConnectionPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        service_id: str,
        multi_cloud_connection_id: str,
        payload: EditMultiCloudConnectionPutRequest,
        **kw,
    ) -> EditMultiCloudConnectionPutResponse:
        """
        Update a multicloud connection parcel
        PUT /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/multicloud-connection/{multiCloudConnectionId}

        :param service_id: Feature Profile ID
        :param multi_cloud_connection_id: Profile Parcel ID
        :param payload: Multicloud Connection Profile Parcel
        :returns: EditMultiCloudConnectionPutResponse
        """
        params = {
            "serviceId": service_id,
            "multiCloudConnectionId": multi_cloud_connection_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/multicloud-connection/{multiCloudConnectionId}",
            return_type=EditMultiCloudConnectionPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, service_id: str, multi_cloud_connection_id: str, **kw):
        """
        Delete a MultiCloud Connection Profile Parcel for Service feature profile
        DELETE /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/multicloud-connection/{multiCloudConnectionId}

        :param service_id: Feature Profile ID
        :param multi_cloud_connection_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "serviceId": service_id,
            "multiCloudConnectionId": multi_cloud_connection_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/multicloud-connection/{multiCloudConnectionId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, service_id: str, multi_cloud_connection_id: str, **kw
    ) -> GetSingleSdRoutingServiceVrfLanMulticloudConnectionPayload:
        """
        Get a multicloud connection parcel
        GET /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/multicloud-connection/{multiCloudConnectionId}

        :param service_id: Feature Profile ID
        :param multi_cloud_connection_id: Profile Parcel ID
        :returns: GetSingleSdRoutingServiceVrfLanMulticloudConnectionPayload
        """
        ...

    @overload
    def get(
        self, service_id: str, **kw
    ) -> GetListSdRoutingServiceVrfLanMulticloudConnectionPayload:
        """
        Get Multicloud Connection Profile Parcels for Service feature profile
        GET /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/multicloud-connection

        :param service_id: Feature Profile ID
        :returns: GetListSdRoutingServiceVrfLanMulticloudConnectionPayload
        """
        ...

    def get(
        self, service_id: str, multi_cloud_connection_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdRoutingServiceVrfLanMulticloudConnectionPayload,
        GetSingleSdRoutingServiceVrfLanMulticloudConnectionPayload,
    ]:
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/multicloud-connection/{multiCloudConnectionId}
        if self._request_adapter.param_checker(
            [(service_id, str), (multi_cloud_connection_id, str)], []
        ):
            params = {
                "serviceId": service_id,
                "multiCloudConnectionId": multi_cloud_connection_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/multicloud-connection/{multiCloudConnectionId}",
                return_type=GetSingleSdRoutingServiceVrfLanMulticloudConnectionPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/multicloud-connection
        if self._request_adapter.param_checker([(service_id, str)], [multi_cloud_connection_id]):
            params = {
                "serviceId": service_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/multicloud-connection",
                return_type=GetListSdRoutingServiceVrfLanMulticloudConnectionPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
