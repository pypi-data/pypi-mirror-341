# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateWanVpnInterfaceSerialParcelForTransportPostRequest,
    CreateWanVpnInterfaceSerialParcelForTransportPostResponse,
    EditWanVpnInterfaceSerialParcelForTransportPutRequest,
    EditWanVpnInterfaceSerialParcelForTransportPutResponse,
    GetListSdwanTransportWanVpnInterfaceSerialPayload,
    GetSingleSdwanTransportWanVpnInterfaceSerialPayload,
)

if TYPE_CHECKING:
    from .schema.schema_builder import SchemaBuilder


class SerialBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/transport/wan/vpn/interface/serial
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        transport_id: str,
        vpn_id: str,
        payload: CreateWanVpnInterfaceSerialParcelForTransportPostRequest,
        **kw,
    ) -> CreateWanVpnInterfaceSerialParcelForTransportPostResponse:
        """
        Create a WanVpn InterfaceSerial parcel for transport feature profile
        POST /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/serial

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param payload: Wan Vpn Interface Serial Profile Parcel
        :returns: CreateWanVpnInterfaceSerialParcelForTransportPostResponse
        """
        params = {
            "transportId": transport_id,
            "vpnId": vpn_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/serial",
            return_type=CreateWanVpnInterfaceSerialParcelForTransportPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        transport_id: str,
        vpn_id: str,
        serial_id: str,
        payload: EditWanVpnInterfaceSerialParcelForTransportPutRequest,
        **kw,
    ) -> EditWanVpnInterfaceSerialParcelForTransportPutResponse:
        """
        Update a WanVpn InterfaceSerial Parcel for transport feature profile
        PUT /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/serial/{serialId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param serial_id: Interface ID
        :param payload: Wan Vpn Interface Serial Profile Parcel
        :returns: EditWanVpnInterfaceSerialParcelForTransportPutResponse
        """
        params = {
            "transportId": transport_id,
            "vpnId": vpn_id,
            "serialId": serial_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/serial/{serialId}",
            return_type=EditWanVpnInterfaceSerialParcelForTransportPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, vpn_id: str, serial_id: str, **kw):
        """
        Delete a  WanVpn InterfaceSerial Parcel for transport feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/serial/{serialId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param serial_id: Interface Parcel ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "vpnId": vpn_id,
            "serialId": serial_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/serial/{serialId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, vpn_id: str, serial_id: str, **kw
    ) -> GetSingleSdwanTransportWanVpnInterfaceSerialPayload:
        """
        Get WanVpn InterfaceSerial Parcel by serialId for transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/serial/{serialId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param serial_id: Interface Parcel ID
        :returns: GetSingleSdwanTransportWanVpnInterfaceSerialPayload
        """
        ...

    @overload
    def get(
        self, transport_id: str, vpn_id: str, **kw
    ) -> GetListSdwanTransportWanVpnInterfaceSerialPayload:
        """
        Get InterfaceSerial Parcels for transport WanVpn Parcel
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/serial

        :param transport_id: Feature Profile ID
        :param vpn_id: Feature Parcel ID
        :returns: GetListSdwanTransportWanVpnInterfaceSerialPayload
        """
        ...

    def get(
        self, transport_id: str, vpn_id: str, serial_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdwanTransportWanVpnInterfaceSerialPayload,
        GetSingleSdwanTransportWanVpnInterfaceSerialPayload,
    ]:
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/serial/{serialId}
        if self._request_adapter.param_checker(
            [(transport_id, str), (vpn_id, str), (serial_id, str)], []
        ):
            params = {
                "transportId": transport_id,
                "vpnId": vpn_id,
                "serialId": serial_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/serial/{serialId}",
                return_type=GetSingleSdwanTransportWanVpnInterfaceSerialPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/serial
        if self._request_adapter.param_checker([(transport_id, str), (vpn_id, str)], [serial_id]):
            params = {
                "transportId": transport_id,
                "vpnId": vpn_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/serial",
                return_type=GetListSdwanTransportWanVpnInterfaceSerialPayload,
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
