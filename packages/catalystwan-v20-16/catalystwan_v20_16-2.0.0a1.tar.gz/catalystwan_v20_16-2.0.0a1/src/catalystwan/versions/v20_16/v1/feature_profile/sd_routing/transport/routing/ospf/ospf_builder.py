# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateSdroutingTransportRoutingOspfFeaturePostRequest,
    CreateSdroutingTransportRoutingOspfFeaturePostResponse,
    EditSdroutingTransportRoutingOspfFeaturePutRequest,
    EditSdroutingTransportRoutingOspfFeaturePutResponse,
    GetListSdRoutingTransportRoutingOspfPayload,
    GetSingleSdRoutingTransportRoutingOspfPayload,
)


class OspfBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sd-routing/transport/{transportId}/routing/ospf
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        transport_id: str,
        payload: CreateSdroutingTransportRoutingOspfFeaturePostRequest,
        **kw,
    ) -> CreateSdroutingTransportRoutingOspfFeaturePostResponse:
        """
        Create a SD-Routing WAN OSPF feature from a specific transport feature profile
        POST /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/routing/ospf

        :param transport_id: Transport Profile ID
        :param payload: SD-Routing WAN OSPF feature from a specific transport feature profile
        :returns: CreateSdroutingTransportRoutingOspfFeaturePostResponse
        """
        params = {
            "transportId": transport_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/routing/ospf",
            return_type=CreateSdroutingTransportRoutingOspfFeaturePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        transport_id: str,
        ospf_id: str,
        payload: EditSdroutingTransportRoutingOspfFeaturePutRequest,
        **kw,
    ) -> EditSdroutingTransportRoutingOspfFeaturePutResponse:
        """
        Edit the SD-Routing WAN OSPF feature from a specific transport feature profile
        PUT /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/routing/ospf/{ospfId}

        :param transport_id: Transport Profile ID
        :param ospf_id: OSPF Feature ID
        :param payload: SD-Routing WAN OSPF feature from a specific transport feature profile
        :returns: EditSdroutingTransportRoutingOspfFeaturePutResponse
        """
        params = {
            "transportId": transport_id,
            "ospfId": ospf_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/routing/ospf/{ospfId}",
            return_type=EditSdroutingTransportRoutingOspfFeaturePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, ospf_id: str, **kw):
        """
        Delete the SD-Routing WAN OSPF feature from a specific transport feature profile
        DELETE /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/routing/ospf/{ospfId}

        :param transport_id: Transport Profile ID
        :param ospf_id: OSPF Feature ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "ospfId": ospf_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/routing/ospf/{ospfId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, ospf_id: str, **kw
    ) -> GetSingleSdRoutingTransportRoutingOspfPayload:
        """
        Get the SD-Routing WAN OSPF feature from a specific transport feature profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/routing/ospf/{ospfId}

        :param transport_id: Transport Profile ID
        :param ospf_id: OSPF Feature ID
        :returns: GetSingleSdRoutingTransportRoutingOspfPayload
        """
        ...

    @overload
    def get(self, transport_id: str, **kw) -> GetListSdRoutingTransportRoutingOspfPayload:
        """
        Get all SD-Routing WAN OSPF features from a specific transport feature profile
        GET /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/routing/ospf

        :param transport_id: Transport Profile ID
        :returns: GetListSdRoutingTransportRoutingOspfPayload
        """
        ...

    def get(
        self, transport_id: str, ospf_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdRoutingTransportRoutingOspfPayload, GetSingleSdRoutingTransportRoutingOspfPayload
    ]:
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/routing/ospf/{ospfId}
        if self._request_adapter.param_checker([(transport_id, str), (ospf_id, str)], []):
            params = {
                "transportId": transport_id,
                "ospfId": ospf_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/routing/ospf/{ospfId}",
                return_type=GetSingleSdRoutingTransportRoutingOspfPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sd-routing/transport/{transportId}/routing/ospf
        if self._request_adapter.param_checker([(transport_id, str)], [ospf_id]):
            params = {
                "transportId": transport_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sd-routing/transport/{transportId}/routing/ospf",
                return_type=GetListSdRoutingTransportRoutingOspfPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
