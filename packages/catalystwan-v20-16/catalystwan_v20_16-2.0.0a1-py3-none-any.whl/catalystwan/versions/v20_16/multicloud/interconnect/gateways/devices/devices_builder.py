# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import InlineResponse2003, InterconnectTypeParam


class DevicesBuilder:
    """
    Builds and executes requests for operations under /multicloud/interconnect/{interconnect-type}/gateways/devices
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, interconnect_type: InterconnectTypeParam, **kw) -> List[InlineResponse2003]:
        """
        API to retrieve available Interconnect Gateway devices.
        GET /dataservice/multicloud/interconnect/{interconnect-type}/gateways/devices

        :param interconnect_type: Interconnect Provider Type
        :returns: List[InlineResponse2003]
        """
        params = {
            "interconnect-type": interconnect_type,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/interconnect/{interconnect-type}/gateways/devices",
            return_type=List[InlineResponse2003],
            params=params,
            **kw,
        )
