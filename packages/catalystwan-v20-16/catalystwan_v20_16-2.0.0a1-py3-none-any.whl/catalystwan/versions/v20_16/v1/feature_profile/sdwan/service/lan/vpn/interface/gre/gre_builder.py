# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateLanVpnInterfaceGreForServicePostRequest,
    CreateLanVpnInterfaceGreForServicePostResponse,
    EditLanVpnInterfaceGreForServicePutRequest,
    EditLanVpnInterfaceGreForServicePutResponse,
    GetListSdwanServiceLanVpnInterfaceGrePayload,
    GetSingleSdwanServiceLanVpnInterfaceGrePayload,
)

if TYPE_CHECKING:
    from .schema.schema_builder import SchemaBuilder


class GreBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/service/lan/vpn/interface/gre
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        service_id: str,
        vpn_id: str,
        payload: CreateLanVpnInterfaceGreForServicePostRequest,
        **kw,
    ) -> CreateLanVpnInterfaceGreForServicePostResponse:
        """
        Create a LanVpn InterfaceGre for service feature profile
        POST /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/gre

        :param service_id: Feature Profile ID
        :param vpn_id: Vpn ID
        :param payload: Lan Vpn Interface Gre
        :returns: CreateLanVpnInterfaceGreForServicePostResponse
        """
        params = {
            "serviceId": service_id,
            "vpnId": vpn_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/gre",
            return_type=CreateLanVpnInterfaceGreForServicePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        service_id: str,
        vpn_id: str,
        gre_id: str,
        payload: EditLanVpnInterfaceGreForServicePutRequest,
        **kw,
    ) -> EditLanVpnInterfaceGreForServicePutResponse:
        """
        Update a LanVpn InterfaceGre Feature for service feature profile
        PUT /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/gre/{greId}

        :param service_id: Feature Profile ID
        :param vpn_id: Vpn ID
        :param gre_id: Interface ID
        :param payload: Lan Vpn Interface Gre
        :returns: EditLanVpnInterfaceGreForServicePutResponse
        """
        params = {
            "serviceId": service_id,
            "vpnId": vpn_id,
            "greId": gre_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/gre/{greId}",
            return_type=EditLanVpnInterfaceGreForServicePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, service_id: str, vpn_id: str, gre_id: str, **kw):
        """
        Delete a  LanVpn InterfaceGre for service feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/gre/{greId}

        :param service_id: Feature Profile ID
        :param vpn_id: Vpn ID
        :param gre_id: Gre ID
        :returns: None
        """
        params = {
            "serviceId": service_id,
            "vpnId": vpn_id,
            "greId": gre_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/gre/{greId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, service_id: str, vpn_id: str, gre_id: str, **kw
    ) -> GetSingleSdwanServiceLanVpnInterfaceGrePayload:
        """
        Get LanVpn InterfaceGre by greId for service feature profile
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/gre/{greId}

        :param service_id: Feature Profile ID
        :param vpn_id: Vpn ID
        :param gre_id: Gre ID
        :returns: GetSingleSdwanServiceLanVpnInterfaceGrePayload
        """
        ...

    @overload
    def get(
        self, service_id: str, vpn_id: str, **kw
    ) -> GetListSdwanServiceLanVpnInterfaceGrePayload:
        """
        Get InterfaceGre for service LanVpn
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/gre

        :param service_id: Feature Profile ID
        :param vpn_id: Vpn ID
        :returns: GetListSdwanServiceLanVpnInterfaceGrePayload
        """
        ...

    def get(
        self, service_id: str, vpn_id: str, gre_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdwanServiceLanVpnInterfaceGrePayload, GetSingleSdwanServiceLanVpnInterfaceGrePayload
    ]:
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/gre/{greId}
        if self._request_adapter.param_checker(
            [(service_id, str), (vpn_id, str), (gre_id, str)], []
        ):
            params = {
                "serviceId": service_id,
                "vpnId": vpn_id,
                "greId": gre_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/gre/{greId}",
                return_type=GetSingleSdwanServiceLanVpnInterfaceGrePayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/gre
        if self._request_adapter.param_checker([(service_id, str), (vpn_id, str)], [gre_id]):
            params = {
                "serviceId": service_id,
                "vpnId": vpn_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/interface/gre",
                return_type=GetListSdwanServiceLanVpnInterfaceGrePayload,
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
