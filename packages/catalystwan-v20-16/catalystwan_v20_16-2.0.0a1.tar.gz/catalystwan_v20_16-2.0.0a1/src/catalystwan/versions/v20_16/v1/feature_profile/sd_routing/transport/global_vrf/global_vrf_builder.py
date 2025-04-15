# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdroutingTransportGlobalVrfFeaturePostRequest,
    CreateSdroutingTransportGlobalVrfFeaturePostResponse,
    EditSdroutingTransportGlobalVrfFeaturePutRequest,
    EditSdroutingTransportGlobalVrfFeaturePutResponse,
    GetListSdRoutingTransportGlobalVrfPayload,
    GetSingleSdRoutingTransportGlobalVrfPayload,
)

if TYPE_CHECKING:
    from .interface.interface_builder import InterfaceBuilder
    from .multicloud_connection.multicloud_connection_builder import MulticloudConnectionBuilder
    from .routing.routing_builder import RoutingBuilder


class GlobalVrfBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/transport/{transportId}/global-vrf
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, transport_id: str, payload: CreateSdroutingTransportGlobalVrfFeaturePostRequest, **kw
    ) -> CreateSdroutingTransportGlobalVrfFeaturePostResponse:
        """
        Create a SD-Routing Global VRF feature from a specific transport feature profile
        POST /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf

        :param transport_id: Transport Profile ID
        :param payload:  Global VRF feature from a specific transport feature profile
        :returns: CreateSdroutingTransportGlobalVrfFeaturePostResponse
        """
        params = {
            "transportId": transport_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf",
            return_type=CreateSdroutingTransportGlobalVrfFeaturePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        transport_id: str,
        vrf_id: str,
        payload: EditSdroutingTransportGlobalVrfFeaturePutRequest,
        **kw,
    ) -> EditSdroutingTransportGlobalVrfFeaturePutResponse:
        """
        Edit the SD-Routing Global VRF feature from a specific transport feature profile
        PUT /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}

        :param transport_id: Transport Profile ID
        :param vrf_id: Global VRF Feature ID
        :param payload:  Global VRF feature from a specific transport feature profile
        :returns: EditSdroutingTransportGlobalVrfFeaturePutResponse
        """
        params = {
            "transportId": transport_id,
            "vrfId": vrf_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}",
            return_type=EditSdroutingTransportGlobalVrfFeaturePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, vrf_id: str, **kw):
        """
        Delete the SD-Routing Global VRF feature from a specific transport feature profile
        DELETE /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}

        :param transport_id: Transport Profile ID
        :param vrf_id: Global VRF Feature ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "vrfId": vrf_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, vrf_id: str, **kw
    ) -> GetSingleSdRoutingTransportGlobalVrfPayload:
        """
        Get the SD-Routing Global VRF feature from a specific transport feature profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}

        :param transport_id: Transport Profile ID
        :param vrf_id: Global VRF Feature ID
        :returns: GetSingleSdRoutingTransportGlobalVrfPayload
        """
        ...

    @overload
    def get(self, transport_id: str, **kw) -> GetListSdRoutingTransportGlobalVrfPayload:
        """
        Get all SD-Routing Global VRF features from a specific transport feature profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf

        :param transport_id: Transport Profile ID
        :returns: GetListSdRoutingTransportGlobalVrfPayload
        """
        ...

    def get(
        self, transport_id: str, vrf_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdRoutingTransportGlobalVrfPayload, GetSingleSdRoutingTransportGlobalVrfPayload
    ]:
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}
        if self._request_adapter.param_checker([(transport_id, str), (vrf_id, str)], []):
            params = {
                "transportId": transport_id,
                "vrfId": vrf_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf/{vrfId}",
                return_type=GetSingleSdRoutingTransportGlobalVrfPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf
        if self._request_adapter.param_checker([(transport_id, str)], [vrf_id]):
            params = {
                "transportId": transport_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/global-vrf",
                return_type=GetListSdRoutingTransportGlobalVrfPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def interface(self) -> InterfaceBuilder:
        """
        The interface property
        """
        from .interface.interface_builder import InterfaceBuilder

        return InterfaceBuilder(self._request_adapter)

    @property
    def multicloud_connection(self) -> MulticloudConnectionBuilder:
        """
        The multicloud-connection property
        """
        from .multicloud_connection.multicloud_connection_builder import MulticloudConnectionBuilder

        return MulticloudConnectionBuilder(self._request_adapter)

    @property
    def routing(self) -> RoutingBuilder:
        """
        The routing property
        """
        from .routing.routing_builder import RoutingBuilder

        return RoutingBuilder(self._request_adapter)
