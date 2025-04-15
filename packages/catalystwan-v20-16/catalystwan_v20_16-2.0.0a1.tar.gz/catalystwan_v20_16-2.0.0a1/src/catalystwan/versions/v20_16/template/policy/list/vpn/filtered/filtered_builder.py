# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List, Optional

from catalystwan.abc import RequestAdapterInterface


class FilteredBuilder:
    """
    Builds and executes requests for operations under /template/policy/list/vpn/filtered
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, info_tag: Optional[str] = None, **kw) -> List[Any]:
        """
        Get policy lists with specific info tag
        GET /dataservice/template/policy/list/vpn/filtered

        :param info_tag: InfoTag
        :returns: List[Any]
        """
        params = {
            "infoTag": info_tag,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/template/policy/list/vpn/filtered",
            return_type=List[Any],
            params=params,
            **kw,
        )
