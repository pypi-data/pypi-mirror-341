# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import (
    CreateLanVpnAndRoutingEigrpParcelAssociationForServicePostRequest,
    CreateLanVpnAndRoutingEigrpParcelAssociationForServicePostResponse,
    EditLanVpnAndRoutingEigrpParcelAssociationForServicePutRequest,
    EditLanVpnAndRoutingEigrpParcelAssociationForServicePutResponse,
    GetLanVpnAssociatedRoutingEigrpParcelsForServiceGetResponse,
    GetSingleSdwanServiceLanVpnRoutingEigrpPayload,
)


class EigrpBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/eigrp
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self,
        service_id: str,
        vpn_id: str,
        payload: CreateLanVpnAndRoutingEigrpParcelAssociationForServicePostRequest,
        **kw,
    ) -> CreateLanVpnAndRoutingEigrpParcelAssociationForServicePostResponse:
        """
        Associate a lanvpn feature with a routingeigrp Feature for service feature profile
        POST /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/eigrp

        :param service_id: Feature Profile ID
        :param vpn_id: Lan Vpn Profile Feature ID
        :param payload: Routing Eigrp Profile Feature Id
        :returns: CreateLanVpnAndRoutingEigrpParcelAssociationForServicePostResponse
        """
        params = {
            "serviceId": service_id,
            "vpnId": vpn_id,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/eigrp",
            return_type=CreateLanVpnAndRoutingEigrpParcelAssociationForServicePostResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def put(
        self,
        service_id: str,
        vpn_id: str,
        eigrp_id: str,
        payload: EditLanVpnAndRoutingEigrpParcelAssociationForServicePutRequest,
        **kw,
    ) -> EditLanVpnAndRoutingEigrpParcelAssociationForServicePutResponse:
        """
        Update a LanVpn feature and a RoutingEigrp Feature association for service feature profile
        PUT /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/eigrp/{eigrpId}

        :param service_id: Feature Profile ID
        :param vpn_id: Profile Feature ID
        :param eigrp_id: Routing Eigrp ID
        :param payload: Routing Eigrp Profile Feature
        :returns: EditLanVpnAndRoutingEigrpParcelAssociationForServicePutResponse
        """
        params = {
            "serviceId": service_id,
            "vpnId": vpn_id,
            "eigrpId": eigrp_id,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/eigrp/{eigrpId}",
            return_type=EditLanVpnAndRoutingEigrpParcelAssociationForServicePutResponse,
            params=params,
            payload=payload,
            **kw,
        )

    def delete(self, service_id: str, vpn_id: str, eigrp_id: str, **kw):
        """
        Delete a LanVpn feature and a RoutingEigrp Feature association for service feature profile
        DELETE /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/eigrp/{eigrpId}

        :param service_id: Feature Profile ID
        :param vpn_id: Profile Feature ID
        :param eigrp_id: Routing Eigrp Feature ID
        :returns: None
        """
        params = {
            "serviceId": service_id,
            "vpnId": vpn_id,
            "eigrpId": eigrp_id,
        }
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/eigrp/{eigrpId}",
            params=params,
            **kw,
        )

    @overload
    def get(
        self, service_id: str, vpn_id: str, eigrp_id: str, **kw
    ) -> GetSingleSdwanServiceLanVpnRoutingEigrpPayload:
        """
        Get LanVpn feature associated RoutingEigrp Feature by eigrpId for service feature profile
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/eigrp/{eigrpId}

        :param service_id: Feature Profile ID
        :param vpn_id: Profile Feature ID
        :param eigrp_id: Routing Eigrp Feature ID
        :returns: GetSingleSdwanServiceLanVpnRoutingEigrpPayload
        """
        ...

    @overload
    def get(
        self, service_id: str, vpn_id: str, **kw
    ) -> List[GetLanVpnAssociatedRoutingEigrpParcelsForServiceGetResponse]:
        """
        Get LanVpn associated Routing Eigrp Features for service feature profile
        GET /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/eigrp

        :param service_id: Feature Profile ID
        :param vpn_id: Feature Feature ID
        :returns: List[GetLanVpnAssociatedRoutingEigrpParcelsForServiceGetResponse]
        """
        ...

    def get(
        self, service_id: str, vpn_id: str, eigrp_id: Optional[str] = None, **kw
    ) -> Union[
        List[GetLanVpnAssociatedRoutingEigrpParcelsForServiceGetResponse],
        GetSingleSdwanServiceLanVpnRoutingEigrpPayload,
    ]:
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/eigrp/{eigrpId}
        if self._request_adapter.param_checker(
            [(service_id, str), (vpn_id, str), (eigrp_id, str)], []
        ):
            params = {
                "serviceId": service_id,
                "vpnId": vpn_id,
                "eigrpId": eigrp_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/eigrp/{eigrpId}",
                return_type=GetSingleSdwanServiceLanVpnRoutingEigrpPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/eigrp
        if self._request_adapter.param_checker([(service_id, str), (vpn_id, str)], [eigrp_id]):
            params = {
                "serviceId": service_id,
                "vpnId": vpn_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/sdwan/service/{serviceId}/lan/vpn/{vpnId}/routing/eigrp",
                return_type=List[GetLanVpnAssociatedRoutingEigrpParcelsForServiceGetResponse],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")
