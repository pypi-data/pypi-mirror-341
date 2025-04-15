# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import InlineResponse20012, InterconnectDeviceLink, InterconnectTypeParam


class MetroSpeedBuilder:
    """
    Builds and executes requests for operations under /multicloud/interconnect/{interconnect-type}/connectivity/device-links/metro-speed
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(
        self, interconnect_type: InterconnectTypeParam, payload: InterconnectDeviceLink, **kw
    ) -> InlineResponse20012:
        """
        API to get metro speed for Device-Link by Device-Link Configuration.
        POST /dataservice/multicloud/interconnect/{interconnect-type}/connectivity/device-links/metro-speed

        :param interconnect_type: Interconnect Provider Type
        :param payload: Request Payload for Multicloud Interconnect Device Links
        :returns: InlineResponse20012
        """
        params = {
            "interconnect-type": interconnect_type,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/multicloud/interconnect/{interconnect-type}/connectivity/device-links/metro-speed",
            return_type=InlineResponse20012,
            params=params,
            payload=payload,
            **kw,
        )
