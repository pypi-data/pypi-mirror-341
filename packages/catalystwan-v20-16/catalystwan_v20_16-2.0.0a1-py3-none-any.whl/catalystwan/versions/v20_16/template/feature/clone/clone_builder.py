# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class CloneBuilder:
    """
    Builds and executes requests for operations under /template/feature/clone
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, id: str, name: str, desc: str, **kw) -> Any:
        """
        Clone a feature template


        Note: In a multitenant vManage system, this API is only available in the Provider view.
        POST /dataservice/template/feature/clone

        :param id: Template Id to clone from
        :param name: Name for the cloned template
        :param desc: Description for the cloned template
        :returns: Any
        """
        params = {
            "id": id,
            "name": name,
            "desc": desc,
        }
        return self._request_adapter.request(
            "POST", "/dataservice/template/feature/clone", params=params, **kw
        )
