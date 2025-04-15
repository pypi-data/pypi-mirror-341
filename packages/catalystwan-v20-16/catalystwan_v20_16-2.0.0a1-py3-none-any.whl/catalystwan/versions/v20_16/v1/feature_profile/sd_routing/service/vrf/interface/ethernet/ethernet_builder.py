# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdroutingServiceVrfInterfaceEthernetFeatureForServicePostRequest,
    CreateSdroutingServiceVrfInterfaceEthernetFeatureForServicePostResponse,
    EditSdroutingServiceVrfInterfaceEthernetFeatureForServicePutRequest,
    EditSdroutingServiceVrfInterfaceEthernetFeatureForServicePutResponse,
    GetListSdRoutingServiceVrfLanInterfaceEthernetPayload,
    GetSingleSdRoutingServiceVrfLanInterfaceEthernetPayload,
)

if TYPE_CHECKING:
    from .dhcp_server.dhcp_server_builder import DhcpServerBuilder


class EthernetBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/interface/ethernet
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        service_id: str,
        vrf_id: str,
        payload: CreateSdroutingServiceVrfInterfaceEthernetFeatureForServicePostRequest,
        **kw,
    ) -> CreateSdroutingServiceVrfInterfaceEthernetFeatureForServicePostResponse:
        """
        Create a SD-Routing ethernet interface feature from a specific service VRF feature in service feature profile
        POST /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/interface/ethernet

        :param service_id: Service Profile ID
        :param vrf_id: VRF Feature ID
        :param payload: SD-Routing ethernet interface feature from a specific service VRF feature
        :returns: CreateSdroutingServiceVrfInterfaceEthernetFeatureForServicePostResponse
        """
        params = {
            "serviceId": service_id,
            "vrfId": vrf_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/interface/ethernet",
            return_type=CreateSdroutingServiceVrfInterfaceEthernetFeatureForServicePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        service_id: str,
        vrf_id: str,
        ethernet_id: str,
        payload: EditSdroutingServiceVrfInterfaceEthernetFeatureForServicePutRequest,
        **kw,
    ) -> EditSdroutingServiceVrfInterfaceEthernetFeatureForServicePutResponse:
        """
        Edit the SD-Routing ethernet interface feature from a specific service VRF feature in service feature profile
        PUT /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/interface/ethernet/{ethernetId}

        :param service_id: Service Profile ID
        :param vrf_id: VRF Feature ID
        :param ethernet_id: Interface Feature ID
        :param payload: SD-Routing ethernet interface feature from a specific service VRF feature
        :returns: EditSdroutingServiceVrfInterfaceEthernetFeatureForServicePutResponse
        """
        params = {
            "serviceId": service_id,
            "vrfId": vrf_id,
            "ethernetId": ethernet_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/interface/ethernet/{ethernetId}",
            return_type=EditSdroutingServiceVrfInterfaceEthernetFeatureForServicePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, service_id: str, vrf_id: str, ethernet_id: str, **kw):
        """
        Delete the SD-Routing ethernet interface feature from a specific service VRF feature in service feature profile
        DELETE /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/interface/ethernet/{ethernetId}

        :param service_id: Service Profile ID
        :param vrf_id: VRF Feature ID
        :param ethernet_id: Interface Feature ID
        :returns: None
        """
        params = {
            "serviceId": service_id,
            "vrfId": vrf_id,
            "ethernetId": ethernet_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/interface/ethernet/{ethernetId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, service_id: str, vrf_id: str, ethernet_id: str, **kw
    ) -> GetSingleSdRoutingServiceVrfLanInterfaceEthernetPayload:
        """
        Get the SD-Routing ethernet interface feature from a specific service VRF feature by feature ID in service feature profile
        GET /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/interface/ethernet/{ethernetId}

        :param service_id: Service Profile ID
        :param vrf_id: VRF Feature ID
        :param ethernet_id: Interface Feature ID
        :returns: GetSingleSdRoutingServiceVrfLanInterfaceEthernetPayload
        """
        ...

    @overload
    def get(
        self, service_id: str, vrf_id: str, **kw
    ) -> GetListSdRoutingServiceVrfLanInterfaceEthernetPayload:
        """
        Get all ethernet interface features from a specific service VRF feature in service feature profile
        GET /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/interface/ethernet

        :param service_id: Service Profile ID
        :param vrf_id: VRF Feature ID
        :returns: GetListSdRoutingServiceVrfLanInterfaceEthernetPayload
        """
        ...

    def get(
        self, service_id: str, vrf_id: str, ethernet_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdRoutingServiceVrfLanInterfaceEthernetPayload,
        GetSingleSdRoutingServiceVrfLanInterfaceEthernetPayload,
    ]:
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/interface/ethernet/{ethernetId}
        if self._request_adapter.param_checker(
            [(service_id, str), (vrf_id, str), (ethernet_id, str)], []
        ):
            params = {
                "serviceId": service_id,
                "vrfId": vrf_id,
                "ethernetId": ethernet_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/interface/ethernet/{ethernetId}",
                return_type=GetSingleSdRoutingServiceVrfLanInterfaceEthernetPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/interface/ethernet
        if self._request_adapter.param_checker([(service_id, str), (vrf_id, str)], [ethernet_id]):
            params = {
                "serviceId": service_id,
                "vrfId": vrf_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/service/{serviceId}/vrf/{vrfId}/interface/ethernet",
                return_type=GetListSdRoutingServiceVrfLanInterfaceEthernetPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def dhcp_server(self) -> DhcpServerBuilder:
        """
        The dhcp-server property
        """
        from .dhcp_server.dhcp_server_builder import DhcpServerBuilder

        return DhcpServerBuilder(self._request_adapter)
