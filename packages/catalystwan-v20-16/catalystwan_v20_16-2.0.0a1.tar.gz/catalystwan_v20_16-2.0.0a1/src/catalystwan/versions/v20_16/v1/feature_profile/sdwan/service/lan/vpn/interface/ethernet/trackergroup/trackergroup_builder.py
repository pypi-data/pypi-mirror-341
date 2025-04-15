# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateLanVpnInterfaceEthernetAndTrackerGroupParcelAssociationForTransportPostRequest,
    CreateLanVpnInterfaceEthernetAndTrackerGroupParcelAssociationForTransportPostResponse,
    EditLanVpnInterfaceEthernetAndTrackerGroupParcelAssociationForTransportPutRequest,
    EditLanVpnInterfaceEthernetAndTrackerGroupParcelAssociationForTransportPutResponse,
    GetLanVpnInterfaceEthernetAssociatedTrackerGroupParcelsForTransportGetResponse,
    GetSingleSdwanServiceLanVpnInterfaceEthernetTrackergroupPayload,
)


class TrackergroupBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ethernet/{ethernetId}/trackergroup
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def put(
        self,
        service_id: str,
        vpn_id: str,
        ethernet_id: str,
        trackergroup_id: str,
        payload: EditLanVpnInterfaceEthernetAndTrackerGroupParcelAssociationForTransportPutRequest,
        **kw,
    ) -> EditLanVpnInterfaceEthernetAndTrackerGroupParcelAssociationForTransportPutResponse:
        """
        Update a LanVpnInterfaceEthernet parcel and a TrackerGroup Parcel association for service feature profile
        PUT /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ethernet/{ethernetId}/trackergroup/{trackergroupId}

        :param service_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ethernet_id: Interface Profile Parcel ID
        :param trackergroup_id: TrackerGroup ID
        :param payload: TrackerGroup Profile Parcel
        :returns: EditLanVpnInterfaceEthernetAndTrackerGroupParcelAssociationForTransportPutResponse
        """
        params = {
            "serviceId": service_id,
            "vpnId": vpn_id,
            "ethernetId": ethernet_id,
            "trackergroupId": trackergroup_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ethernet/{ethernetId}/trackergroup/{trackergroupId}",
            return_type=EditLanVpnInterfaceEthernetAndTrackerGroupParcelAssociationForTransportPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, service_id: str, vpn_id: str, ethernet_id: str, trackergroup_id: str, **kw):
        """
        Delete a LanVpnInterfaceEthernet and a TrackerGroup Parcel association for service feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ethernet/{ethernetId}/trackergroup/{trackergroupId}

        :param service_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ethernet_id: Interface Profile Parcel ID
        :param trackergroup_id: TrackerGroup Parcel ID
        :returns: None
        """
        params = {
            "serviceId": service_id,
            "vpnId": vpn_id,
            "ethernetId": ethernet_id,
            "trackergroupId": trackergroup_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ethernet/{ethernetId}/trackergroup/{trackergroupId}",
            params=params,
            **kw,
        )

    def post(
        self,
        service_id: str,
        vpn_parcel_id: str,
        ethernet_id: str,
        payload: CreateLanVpnInterfaceEthernetAndTrackerGroupParcelAssociationForTransportPostRequest,
        **kw,
    ) -> CreateLanVpnInterfaceEthernetAndTrackerGroupParcelAssociationForTransportPostResponse:
        """
        Associate a LanVpnInterfaceEthernet parcel with a TrackerGroup Parcel for service feature profile
        POST /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnParcelId}/interface/ethernet/{ethernetId}/trackergroup

        :param service_id: Feature Profile ID
        :param vpn_parcel_id: VPN Profile Parcel ID
        :param ethernet_id: Interface Profile Parcel ID
        :param payload: TrackerGroup Profile Parcel Id
        :returns: CreateLanVpnInterfaceEthernetAndTrackerGroupParcelAssociationForTransportPostResponse
        """
        params = {
            "serviceId": service_id,
            "vpnParcelId": vpn_parcel_id,
            "ethernetId": ethernet_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnParcelId}/interface/ethernet/{ethernetId}/trackergroup",
            return_type=CreateLanVpnInterfaceEthernetAndTrackerGroupParcelAssociationForTransportPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    @overload
    def get(
        self, service_id: str, vpn_id: str, ethernet_id: str, trackergroup_id: str, **kw
    ) -> GetSingleSdwanServiceLanVpnInterfaceEthernetTrackergroupPayload:
        """
        Get LanVpnInterfaceEthernet associated TrackerGroup Parcel by trackergroupId for service feature profile
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ethernet/{ethernetId}/trackergroup/{trackergroupId}

        :param service_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param ethernet_id: Interface Profile Parcel ID
        :param trackergroup_id: TrackerGroup Parcel ID
        :returns: GetSingleSdwanServiceLanVpnInterfaceEthernetTrackergroupPayload
        """
        ...

    @overload
    def get(
        self, service_id: str, vpn_id: str, ethernet_id: str, **kw
    ) -> List[GetLanVpnInterfaceEthernetAssociatedTrackerGroupParcelsForTransportGetResponse]:
        """
        Get LanVpnInterfaceEthernet associated TrackerGroup Parcels for service feature profile
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ethernet/{ethernetId}/trackergroup

        :param service_id: Feature Profile ID
        :param vpn_id: Feature Parcel ID
        :param ethernet_id: Interface Profile Parcel ID
        :returns: List[GetLanVpnInterfaceEthernetAssociatedTrackerGroupParcelsForTransportGetResponse]
        """
        ...

    def get(
        self,
        service_id: str,
        vpn_id: str,
        ethernet_id: str,
        trackergroup_id: Optional[str] = None,
        **kw,
    ) -> Union[
        List[GetLanVpnInterfaceEthernetAssociatedTrackerGroupParcelsForTransportGetResponse],
        GetSingleSdwanServiceLanVpnInterfaceEthernetTrackergroupPayload,
    ]:
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ethernet/{ethernetId}/trackergroup/{trackergroupId}
        if self._request_adapter.param_checker(
            [(service_id, str), (vpn_id, str), (ethernet_id, str), (trackergroup_id, str)], []
        ):
            params = {
                "serviceId": service_id,
                "vpnId": vpn_id,
                "ethernetId": ethernet_id,
                "trackergroupId": trackergroup_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ethernet/{ethernetId}/trackergroup/{trackergroupId}",
                return_type=GetSingleSdwanServiceLanVpnInterfaceEthernetTrackergroupPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ethernet/{ethernetId}/trackergroup
        if self._request_adapter.param_checker(
            [(service_id, str), (vpn_id, str), (ethernet_id, str)], [trackergroup_id]
        ):
            params = {
                "serviceId": service_id,
                "vpnId": vpn_id,
                "ethernetId": ethernet_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/ethernet/{ethernetId}/trackergroup",
                return_type=List[
                    GetLanVpnInterfaceEthernetAssociatedTrackerGroupParcelsForTransportGetResponse
                ],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
