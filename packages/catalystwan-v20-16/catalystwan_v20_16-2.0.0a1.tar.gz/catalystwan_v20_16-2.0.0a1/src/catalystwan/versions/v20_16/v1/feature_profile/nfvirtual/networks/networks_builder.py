# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateNfvirtualNetworksFeatureProfilePostRequest,
    CreateNfvirtualNetworksFeatureProfilePostResponse,
    EditNfvirtualNetworksFeatureProfilePutRequest,
    EditNfvirtualNetworksFeatureProfilePutResponse,
    GetAllNfvirtualNetworksFeatureProfilesGetResponse,
    GetSingleNfvirtualNetworksPayload,
)

if TYPE_CHECKING:
    from .lan.lan_builder import LanBuilder
    from .ovsnetwork.ovsnetwork_builder import OvsnetworkBuilder
    from .routes.routes_builder import RoutesBuilder
    from .switch.switch_builder import SwitchBuilder
    from .vnf_attributes.vnf_attributes_builder import VnfAttributesBuilder
    from .wan.wan_builder import WanBuilder


class NetworksBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/nfvirtual/networks
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, payload: CreateNfvirtualNetworksFeatureProfilePostRequest, **kw
    ) -> CreateNfvirtualNetworksFeatureProfilePostResponse:
        """
        Create a nfvirtual Networks Feature Profile
        POST /dataservice/v1/feature-profile/nfvirtual/networks

        :param payload: Nfvirtual Feature profile
        :returns: CreateNfvirtualNetworksFeatureProfilePostResponse
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/nfvirtual/networks",
            return_type=CreateNfvirtualNetworksFeatureProfilePostResponse,
            payload=payload,
            **kw,
        )

    def put(
        self, network_id: str, payload: EditNfvirtualNetworksFeatureProfilePutRequest, **kw
    ) -> EditNfvirtualNetworksFeatureProfilePutResponse:
        """
        Edit a Nfvirtual Networks Feature Profile
        PUT /dataservice/v1/feature-profile/nfvirtual/networks/{networkId}

        :param network_id: Feature Profile ID
        :param payload: Nfvirtual Feature profile
        :returns: EditNfvirtualNetworksFeatureProfilePutResponse
        """
        params = {
            "networkId": network_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/nfvirtual/networks/{networkId}",
            return_type=EditNfvirtualNetworksFeatureProfilePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, network_id: str, **kw):
        """
        Delete a Nfvirtual Networks Feature Profile
        DELETE /dataservice/v1/feature-profile/nfvirtual/networks/{networkId}

        :param network_id: Network id
        :returns: None
        """
        params = {
            "networkId": network_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/nfvirtual/networks/{networkId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, *, offset: int, limit: int, **kw
    ) -> List[GetAllNfvirtualNetworksFeatureProfilesGetResponse]:
        """
        Get all Nfvirtual Feature Profiles
        GET /dataservice/v1/feature-profile/nfvirtual/networks

        :param offset: Pagination offset
        :param limit: Pagination limit
        :returns: List[GetAllNfvirtualNetworksFeatureProfilesGetResponse]
        """
        ...

    @overload
    def get(self, *, network_id: str, details: bool, **kw) -> GetSingleNfvirtualNetworksPayload:
        """
        Get a Nfvirtual Networks Feature Profile with networkId
        GET /dataservice/v1/feature-profile/nfvirtual/networks/{networkId}

        :param network_id: Feature Profile ID
        :param details: get feature details
        :returns: GetSingleNfvirtualNetworksPayload
        """
        ...

    def get(
        self,
        *,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        network_id: Optional[str] = None,
        details: Optional[bool] = None,
        **kw,
    ) -> Union[
        List[GetAllNfvirtualNetworksFeatureProfilesGetResponse], GetSingleNfvirtualNetworksPayload
    ]:
        # /dataservice/v1/feature-profile/nfvirtual/networks
        if self._request_adapter.param_checker(
            [(offset, int), (limit, int)], [network_id, details]
        ):
            params = {
                "offset": offset,
                "limit": limit,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/nfvirtual/networks",
                return_type=List[GetAllNfvirtualNetworksFeatureProfilesGetResponse],
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/nfvirtual/networks/{networkId}
        if self._request_adapter.param_checker(
            [(network_id, str), (details, bool)], [offset, limit]
        ):
            params = {
                "networkId": network_id,
                "details": details,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/nfvirtual/networks/{networkId}",
                return_type=GetSingleNfvirtualNetworksPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def lan(self) -> LanBuilder:
        """
        The lan property
        """
        from .lan.lan_builder import LanBuilder

        return LanBuilder(self._request_adapter)

    @property
    def ovsnetwork(self) -> OvsnetworkBuilder:
        """
        The ovsnetwork property
        """
        from .ovsnetwork.ovsnetwork_builder import OvsnetworkBuilder

        return OvsnetworkBuilder(self._request_adapter)

    @property
    def routes(self) -> RoutesBuilder:
        """
        The routes property
        """
        from .routes.routes_builder import RoutesBuilder

        return RoutesBuilder(self._request_adapter)

    @property
    def switch(self) -> SwitchBuilder:
        """
        The switch property
        """
        from .switch.switch_builder import SwitchBuilder

        return SwitchBuilder(self._request_adapter)

    @property
    def vnf_attributes(self) -> VnfAttributesBuilder:
        """
        The vnf-attributes property
        """
        from .vnf_attributes.vnf_attributes_builder import VnfAttributesBuilder

        return VnfAttributesBuilder(self._request_adapter)

    @property
    def wan(self) -> WanBuilder:
        """
        The wan property
        """
        from .wan.wan_builder import WanBuilder

        return WanBuilder(self._request_adapter)
