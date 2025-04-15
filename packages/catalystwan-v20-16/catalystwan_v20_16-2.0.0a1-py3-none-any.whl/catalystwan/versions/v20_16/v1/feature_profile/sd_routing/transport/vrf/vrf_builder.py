# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdroutingTransportVrfFeaturePostRequest,
    CreateSdroutingTransportVrfFeaturePostResponse,
    EditSdroutingTransportVrfFeaturePutRequest,
    EditSdroutingTransportVrfFeaturePutResponse,
    GetListSdRoutingTransportVrfPayload,
    GetSingleSdRoutingTransportVrfPayload,
)

if TYPE_CHECKING:
    from .interface.interface_builder import InterfaceBuilder
    from .routing.routing_builder import RoutingBuilder


class VrfBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/transport/{transportId}/vrf
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, transport_id: str, payload: CreateSdroutingTransportVrfFeaturePostRequest, **kw
    ) -> CreateSdroutingTransportVrfFeaturePostResponse:
        """
        Create a SD-Routing VRF feature from a specific transport feature profile
        POST /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf

        :param transport_id: Transport Profile ID
        :param payload:  VRF feature from a specific transport feature profile
        :returns: CreateSdroutingTransportVrfFeaturePostResponse
        """
        params = {
            "transportId": transport_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf",
            return_type=CreateSdroutingTransportVrfFeaturePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        transport_id: str,
        vrf_id: str,
        payload: EditSdroutingTransportVrfFeaturePutRequest,
        **kw,
    ) -> EditSdroutingTransportVrfFeaturePutResponse:
        """
        Edit the SD-Routing VRF feature from a specific transport feature profile
        PUT /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}

        :param transport_id: Transport Profile ID
        :param vrf_id: VRF Feature ID
        :param payload:  VRF feature from a specific transport feature profile
        :returns: EditSdroutingTransportVrfFeaturePutResponse
        """
        params = {
            "transportId": transport_id,
            "vrfId": vrf_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}",
            return_type=EditSdroutingTransportVrfFeaturePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, vrf_id: str, **kw):
        """
        Delete the SD-Routing VRF feature from a specific transport feature profile
        DELETE /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}

        :param transport_id: Transport Profile ID
        :param vrf_id: VRF Feature ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "vrfId": vrf_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}",
            params=params,
            **kw,
        )

    @overload
    def get(self, transport_id: str, vrf_id: str, **kw) -> GetSingleSdRoutingTransportVrfPayload:
        """
        Get the SD-Routing VRF feature from a specific transport feature profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}

        :param transport_id: Transport Profile ID
        :param vrf_id: VRF Feature ID
        :returns: GetSingleSdRoutingTransportVrfPayload
        """
        ...

    @overload
    def get(self, transport_id: str, **kw) -> GetListSdRoutingTransportVrfPayload:
        """
        Get all SD-Routing VRF features from a specific transport feature profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf

        :param transport_id: Transport Profile ID
        :returns: GetListSdRoutingTransportVrfPayload
        """
        ...

    def get(
        self, transport_id: str, vrf_id: Optional[str] = None, **kw
    ) -> Union[GetListSdRoutingTransportVrfPayload, GetSingleSdRoutingTransportVrfPayload]:
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}
        if self._request_adapter.param_checker([(transport_id, str), (vrf_id, str)], []):
            params = {
                "transportId": transport_id,
                "vrfId": vrf_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}",
                return_type=GetSingleSdRoutingTransportVrfPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf
        if self._request_adapter.param_checker([(transport_id, str)], [vrf_id]):
            params = {
                "transportId": transport_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf",
                return_type=GetListSdRoutingTransportVrfPayload,
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
    def routing(self) -> RoutingBuilder:
        """
        The routing property
        """
        from .routing.routing_builder import RoutingBuilder

        return RoutingBuilder(self._request_adapter)
