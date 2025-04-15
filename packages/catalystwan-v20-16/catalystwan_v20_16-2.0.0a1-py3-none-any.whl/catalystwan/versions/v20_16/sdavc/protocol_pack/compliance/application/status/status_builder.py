# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class StatusBuilder:
    """
    Builds and executes requests for operations under /sdavc/protocol-pack/compliance/application/status
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, uuid: str, **kw) -> Any:
        """
        Get application name compliance task status
        GET /dataservice/sdavc/protocol-pack/compliance/application/status/{uuid}

        :param uuid: Uuid
        :returns: Any
        """
        params = {
            "uuid": uuid,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/sdavc/protocol-pack/compliance/application/status/{uuid}",
            params=params,
            **kw,
        )
