# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import InlineResponse20016


class IpTransitBuilder:
    """
    Builds and executes requests for operations under /multicloud/interconnect/ip-transit
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self, interconnect_service_type: str, interconnect_type: str, **kw
    ) -> InlineResponse20016:
        """
        API to retrieve Interconnect ip transit in MB supported by an  Interconnect provider.
        GET /dataservice/multicloud/interconnect/ip-transit

        :param interconnect_service_type: Interconnect Service Type
        :param interconnect_type: Interconnect provider type
        :returns: InlineResponse20016
        """
        params = {
            "interconnect-service-type": interconnect_service_type,
            "interconnect-type": interconnect_type,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/interconnect/ip-transit",
            return_type=InlineResponse20016,
            params=params,
            **kw,
        )
