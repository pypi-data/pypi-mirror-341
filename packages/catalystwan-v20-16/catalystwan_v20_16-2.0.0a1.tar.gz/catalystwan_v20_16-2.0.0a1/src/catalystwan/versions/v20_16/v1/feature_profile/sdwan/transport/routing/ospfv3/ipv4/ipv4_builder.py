# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateRoutingOspfv3Ipv4AfProfileParcelForTransportPostRequest,
    CreateRoutingOspfv3Ipv4AfProfileParcelForTransportPostResponse,
    EditRoutingOspfv3Ipv4AfProfileParcelForTransportPutRequest,
    EditRoutingOspfv3Ipv4AfProfileParcelForTransportPutResponse,
    GetListSdwanTransportRoutingOspfv3Ipv4Payload,
    GetSingleSdwanTransportRoutingOspfv3Ipv4Payload,
)


class Ipv4Builder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/transport/{transportId}/routing/ospfv3/ipv4
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        transport_id: str,
        payload: CreateRoutingOspfv3Ipv4AfProfileParcelForTransportPostRequest,
        **kw,
    ) -> CreateRoutingOspfv3Ipv4AfProfileParcelForTransportPostResponse:
        """
        Create a routing OSPFv3 IPv4 address family profile parcel for transport feature profile
        POST /dataservice/v1/feature-profile/sdwan/transport/{transportId}/routing/ospfv3/ipv4

        :param transport_id: Feature Profile ID
        :param payload: Routing Ospfv3 IPv4 Address Family Profile Parcel
        :returns: CreateRoutingOspfv3Ipv4AfProfileParcelForTransportPostResponse
        """
        params = {
            "transportId": transport_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/routing/ospfv3/ipv4",
            return_type=CreateRoutingOspfv3Ipv4AfProfileParcelForTransportPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        transport_id: str,
        ospfv3_id: str,
        payload: EditRoutingOspfv3Ipv4AfProfileParcelForTransportPutRequest,
        **kw,
    ) -> EditRoutingOspfv3Ipv4AfProfileParcelForTransportPutResponse:
        """
        Update a routing OSPFv3 IPv4 address family profile parcel for transport feature profile
        PUT /dataservice/v1/feature-profile/sdwan/transport/{transportId}/routing/ospfv3/ipv4/{ospfv3Id}

        :param transport_id: Feature Profile ID
        :param ospfv3_id: Profile Parcel ID
        :param payload: Routing Ospfv3 IPv4 Address Family Profile Parcel
        :returns: EditRoutingOspfv3Ipv4AfProfileParcelForTransportPutResponse
        """
        params = {
            "transportId": transport_id,
            "ospfv3Id": ospfv3_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/routing/ospfv3/ipv4/{ospfv3Id}",
            return_type=EditRoutingOspfv3Ipv4AfProfileParcelForTransportPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, ospfv3_id: str, **kw):
        """
        Delete the routing OSPFv3 IPv4 address family profile parcel by ID for transport feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/transport/{transportId}/routing/ospfv3/ipv4/{ospfv3Id}

        :param transport_id: Feature Profile ID
        :param ospfv3_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "ospfv3Id": ospfv3_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/routing/ospfv3/ipv4/{ospfv3Id}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, ospfv3_id: str, **kw
    ) -> GetSingleSdwanTransportRoutingOspfv3Ipv4Payload:
        """
        Get the routing OSPFv3 IPv4 address family profile parcel by ID for transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/routing/ospfv3/ipv4/{ospfv3Id}

        :param transport_id: Feature Profile ID
        :param ospfv3_id: Profile Parcel ID
        :returns: GetSingleSdwanTransportRoutingOspfv3Ipv4Payload
        """
        ...

    @overload
    def get(self, transport_id: str, **kw) -> GetListSdwanTransportRoutingOspfv3Ipv4Payload:
        """
        Get all routing OSPFv3 IPv4 address family profile parcels for transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/routing/ospfv3/ipv4

        :param transport_id: Feature Profile ID
        :returns: GetListSdwanTransportRoutingOspfv3Ipv4Payload
        """
        ...

    def get(
        self, transport_id: str, ospfv3_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdwanTransportRoutingOspfv3Ipv4Payload,
        GetSingleSdwanTransportRoutingOspfv3Ipv4Payload,
    ]:
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/routing/ospfv3/ipv4/{ospfv3Id}
        if self._request_adapter.param_checker([(transport_id, str), (ospfv3_id, str)], []):
            params = {
                "transportId": transport_id,
                "ospfv3Id": ospfv3_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/routing/ospfv3/ipv4/{ospfv3Id}",
                return_type=GetSingleSdwanTransportRoutingOspfv3Ipv4Payload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/routing/ospfv3/ipv4
        if self._request_adapter.param_checker([(transport_id, str)], [ospfv3_id]):
            params = {
                "transportId": transport_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/routing/ospfv3/ipv4",
                return_type=GetListSdwanTransportRoutingOspfv3Ipv4Payload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
