# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any, List

from catalystwan.abc import RequestAdapterInterface


class DisconnectBuilder:
    """
    Builds and executes requests for operations under /mdp/disconnect
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, nms_id: str, **kw) -> List[Any]:
        """
        disconnect from mpd controller
        GET /dataservice/mdp/disconnect/{nmsId}

        :param nms_id: Nms id
        :returns: List[Any]
        """
        params = {
            "nmsId": nms_id,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/mdp/disconnect/{nmsId}", return_type=List[Any], params=params, **kw
        )
