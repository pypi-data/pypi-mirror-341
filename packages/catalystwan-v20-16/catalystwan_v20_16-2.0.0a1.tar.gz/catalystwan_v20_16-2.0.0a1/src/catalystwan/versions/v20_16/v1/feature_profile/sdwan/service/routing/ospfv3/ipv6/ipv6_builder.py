# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateRoutingOspfv3Ipv6AfProfileParcelForServicePostRequest,
    CreateRoutingOspfv3Ipv6AfProfileParcelForServicePostResponse,
    EditRoutingOspfv3IPv6AfProfileParcelForServicePutRequest,
    EditRoutingOspfv3IPv6AfProfileParcelForServicePutResponse,
    GetListSdwanServiceRoutingOspfv3Ipv6Payload,
    GetSingleSdwanServiceRoutingOspfv3Ipv6Payload,
)


class Ipv6Builder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/service/{serviceId}/routing/ospfv3/ipv6
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        service_id: str,
        payload: CreateRoutingOspfv3Ipv6AfProfileParcelForServicePostRequest,
        **kw,
    ) -> CreateRoutingOspfv3Ipv6AfProfileParcelForServicePostResponse:
        """
        Create a Routing OSPFv3 IPv6 Address Family Profile Parcel for Service feature profile
        POST /dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/ospfv3/ipv6

        :param service_id: Feature Profile ID
        :param payload: Routing OSPFv3 IPv6 Address Family Profile Parcel
        :returns: CreateRoutingOspfv3Ipv6AfProfileParcelForServicePostResponse
        """
        params = {
            "serviceId": service_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/ospfv3/ipv6",
            return_type=CreateRoutingOspfv3Ipv6AfProfileParcelForServicePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        service_id: str,
        ospfv3_id: str,
        payload: EditRoutingOspfv3IPv6AfProfileParcelForServicePutRequest,
        **kw,
    ) -> EditRoutingOspfv3IPv6AfProfileParcelForServicePutResponse:
        """
        Update a Routing OSPFv3 IPv6 Address Family Profile Parcel for Service feature profile
        PUT /dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/ospfv3/ipv6/{ospfv3Id}

        :param service_id: Feature Profile ID
        :param ospfv3_id: Profile Parcel ID
        :param payload: Routing OSPFv3 IPv6 Address Family Profile Parcel
        :returns: EditRoutingOspfv3IPv6AfProfileParcelForServicePutResponse
        """
        params = {
            "serviceId": service_id,
            "ospfv3Id": ospfv3_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/ospfv3/ipv6/{ospfv3Id}",
            return_type=EditRoutingOspfv3IPv6AfProfileParcelForServicePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, service_id: str, ospfv3_id: str, **kw):
        """
        Delete a Routing OSPFv3 IPv6 Address Family Profile Parcel for Service feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/ospfv3/ipv6/{ospfv3Id}

        :param service_id: Feature Profile ID
        :param ospfv3_id: Profile Parcel ID
        :returns: None
        """
        params = {
            "serviceId": service_id,
            "ospfv3Id": ospfv3_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/ospfv3/ipv6/{ospfv3Id}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, service_id: str, ospfv3_id: str, **kw
    ) -> GetSingleSdwanServiceRoutingOspfv3Ipv6Payload:
        """
        Get Routing OSPFv3 IPv6 Address Family Profile Parcel by parcelId for Service feature profile
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/ospfv3/ipv6/{ospfv3Id}

        :param service_id: Feature Profile ID
        :param ospfv3_id: Profile Parcel ID
        :returns: GetSingleSdwanServiceRoutingOspfv3Ipv6Payload
        """
        ...

    @overload
    def get(self, service_id: str, **kw) -> GetListSdwanServiceRoutingOspfv3Ipv6Payload:
        """
        Get Routing OSPFv3 IPv6 Address Family Profile Parcels for Service feature profile
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/ospfv3/ipv6

        :param service_id: Feature Profile ID
        :returns: GetListSdwanServiceRoutingOspfv3Ipv6Payload
        """
        ...

    def get(
        self, service_id: str, ospfv3_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdwanServiceRoutingOspfv3Ipv6Payload, GetSingleSdwanServiceRoutingOspfv3Ipv6Payload
    ]:
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/ospfv3/ipv6/{ospfv3Id}
        if self._request_adapter.param_checker([(service_id, str), (ospfv3_id, str)], []):
            params = {
                "serviceId": service_id,
                "ospfv3Id": ospfv3_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/ospfv3/ipv6/{ospfv3Id}",
                return_type=GetSingleSdwanServiceRoutingOspfv3Ipv6Payload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/ospfv3/ipv6
        if self._request_adapter.param_checker([(service_id, str)], [ospfv3_id]):
            params = {
                "serviceId": service_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/routing/ospfv3/ipv6",
                return_type=GetListSdwanServiceRoutingOspfv3Ipv6Payload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
