# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class ReportingBuilder:
    """
    Builds and executes requests for operations under /umbrella/getkeys/reporting
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw):
        """
        Get reporting keys from Umbrella
        GET /dataservice/umbrella/getkeys/reporting

        :returns: None
        """
        return self._request_adapter.request("GET", "/dataservice/umbrella/getkeys/reporting", **kw)
