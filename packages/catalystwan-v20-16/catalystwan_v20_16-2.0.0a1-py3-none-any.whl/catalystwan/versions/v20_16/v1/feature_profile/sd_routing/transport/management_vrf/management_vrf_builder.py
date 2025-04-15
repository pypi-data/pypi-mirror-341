# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdroutingManagementVrfFeaturePostRequest,
    CreateSdroutingManagementVrfFeaturePostResponse,
    EditSdroutingManagementVrfFeaturePutRequest,
    EditSdroutingManagementVrfFeaturePutResponse,
    GetListSdRoutingTransportManagementVrfPayload,
    GetSingleSdRoutingTransportManagementVrfPayload,
)

if TYPE_CHECKING:
    from .interface.interface_builder import InterfaceBuilder


class ManagementVrfBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/transport/{transportId}/management-vrf
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, transport_id: str, payload: CreateSdroutingManagementVrfFeaturePostRequest, **kw
    ) -> CreateSdroutingManagementVrfFeaturePostResponse:
        """
        Create a SD-Routing Management VRF feature from a specific transport feature profile
        POST /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/management-vrf

        :param transport_id: Transport Profile ID
        :param payload: SD-Routing Management VRF feature from a specific transport feature profile
        :returns: CreateSdroutingManagementVrfFeaturePostResponse
        """
        params = {
            "transportId": transport_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/management-vrf",
            return_type=CreateSdroutingManagementVrfFeaturePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        transport_id: str,
        vrf_id: str,
        payload: EditSdroutingManagementVrfFeaturePutRequest,
        **kw,
    ) -> EditSdroutingManagementVrfFeaturePutResponse:
        """
        Edit the SD-Routing Management VRF feature from a specific transport feature profile
        PUT /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/management-vrf/{vrfId}

        :param transport_id: Transport Profile ID
        :param vrf_id: Management VRF Feature ID
        :param payload: SD-Routing Management VRF feature from a specific transport feature profile
        :returns: EditSdroutingManagementVrfFeaturePutResponse
        """
        params = {
            "transportId": transport_id,
            "vrfId": vrf_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/management-vrf/{vrfId}",
            return_type=EditSdroutingManagementVrfFeaturePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, vrf_id: str, **kw):
        """
        Delete the SD-Routing Management VRF feature from a specific transport feature profile
        DELETE /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/management-vrf/{vrfId}

        :param transport_id: Transport Profile ID
        :param vrf_id: Management VRF Feature ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "vrfId": vrf_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/management-vrf/{vrfId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, vrf_id: str, **kw
    ) -> GetSingleSdRoutingTransportManagementVrfPayload:
        """
        Get the SD-Routing Management VRF feature from a specific transport feature profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/management-vrf/{vrfId}

        :param transport_id: Transport Profile ID
        :param vrf_id: Management VRF Feature ID
        :returns: GetSingleSdRoutingTransportManagementVrfPayload
        """
        ...

    @overload
    def get(self, transport_id: str, **kw) -> GetListSdRoutingTransportManagementVrfPayload:
        """
        Get all SD-Routing Management VRF features from a specific transport feature profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/management-vrf

        :param transport_id: Transport Profile ID
        :returns: GetListSdRoutingTransportManagementVrfPayload
        """
        ...

    def get(
        self, transport_id: str, vrf_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdRoutingTransportManagementVrfPayload,
        GetSingleSdRoutingTransportManagementVrfPayload,
    ]:
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/management-vrf/{vrfId}
        if self._request_adapter.param_checker([(transport_id, str), (vrf_id, str)], []):
            params = {
                "transportId": transport_id,
                "vrfId": vrf_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/management-vrf/{vrfId}",
                return_type=GetSingleSdRoutingTransportManagementVrfPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/management-vrf
        if self._request_adapter.param_checker([(transport_id, str)], [vrf_id]):
            params = {
                "transportId": transport_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/management-vrf",
                return_type=GetListSdRoutingTransportManagementVrfPayload,
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
