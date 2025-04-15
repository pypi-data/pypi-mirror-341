# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateWanVpnProfileParcelForTransportPostRequest,
    CreateWanVpnProfileParcelForTransportPostResponse,
    EditWanVpnProfileParcelForTransportPutRequest,
    EditWanVpnProfileParcelForTransportPutResponse,
    GetListSdwanTransportWanVpnPayload,
    GetSingleSdwanTransportWanVpnPayload,
)

if TYPE_CHECKING:
    from .interface.interface_builder import InterfaceBuilder
    from .routing.routing_builder import RoutingBuilder
    from .schema.schema_builder import SchemaBuilder


class VpnBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/transport/wan/vpn
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, transport_id: str, payload: CreateWanVpnProfileParcelForTransportPostRequest, **kw
    ) -> CreateWanVpnProfileParcelForTransportPostResponse:
        """
        Create a Wan Vpn Profile Parcel for Transport feature profile
        POST /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn

        :param transport_id: Feature Profile ID
        :param payload: Wan Vpn Profile Parcel
        :returns: CreateWanVpnProfileParcelForTransportPostResponse
        """
        params = {
            "transportId": transport_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn",
            return_type=CreateWanVpnProfileParcelForTransportPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        transport_id: str,
        vpn_id: str,
        payload: EditWanVpnProfileParcelForTransportPutRequest,
        **kw,
    ) -> EditWanVpnProfileParcelForTransportPutResponse:
        """
        Update a Wan Vpn Profile Parcel for Transport feature profile
        PUT /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param payload: Wan Vpn Profile Parcel
        :returns: EditWanVpnProfileParcelForTransportPutResponse
        """
        params = {
            "transportId": transport_id,
            "vpnId": vpn_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}",
            return_type=EditWanVpnProfileParcelForTransportPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, vpn_id: str, **kw):
        """
        Delete a Wan Vpn Profile Parcel for Transport feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "vpnId": vpn_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}",
            params=params,
            **kw,
        )

    @overload
    def get(self, transport_id: str, vpn_id: str, **kw) -> GetSingleSdwanTransportWanVpnPayload:
        """
        Get Wan Vpn Profile Parcel by parcelId for Transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :returns: GetSingleSdwanTransportWanVpnPayload
        """
        ...

    @overload
    def get(self, transport_id: str, **kw) -> GetListSdwanTransportWanVpnPayload:
        """
        Get Wan Vpn Profile Parcels for Transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn

        :param transport_id: Feature Profile ID
        :returns: GetListSdwanTransportWanVpnPayload
        """
        ...

    def get(
        self, transport_id: str, vpn_id: Optional[str] = None, **kw
    ) -> Union[GetListSdwanTransportWanVpnPayload, GetSingleSdwanTransportWanVpnPayload]:
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}
        if self._request_adapter.param_checker([(transport_id, str), (vpn_id, str)], []):
            params = {
                "transportId": transport_id,
                "vpnId": vpn_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}",
                return_type=GetSingleSdwanTransportWanVpnPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn
        if self._request_adapter.param_checker([(transport_id, str)], [vpn_id]):
            params = {
                "transportId": transport_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn",
                return_type=GetListSdwanTransportWanVpnPayload,
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

    @property
    def schema(self) -> SchemaBuilder:
        """
        The schema property
        """
        from .schema.schema_builder import SchemaBuilder

        return SchemaBuilder(self._request_adapter)
