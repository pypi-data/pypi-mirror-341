# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateNfvirtualOvsNetworkParcelPostRequest,
    CreateNfvirtualOvsNetworkParcelPostResponse,
    EditNfvirtualOvsNetworkParcelPutRequest,
    EditNfvirtualOvsNetworkParcelPutResponse,
    GetSingleNfvirtualNetworksOvsnetworkPayload,
)


class OvsnetworkBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/nfvirtual/networks/ovsnetwork
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, networks_id: str, payload: CreateNfvirtualOvsNetworkParcelPostRequest, **kw
    ) -> CreateNfvirtualOvsNetworkParcelPostResponse:
        """
        Create OVS Network Profile Parcel for Networks feature profile
        POST /dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/ovsnetwork

        :param networks_id: Feature Profile ID
        :param payload: OVS Network Profile Parcel
        :returns: CreateNfvirtualOvsNetworkParcelPostResponse
        """
        params = {
            "networksId": networks_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/ovsnetwork",
            return_type=CreateNfvirtualOvsNetworkParcelPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        networks_id: str,
        ovs_network_id: str,
        payload: EditNfvirtualOvsNetworkParcelPutRequest,
        **kw,
    ) -> EditNfvirtualOvsNetworkParcelPutResponse:
        """
        Edit a OVS Network Profile Parcel for Networks feature profile
        PUT /dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/ovsnetwork/{ovsNetworkId}

        :param networks_id: Feature Profile ID
        :param ovs_network_id: Profile Parcel ID
        :param payload: OVS Network Profile Parcel
        :returns: EditNfvirtualOvsNetworkParcelPutResponse
        """
        params = {
            "networksId": networks_id,
            "ovsNetworkId": ovs_network_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/ovsnetwork/{ovsNetworkId}",
            return_type=EditNfvirtualOvsNetworkParcelPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, networks_id: str, ovs_network_id: str, **kw):
        """
        Delete a OVS Network Profile Parcel for Networks feature profile
        DELETE /dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/ovsnetwork/{ovsNetworkId}

        :param networks_id: Feature Profile ID
        :param ovs_network_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "networksId": networks_id,
            "ovsNetworkId": ovs_network_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/ovsnetwork/{ovsNetworkId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, *, network_id: str, details: bool, **kw
    ) -> GetSingleNfvirtualNetworksOvsnetworkPayload:
        """
        Get all Nfvirtual OVS Networks Feature Profile with networkId
        GET /dataservice/v1/feature-profile/nfvirtual/networks/ovsnetwork/{networkId}

        :param network_id: Feature Profile Id
        :param details: get feature details
        :returns: GetSingleNfvirtualNetworksOvsnetworkPayload
        """
        ...

    @overload
    def get(
        self, *, networks_id: str, ovs_network_id: str, **kw
    ) -> GetSingleNfvirtualNetworksOvsnetworkPayload:
        """
        Get OVS Network Profile Parcels for Networks feature profile
        GET /dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/ovsnetwork/{ovsNetworkId}

        :param networks_id: Feature Profile ID
        :param ovs_network_id: Profile Parcel ID
        :returns: GetSingleNfvirtualNetworksOvsnetworkPayload
        """
        ...

    def get(
        self,
        *,
        network_id: Optional[str] = None,
        details: Optional[bool] = None,
        networks_id: Optional[str] = None,
        ovs_network_id: Optional[str] = None,
        **kw,
    ) -> GetSingleNfvirtualNetworksOvsnetworkPayload:
        # /dataservice/v1/feature-profile/nfvirtual/networks/ovsnetwork/{networkId}
        if self._request_adapter.param_checker(
            [(network_id, str), (details, bool)], [networks_id, ovs_network_id]
        ):
            params = {
                "networkId": network_id,
                "details": details,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/nfvirtual/networks/ovsnetwork/{networkId}",
                return_type=GetSingleNfvirtualNetworksOvsnetworkPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/ovsnetwork/{ovsNetworkId}
        if self._request_adapter.param_checker(
            [(networks_id, str), (ovs_network_id, str)], [network_id, details]
        ):
            params = {
                "networksId": networks_id,
                "ovsNetworkId": ovs_network_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/ovsnetwork/{ovsNetworkId}",
                return_type=GetSingleNfvirtualNetworksOvsnetworkPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
