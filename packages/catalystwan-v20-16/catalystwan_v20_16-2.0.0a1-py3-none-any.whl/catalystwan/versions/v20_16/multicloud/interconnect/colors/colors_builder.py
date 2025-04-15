# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import InlineResponse2002, TunnelTypeParam


class ColorsBuilder:
    """
    Builds and executes requests for operations under /multicloud/interconnect/colors
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, tunnel_type: TunnelTypeParam, **kw) -> InlineResponse2002:
        """
        API to retrieve supported Colors for Interconnect tunnel type.
        GET /dataservice/multicloud/interconnect/colors/{tunnel-type}

        :param tunnel_type: Interconnect Loopback Tunnel Type
        :returns: InlineResponse2002
        """
        params = {
            "tunnel-type": tunnel_type,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/multicloud/interconnect/colors/{tunnel-type}",
            return_type=InlineResponse2002,
            params=params,
            **kw,
        )
