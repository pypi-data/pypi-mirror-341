# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateEsimCellularControllerProfileFeatureForTransportPostRequest,
    CreateEsimCellularControllerProfileFeatureForTransportPostResponse,
    EditEsimCellularControllerProfileFeatureForTransportPutRequest,
    EditEsimCellularControllerProfileFeatureForTransportPutResponse,
    GetListSdwanTransportEsimcellularControllerPayload,
    GetSingleSdwanTransportEsimcellularControllerPayload,
)


class EsimcellularControllerBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/transport/{transportId}/esimcellular-controller
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        transport_id: str,
        payload: CreateEsimCellularControllerProfileFeatureForTransportPostRequest,
        **kw,
    ) -> CreateEsimCellularControllerProfileFeatureForTransportPostResponse:
        """
        Create a eSim Cellular Controller Feature for Transport feature profile
        POST /dataservice/v1/feature-profile/sdwan/transport/{transportId}/esimcellular-controller

        :param transport_id: Feature Profile ID
        :param payload: eSim Cellular Controller Feature
        :returns: CreateEsimCellularControllerProfileFeatureForTransportPostResponse
        """
        params = {
            "transportId": transport_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/esimcellular-controller",
            return_type=CreateEsimCellularControllerProfileFeatureForTransportPostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        transport_id: str,
        esim_cellular_controller_id: str,
        payload: EditEsimCellularControllerProfileFeatureForTransportPutRequest,
        **kw,
    ) -> EditEsimCellularControllerProfileFeatureForTransportPutResponse:
        """
        Update a eSim Cellular Controller Feature for Transport feature profile
        PUT /dataservice/v1/feature-profile/sdwan/transport/{transportId}/esimcellular-controller/{esimCellularControllerId}

        :param transport_id: Feature Profile ID
        :param esim_cellular_controller_id: Feature ID
        :param payload: EsimCellular Controller Feature
        :returns: EditEsimCellularControllerProfileFeatureForTransportPutResponse
        """
        params = {
            "transportId": transport_id,
            "esimCellularControllerId": esim_cellular_controller_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/esimcellular-controller/{esimCellularControllerId}",
            return_type=EditEsimCellularControllerProfileFeatureForTransportPutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, transport_id: str, esim_cellular_controller_id: str, **kw):
        """
        Delete a eSim Cellular Controller Feature for Transport feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/transport/{transportId}/esimcellular-controller/{esimCellularControllerId}

        :param transport_id: Feature Profile ID
        :param esim_cellular_controller_id: Feature ID
        :returns: None
        """
        params = {
            "transportId": transport_id,
            "esimCellularControllerId": esim_cellular_controller_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/esimcellular-controller/{esimCellularControllerId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, transport_id: str, esim_cellular_controller_id: str, **kw
    ) -> GetSingleSdwanTransportEsimcellularControllerPayload:
        """
        Get eSim Cellular Controller Feature by Feature Id for Transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/esimcellular-controller/{esimCellularControllerId}

        :param transport_id: Feature Profile ID
        :param esim_cellular_controller_id: Feature ID
        :returns: GetSingleSdwanTransportEsimcellularControllerPayload
        """
        ...

    @overload
    def get(self, transport_id: str, **kw) -> GetListSdwanTransportEsimcellularControllerPayload:
        """
        Get eSim Cellular Controller Features for Transport feature profile
        GET /dataservice/v1/feature-profile/sdwan/transport/{transportId}/esimcellular-controller

        :param transport_id: Feature Profile ID
        :returns: GetListSdwanTransportEsimcellularControllerPayload
        """
        ...

    def get(
        self, transport_id: str, esim_cellular_controller_id: Optional[str] = None, **kw
    ) -> Union[
        GetListSdwanTransportEsimcellularControllerPayload,
        GetSingleSdwanTransportEsimcellularControllerPayload,
    ]:
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/esimcellular-controller/{esimCellularControllerId}
        if self._request_adapter.param_checker(
            [(transport_id, str), (esim_cellular_controller_id, str)], []
        ):
            params = {
                "transportId": transport_id,
                "esimCellularControllerId": esim_cellular_controller_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/esimcellular-controller/{esimCellularControllerId}",
                return_type=GetSingleSdwanTransportEsimcellularControllerPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/transport/{transportId}/esimcellular-controller
        if self._request_adapter.param_checker(
            [(transport_id, str)], [esim_cellular_controller_id]
        ):
            params = {
                "transportId": transport_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/transport/{transportId}/esimcellular-controller",
                return_type=GetListSdwanTransportEsimcellularControllerPayload,
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
