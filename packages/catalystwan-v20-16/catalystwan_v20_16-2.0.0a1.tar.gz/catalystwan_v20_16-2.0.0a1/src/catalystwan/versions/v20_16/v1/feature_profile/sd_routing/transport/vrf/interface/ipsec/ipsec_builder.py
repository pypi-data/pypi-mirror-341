# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdroutingTransportVrfInterfaceIpsecFeatureForTransportPostRequest,
    CreateSdroutingTransportVrfInterfaceIpsecFeatureForTransportPostResponse,
    EditSdroutingTransportVrfInterfaceIpsecFeatureForTransportPutRequest,
    EditSdroutingTransportVrfInterfaceIpsecFeatureForTransportPutResponse,
    GetListSdRoutingTransportVrfWanInterfaceIpsecPayload,
    GetSingleSdRoutingTransportVrfWanInterfaceIpsecPayload,
)


class IpsecBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/interface/ipsec
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        transport_id: str,
        vrf_id: str,
        payload: CreateSdroutingTransportVrfInterfaceIpsecFeatureForTransportPostRequest,
        **kw,
    ) -> CreateSdroutingTransportVrfInterfaceIpsecFeatureForTransportPostResponse:
        """
        Create a SD-Routing IPSec interface feature in a specific transport VRF from a specific transport feature profile
        POST /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/interface/ipsec

        :param transport_id: Transport Profile ID
        :param vrf_id: Transport VRF Feature ID
        :param payload:  IPSec interface feature in a specific transport VRF from a specific transport feature profile
        :returns: CreateSdroutingTransportVrfInterfaceIpsecFeatureForTransportPostResponse
        """
        params = {
            "transportId": transport_id,
            "vrfId": vrf_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/interface/ipsec",
            return_type=CreateSdroutingTransportVrfInterfaceIpsecFeatureForTransportPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        transport_id: str,
        vrf_id: str,
        ipsec_id: str,
        payload: EditSdroutingTransportVrfInterfaceIpsecFeatureForTransportPutRequest,
        **kw,
    ) -> EditSdroutingTransportVrfInterfaceIpsecFeatureForTransportPutResponse:
        """
        Edit the SD-Routing IPSec interface feature in a specific transport VRF from a specific transport feature profile
        PUT /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/interface/ipsec/{ipsecId}

        :param transport_id: Transport Profile ID
        :param vrf_id: Transport VRF Feature ID
        :param ipsec_id: IPSec Interface Feature ID
        :param payload:  IPSec interface feature in a specific transport VRF from a specific transport feature profile
        :returns: EditSdroutingTransportVrfInterfaceIpsecFeatureForTransportPutResponse
        """
        params = {
            "transportId": transport_id,
            "vrfId": vrf_id,
            "ipsecId": ipsec_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/interface/ipsec/{ipsecId}",
            return_type=EditSdroutingTransportVrfInterfaceIpsecFeatureForTransportPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, vrf_id: str, ipsec_id: str, **kw):
        """
        Delete the SD-Routing IPSec interface feature in a specific transport VRF from a specific transport feature profile
        DELETE /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/interface/ipsec/{ipsecId}

        :param transport_id: Transport Profile ID
        :param vrf_id: Transport VRF feature ID
        :param ipsec_id: IPSec Interface Feature ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "vrfId": vrf_id,
            "ipsecId": ipsec_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/interface/ipsec/{ipsecId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, vrf_id: str, ipsec_id: str, **kw
    ) -> GetSingleSdRoutingTransportVrfWanInterfaceIpsecPayload:
        """
        Get the SD-Routing IPSec interface feature in a specific transport VRF from a specific transport feature profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/interface/ipsec/{ipsecId}

        :param transport_id: Transport Profile ID
        :param vrf_id: Transport VRF Feature ID
        :param ipsec_id: IPSec Interface Feature ID
        :returns: GetSingleSdRoutingTransportVrfWanInterfaceIpsecPayload
        """
        ...

    @overload
    def get(
        self, transport_id: str, vrf_id: str, **kw
    ) -> GetListSdRoutingTransportVrfWanInterfaceIpsecPayload:
        """
        Get all  IPSec interface features in a specific transport VRF from a specific transport feature profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/interface/ipsec

        :param transport_id: Transport Profile ID
        :param vrf_id: Transport VRF Feature ID
        :returns: GetListSdRoutingTransportVrfWanInterfaceIpsecPayload
        """
        ...

    def get(
        self, transport_id: str, vrf_id: str, ipsec_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdRoutingTransportVrfWanInterfaceIpsecPayload,
        GetSingleSdRoutingTransportVrfWanInterfaceIpsecPayload,
    ]:
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/interface/ipsec/{ipsecId}
        if self._request_adapter.param_checker(
            [(transport_id, str), (vrf_id, str), (ipsec_id, str)], []
        ):
            params = {
                "transportId": transport_id,
                "vrfId": vrf_id,
                "ipsecId": ipsec_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/interface/ipsec/{ipsecId}",
                return_type=GetSingleSdRoutingTransportVrfWanInterfaceIpsecPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/interface/ipsec
        if self._request_adapter.param_checker([(transport_id, str), (vrf_id, str)], [ipsec_id]):
            params = {
                "transportId": transport_id,
                "vrfId": vrf_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/vrf/{vrfId}/interface/ipsec",
                return_type=GetListSdRoutingTransportVrfWanInterfaceIpsecPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
