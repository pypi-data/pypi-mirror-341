# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class SequencesBuilder:
    """
    Builds and executes requests for operations under /partner/aci/policy/sequences
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[Any]:
        """
        Get data prefix sequence
        GET /dataservice/partner/aci/policy/sequences

        :returns: List[Any]
        """
        return self._request_adapter.request(
            "GET", "/dataservice/partner/aci/policy/sequences", return_type=List[Any], **kw
        )
