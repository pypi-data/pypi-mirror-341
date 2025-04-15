# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import InlineResponse200


class TypesBuilder:
    """
    Builds and executes requests for operations under /multicloud/interconnect/types
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> InlineResponse200:
        """
        API to retrieve list of supported Interconnect provider Types.
        GET /dataservice/multicloud/interconnect/types

        :returns: InlineResponse200
        """
        return self._request_adapter.request(
            "GET", "/dataservice/multicloud/interconnect/types", return_type=InlineResponse200, **kw
        )
