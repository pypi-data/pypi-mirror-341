# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateNfvirtualVnfParcelPostRequest,
    CreateNfvirtualVnfParcelPostResponse,
    EditNfvirtualVnfParcelPutRequest,
    EditNfvirtualVnfParcelPutResponse,
    GetSingleNfvirtualNetworksVnfAttributesVnfPayload,
)


class VnfBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/nfvirtual/networks/{networksId}/vnf-attributes/{vnfAttributesId}/vnf
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        networks_id: str,
        vnf_attributes_id: str,
        payload: CreateNfvirtualVnfParcelPostRequest,
        **kw,
    ) -> CreateNfvirtualVnfParcelPostResponse:
        """
        Create VNF Profile Parcel for Networks feature profile
        POST /dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/vnf-attributes/{vnfAttributesId}/vnf

        :param networks_id: Feature Profile ID
        :param vnf_attributes_id: Profile Parcel ID
        :param payload: VNF config Profile Parcel
        :returns: CreateNfvirtualVnfParcelPostResponse
        """
        params = {
            "networksId": networks_id,
            "vnfAttributesId": vnf_attributes_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/vnf-attributes/{vnfAttributesId}/vnf",
            return_type=CreateNfvirtualVnfParcelPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def get(
        self, networks_id: str, vnf_attributes_id: str, vnf_id: str, **kw
    ) -> GetSingleNfvirtualNetworksVnfAttributesVnfPayload:
        """
        Get VNF Profile Parcels for Networks feature profile
        GET /dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/vnf-attributes/{vnfAttributesId}/vnf/{vnfId}

        :param networks_id: Feature Profile ID
        :param vnf_attributes_id: Profile Parcel ID
        :param vnf_id: VNF Parcel ID
        :returns: GetSingleNfvirtualNetworksVnfAttributesVnfPayload
        """
        params = {
            "networksId": networks_id,
            "vnfAttributesId": vnf_attributes_id,
            "vnfId": vnf_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/vnf-attributes/{vnfAttributesId}/vnf/{vnfId}",
            return_type=GetSingleNfvirtualNetworksVnfAttributesVnfPayload,
            params=params,
            **kw,
        )

    def put(
        self,
        networks_id: str,
        vnf_attributes_id: str,
        vnf_id: str,
        payload: EditNfvirtualVnfParcelPutRequest,
        **kw,
    ) -> EditNfvirtualVnfParcelPutResponse:
        """
        Edit a VNF Profile Parcel for networks feature profile
        PUT /dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/vnf-attributes/{vnfAttributesId}/vnf/{vnfId}

        :param networks_id: Feature Profile ID
        :param vnf_attributes_id: Profile Parcel ID
        :param vnf_id: VNF Parcel ID
        :param payload: VNF Profile Parcel
        :returns: EditNfvirtualVnfParcelPutResponse
        """
        params = {
            "networksId": networks_id,
            "vnfAttributesId": vnf_attributes_id,
            "vnfId": vnf_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/vnf-attributes/{vnfAttributesId}/vnf/{vnfId}",
            return_type=EditNfvirtualVnfParcelPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, networks_id: str, vnf_attributes_id: str, vnf_id: str, **kw):
        """
        Delete a VNF Profile Parcel for Networks feature profile
        DELETE /dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/vnf-attributes/{vnfAttributesId}/vnf/{vnfId}

        :param networks_id: Feature Profile ID
        :param vnf_attributes_id: Profile Parcel ID
        :param vnf_id: VNF Parcel ID
        :returns: None
        """
        params = {
            "networksId": networks_id,
            "vnfAttributesId": vnf_attributes_id,
            "vnfId": vnf_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/nfvirtual/networks/{networksId}/vnf-attributes/{vnfAttributesId}/vnf/{vnfId}",
            params=params,
            **kw,
        )
