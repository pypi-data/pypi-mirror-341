# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class AttacheddiaBuilder:
    """
    Builds and executes requests for operations under /template/cloudx/attacheddia
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[Any]:
        """
        Get attached Dia site list
        GET /dataservice/template/cloudx/attacheddia

        :returns: List[Any]
        """
        return self._request_adapter.request(
            "GET", "/dataservice/template/cloudx/attacheddia", return_type=List[Any], **kw
        )
