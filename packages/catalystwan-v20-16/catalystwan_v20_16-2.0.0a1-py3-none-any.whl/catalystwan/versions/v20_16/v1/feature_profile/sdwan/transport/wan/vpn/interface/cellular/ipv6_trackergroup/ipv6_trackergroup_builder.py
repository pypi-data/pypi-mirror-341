# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateWanVpnInterfaceCellularAndIpv6TrackerGroupParcelAssociationForTransportPostRequest,
    CreateWanVpnInterfaceCellularAndIpv6TrackerGroupParcelAssociationForTransportPostResponse,
    EditWanVpnInterfaceCellularAndIpv6TrackerGroupParcelAssociationForTransportPutRequest,
    EditWanVpnInterfaceCellularAndIpv6TrackerGroupParcelAssociationForTransportPutResponse,
    GetSingleSdwanTransportWanVpnInterfaceCellularIpv6TrackergroupPayload,
    GetWanVpnInterfaceCellularAssociatedIpv6TrackerGroupParcelsForTransportGetResponse,
)


class Ipv6TrackergroupBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular/{cellularId}/ipv6-trackergroup
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def put(
        self,
        transport_id: str,
        vpn_id: str,
        cellular_id: str,
        ipv6_trackergroup_id: str,
        payload: EditWanVpnInterfaceCellularAndIpv6TrackerGroupParcelAssociationForTransportPutRequest,
        **kw,
    ) -> EditWanVpnInterfaceCellularAndIpv6TrackerGroupParcelAssociationForTransportPutResponse:
        """
        Update a WanVpnInterfaceCellular parcel and a IPv6 TrackerGroup Parcel association for transport feature profile
        PUT /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular/{cellularId}/ipv6-trackergroup/{ipv6-trackergroupId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param cellular_id: Interface Profile Parcel ID
        :param ipv6_trackergroup_id: IPv6 TrackerGroup ID
        :param payload: IPv6 TrackerGroup Profile Parcel
        :returns: EditWanVpnInterfaceCellularAndIpv6TrackerGroupParcelAssociationForTransportPutResponse
        """
        params = {
            "transportId": transport_id,
            "vpnId": vpn_id,
            "cellularId": cellular_id,
            "ipv6-trackergroupId": ipv6_trackergroup_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular/{cellularId}/ipv6-trackergroup/{ipv6-trackergroupId}",
            return_type=EditWanVpnInterfaceCellularAndIpv6TrackerGroupParcelAssociationForTransportPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(
        self, transport_id: str, vpn_id: str, cellular_id: str, ipv6_trackergroup_id: str, **kw
    ):
        """
        Delete a WanVpnInterfaceCellular and a IPv6 TrackerGroup Parcel association for transport feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular/{cellularId}/ipv6-trackergroup/{ipv6-trackergroupId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param cellular_id: Interface Profile Parcel ID
        :param ipv6_trackergroup_id: TrackerGroup Parcel ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "vpnId": vpn_id,
            "cellularId": cellular_id,
            "ipv6-trackergroupId": ipv6_trackergroup_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular/{cellularId}/ipv6-trackergroup/{ipv6-trackergroupId}",
            params=params,
            **kw,
        )

    def post(
        self,
        transport_id: str,
        vpn_parcel_id: str,
        cellular_id: str,
        payload: CreateWanVpnInterfaceCellularAndIpv6TrackerGroupParcelAssociationForTransportPostRequest,
        **kw,
    ) -> CreateWanVpnInterfaceCellularAndIpv6TrackerGroupParcelAssociationForTransportPostResponse:
        """
        Associate a WanVpnInterfaceCellular parcel with a IPv6 TrackerGroup Parcel for transport feature profile
        POST /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnParcelId}/interface/cellular/{cellularId}/ipv6-trackergroup

        :param transport_id: Feature Profile ID
        :param vpn_parcel_id: VPN Profile Parcel ID
        :param cellular_id: Interface Profile Parcel ID
        :param payload: IPv6 TrackerGroup Profile Parcel Id
        :returns: CreateWanVpnInterfaceCellularAndIpv6TrackerGroupParcelAssociationForTransportPostResponse
        """
        params = {
            "transportId": transport_id,
            "vpnParcelId": vpn_parcel_id,
            "cellularId": cellular_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnParcelId}/interface/cellular/{cellularId}/ipv6-trackergroup",
            return_type=CreateWanVpnInterfaceCellularAndIpv6TrackerGroupParcelAssociationForTransportPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, vpn_id: str, cellular_id: str, ipv6_trackergroup_id: str, **kw
    ) -> GetSingleSdwanTransportWanVpnInterfaceCellularIpv6TrackergroupPayload:
        """
        Get WanVpnInterfaceCellular associated IPv6 TrackerGroup Parcel by ipv6-trackergroupId for transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular/{cellularId}/ipv6-trackergroup/{ipv6-trackergroupId}

        :param transport_id: Feature Profile ID
        :param vpn_id: Profile Parcel ID
        :param cellular_id: Interface Profile Parcel ID
        :param ipv6_trackergroup_id: TrackerGroup Parcel ID
        :returns: GetSingleSdwanTransportWanVpnInterfaceCellularIpv6TrackergroupPayload
        """
        ...

    @overload
    def get(
        self, transport_id: str, vpn_id: str, cellular_id: str, **kw
    ) -> List[GetWanVpnInterfaceCellularAssociatedIpv6TrackerGroupParcelsForTransportGetResponse]:
        """
        Get WanVpnInterfaceCellular associated IPv6 TrackerGroup Parcels for transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular/{cellularId}/ipv6-trackergroup

        :param transport_id: Feature Profile ID
        :param vpn_id: Feature Parcel ID
        :param cellular_id: Interface Profile Parcel ID
        :returns: List[GetWanVpnInterfaceCellularAssociatedIpv6TrackerGroupParcelsForTransportGetResponse]
        """
        ...

    def get(
        self,
        transport_id: str,
        vpn_id: str,
        cellular_id: str,
        ipv6_trackergroup_id: Optional[str] = None,
        **kw,
    ) -> Union[
        List[GetWanVpnInterfaceCellularAssociatedIpv6TrackerGroupParcelsForTransportGetResponse],
        GetSingleSdwanTransportWanVpnInterfaceCellularIpv6TrackergroupPayload,
    ]:
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular/{cellularId}/ipv6-trackergroup/{ipv6-trackergroupId}
        if self._request_adapter.param_checker(
            [(transport_id, str), (vpn_id, str), (cellular_id, str), (ipv6_trackergroup_id, str)],
            [],
        ):
            params = {
                "transportId": transport_id,
                "vpnId": vpn_id,
                "cellularId": cellular_id,
                "ipv6-trackergroupId": ipv6_trackergroup_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular/{cellularId}/ipv6-trackergroup/{ipv6-trackergroupId}",
                return_type=GetSingleSdwanTransportWanVpnInterfaceCellularIpv6TrackergroupPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular/{cellularId}/ipv6-trackergroup
        if self._request_adapter.param_checker(
            [(transport_id, str), (vpn_id, str), (cellular_id, str)], [ipv6_trackergroup_id]
        ):
            params = {
                "transportId": transport_id,
                "vpnId": vpn_id,
                "cellularId": cellular_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/wan/vpn/{vpnId}/interface/cellular/{cellularId}/ipv6-trackergroup",
                return_type=List[
                    GetWanVpnInterfaceCellularAssociatedIpv6TrackerGroupParcelsForTransportGetResponse
                ],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
