# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateWanVpnInterfaceEthernetParcelForTransportPostRequest,
    CreateWanVpnInterfaceEthernetParcelForTransportPostResponse,
    EditWanVpnInterfaceEthernetParcelForTransportPutRequest,
    EditWanVpnInterfaceEthernetParcelForTransportPutResponse,
    GetListSdwanTransportWanVpnInterfaceEthernetPayload,
    GetSingleSdwanTransportWanVpnInterfaceEthernetPayload,
)

if TYPE_CHECKING:
    from .ipv6_tracker.ipv6_tracker_builder import Ipv6TrackerBuilder
    from .ipv6_trackergroup.ipv6_trackergroup_builder import Ipv6TrackergroupBuilder
    from .schema.schema_builder import SchemaBuilder
    from .tracker.tracker_builder import TrackerBuilder
    from .trackergroup.trackergroup_builder import TrackergroupBuilder


class EthernetBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/transport/wan/vpn/interface/ethernet
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        transport_id: str,
        vpn_id: str,
        payload: CreateWanVpnInterfaceEthernetParcelForTransportPostRequest,
        **kw,
    ) -> CreateWanVpnInterfaceEthernetParcelForTransportPostResponse:
        """
        Create a WanVpn InterfaceEthernet parcel for transport feature profile
        POST /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ethernet

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param payload: Wan Vpn Interface Ethernet Profile Parcel
        :returns: CreateWanVpnInterfaceEthernetParcelForTransportPostResponse
        """
        params = {
            "transportId": transport_id,
            "vpnId": vpn_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ethernet",
            return_type=CreateWanVpnInterfaceEthernetParcelForTransportPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        transport_id: str,
        vpn_id: str,
        ethernet_id: str,
        payload: EditWanVpnInterfaceEthernetParcelForTransportPutRequest,
        **kw,
    ) -> EditWanVpnInterfaceEthernetParcelForTransportPutResponse:
        """
        Update a WanVpn InterfaceEthernet Parcel for transport feature profile
        PUT /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ethernet/{ethernetId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ethernet_id: Interface ID
        :param payload: Wan Vpn Interface Ethernet Profile Parcel
        :returns: EditWanVpnInterfaceEthernetParcelForTransportPutResponse
        """
        params = {
            "transportId": transport_id,
            "vpnId": vpn_id,
            "ethernetId": ethernet_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ethernet/{ethernetId}",
            return_type=EditWanVpnInterfaceEthernetParcelForTransportPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, vpn_id: str, ethernet_id: str, **kw):
        """
        Delete a  WanVpn InterfaceEthernet Parcel for transport feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ethernet/{ethernetId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ethernet_id: Interface Parcel ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "vpnId": vpn_id,
            "ethernetId": ethernet_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ethernet/{ethernetId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, vpn_id: str, ethernet_id: str, **kw
    ) -> GetSingleSdwanTransportWanVpnInterfaceEthernetPayload:
        """
        Get WanVpn InterfaceEthernet Parcel by ethernetId for transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ethernet/{ethernetId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ethernet_id: Interface Parcel ID
        :returns: GetSingleSdwanTransportWanVpnInterfaceEthernetPayload
        """
        ...

    @overload
    def get(
        self, transport_id: str, vpn_id: str, **kw
    ) -> GetListSdwanTransportWanVpnInterfaceEthernetPayload:
        """
        Get InterfaceEthernet Parcels for transport WanVpn Parcel
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ethernet

        :param transport_id: Feature Profile ID
        :param vpn_id: Feature Parcel ID
        :returns: GetListSdwanTransportWanVpnInterfaceEthernetPayload
        """
        ...

    def get(
        self, transport_id: str, vpn_id: str, ethernet_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdwanTransportWanVpnInterfaceEthernetPayload,
        GetSingleSdwanTransportWanVpnInterfaceEthernetPayload,
    ]:
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ethernet/{ethernetId}
        if self._request_adapter.param_checker(
            [(transport_id, str), (vpn_id, str), (ethernet_id, str)], []
        ):
            params = {
                "transportId": transport_id,
                "vpnId": vpn_id,
                "ethernetId": ethernet_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ethernet/{ethernetId}",
                return_type=GetSingleSdwanTransportWanVpnInterfaceEthernetPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ethernet
        if self._request_adapter.param_checker([(transport_id, str), (vpn_id, str)], [ethernet_id]):
            params = {
                "transportId": transport_id,
                "vpnId": vpn_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/ethernet",
                return_type=GetListSdwanTransportWanVpnInterfaceEthernetPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def ipv6_tracker(self) -> Ipv6TrackerBuilder:
        """
        The ipv6-tracker property
        """
        from .ipv6_tracker.ipv6_tracker_builder import Ipv6TrackerBuilder

        return Ipv6TrackerBuilder(self._request_adapter)

    @property
    def ipv6_trackergroup(self) -> Ipv6TrackergroupBuilder:
        """
        The ipv6-trackergroup property
        """
        from .ipv6_trackergroup.ipv6_trackergroup_builder import Ipv6TrackergroupBuilder

        return Ipv6TrackergroupBuilder(self._request_adapter)

    @property
    def schema(self) -> SchemaBuilder:
        """
        The schema property
        """
        from .schema.schema_builder import SchemaBuilder

        return SchemaBuilder(self._request_adapter)

    @property
    def tracker(self) -> TrackerBuilder:
        """
        The tracker property
        """
        from .tracker.tracker_builder import TrackerBuilder

        return TrackerBuilder(self._request_adapter)

    @property
    def trackergroup(self) -> TrackergroupBuilder:
        """
        The trackergroup property
        """
        from .trackergroup.trackergroup_builder import TrackergroupBuilder

        return TrackergroupBuilder(self._request_adapter)
