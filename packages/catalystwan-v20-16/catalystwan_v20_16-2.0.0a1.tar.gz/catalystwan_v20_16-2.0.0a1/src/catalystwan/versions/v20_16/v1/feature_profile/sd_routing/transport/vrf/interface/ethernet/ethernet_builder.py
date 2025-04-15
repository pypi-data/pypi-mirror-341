# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdroutingTransportVrfInterfaceEthernetParcelForTransportPostRequest,
    CreateSdroutingTransportVrfInterfaceEthernetParcelForTransportPostResponse,
    EditSdroutingTransportVrfInterfaceEthernetParcelForTransportPutRequest,
    EditSdroutingTransportVrfInterfaceEthernetParcelForTransportPutResponse,
    GetListSdRoutingTransportVrfWanInterfaceEthernetPayload,
    GetSingleSdRoutingTransportVrfWanInterfaceEthernetPayload,
)


class EthernetBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/interface/ethernet
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        transport_id: str,
        vrf_id: str,
        payload: CreateSdroutingTransportVrfInterfaceEthernetParcelForTransportPostRequest,
        **kw,
    ) -> CreateSdroutingTransportVrfInterfaceEthernetParcelForTransportPostResponse:
        """
        Create a SD-Routing Ethernet interface feature from a specific transport VRF feature in Transport Feature Profile
        POST /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/interface/ethernet

        :param transport_id: Transport Profile ID
        :param vrf_id: VRF Feature ID
        :param payload: SD-Routing Ethernet interface feature from a specific transport VRF feature
        :returns: CreateSdroutingTransportVrfInterfaceEthernetParcelForTransportPostResponse
        """
        params = {
            "transportId": transport_id,
            "vrfId": vrf_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/interface/ethernet",
            return_type=CreateSdroutingTransportVrfInterfaceEthernetParcelForTransportPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        transport_id: str,
        vrf_id: str,
        ethernet_id: str,
        payload: EditSdroutingTransportVrfInterfaceEthernetParcelForTransportPutRequest,
        **kw,
    ) -> EditSdroutingTransportVrfInterfaceEthernetParcelForTransportPutResponse:
        """
        Edit the SD-Routing Ethernet interface feature from a specific transport VRF feature in Transport Feature Profile
        PUT /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/interface/ethernet/{ethernetId}

        :param transport_id: Transport Profile ID
        :param vrf_id: VRF Feature ID
        :param ethernet_id: Interface Feature ID
        :param payload: SD-Routing Ethernet interface feature from a specific transport VRF feature
        :returns: EditSdroutingTransportVrfInterfaceEthernetParcelForTransportPutResponse
        """
        params = {
            "transportId": transport_id,
            "vrfId": vrf_id,
            "ethernetId": ethernet_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/interface/ethernet/{ethernetId}",
            return_type=EditSdroutingTransportVrfInterfaceEthernetParcelForTransportPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, vrf_id: str, ethernet_id: str, **kw):
        """
        Delete the SD-Routing Ethernet interface feature from a specific transport VRF feature in Transport Feature Profile
        DELETE /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/interface/ethernet/{ethernetId}

        :param transport_id: Transport Profile ID
        :param vrf_id: VRF Feature ID
        :param ethernet_id: Interface Feature ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "vrfId": vrf_id,
            "ethernetId": ethernet_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/interface/ethernet/{ethernetId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, vrf_id: str, ethernet_id: str, **kw
    ) -> GetSingleSdRoutingTransportVrfWanInterfaceEthernetPayload:
        """
        Get the SD-Routing Ethernet interface feature from a specific transport VRF feature by ethernetId in Transport Feature Profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/interface/ethernet/{ethernetId}

        :param transport_id: Transport Profile ID
        :param vrf_id: VRF Feature ID
        :param ethernet_id: Interface Feature ID
        :returns: GetSingleSdRoutingTransportVrfWanInterfaceEthernetPayload
        """
        ...

    @overload
    def get(
        self, transport_id: str, vrf_id: str, **kw
    ) -> GetListSdRoutingTransportVrfWanInterfaceEthernetPayload:
        """
        Get all  Ethernet interface features for a specific transport VRF feature in Transport Feature Profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/interface/ethernet

        :param transport_id: Transport Profile ID
        :param vrf_id: VRF Feature ID
        :returns: GetListSdRoutingTransportVrfWanInterfaceEthernetPayload
        """
        ...

    def get(
        self, transport_id: str, vrf_id: str, ethernet_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdRoutingTransportVrfWanInterfaceEthernetPayload,
        GetSingleSdRoutingTransportVrfWanInterfaceEthernetPayload,
    ]:
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/interface/ethernet/{ethernetId}
        if self._request_adapter.param_checker(
            [(transport_id, str), (vrf_id, str), (ethernet_id, str)], []
        ):
            params = {
                "transportId": transport_id,
                "vrfId": vrf_id,
                "ethernetId": ethernet_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/interface/ethernet/{ethernetId}",
                return_type=GetSingleSdRoutingTransportVrfWanInterfaceEthernetPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/interface/ethernet
        if self._request_adapter.param_checker([(transport_id, str), (vrf_id, str)], [ethernet_id]):
            params = {
                "transportId": transport_id,
                "vrfId": vrf_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/interface/ethernet",
                return_type=GetListSdRoutingTransportVrfWanInterfaceEthernetPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
