# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class DevicesBuilder:
    """
    Builds and executes requests for operations under /mdp/devices
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, nms_id: str, **kw) -> List[Any]:
        """
        Retrieve MDP supported devices
        GET /dataservice/mdp/devices/{nmsId}

        :param nms_id: Nms id
        :returns: List[Any]
        """
        params = {
            "nmsId": nms_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/mdp/devices/{nmsId}", return_type=List[Any], params=params, **kw
        )
