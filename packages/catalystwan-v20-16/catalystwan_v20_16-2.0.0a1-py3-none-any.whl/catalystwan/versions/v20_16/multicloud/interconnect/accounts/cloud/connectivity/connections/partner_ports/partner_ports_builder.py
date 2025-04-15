# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import InlineResponse2006


class PartnerPortsBuilder:
    """
    Builds and executes requests for operations under /multicloud/interconnect/{interconnect-type}/accounts/{interconnect-account-id}/cloud/{cloud-type}/connectivity/connections/partner-ports
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        interconnect_type: str,
        interconnect_account_id: str,
        cloud_type: str,
        connect_type: Optional[str] = None,
        vxc_permitted: Optional[str] = None,
        authorization_key: Optional[str] = None,
        refresh: Optional[str] = "false",
        **kw,
    ) -> InlineResponse2006:
        """
        API to retrieve supported partner regions for an Interconnect provider.
        GET /dataservice/multicloud/interconnect/{interconnect-type}/accounts/{interconnect-account-id}/cloud/{cloud-type}/connectivity/connections/partner-ports

        :param interconnect_type: Interconnect provider Type
        :param interconnect_account_id: Interconnect provider account id
        :param cloud_type: Cloud provider type
        :param connect_type: Interconnect connection connect type
        :param vxc_permitted: Interconnect connection cross connect enabled
        :param authorization_key: Cloud connectivity gateway service/pairing key
        :param refresh: Interconnect connection provider sync enabled
        :returns: InlineResponse2006
        """
        params = {
            "interconnect-type": interconnect_type,
            "interconnect-account-id": interconnect_account_id,
            "cloud-type": cloud_type,
            "connect-type": connect_type,
            "vxc-permitted": vxc_permitted,
            "authorization-key": authorization_key,
            "refresh": refresh,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/interconnect/{interconnect-type}/accounts/{interconnect-account-id}/cloud/{cloud-type}/connectivity/connections/partner-ports",
            return_type=InlineResponse2006,
            params=params,
            **kw,
        )
