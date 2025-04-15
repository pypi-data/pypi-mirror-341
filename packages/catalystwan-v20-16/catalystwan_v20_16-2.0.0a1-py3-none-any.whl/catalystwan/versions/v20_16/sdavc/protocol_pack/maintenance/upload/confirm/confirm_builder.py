# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class ConfirmBuilder:
    """
    Builds and executes requests for operations under /sdavc/protocol-pack/maintenance/upload/confirm
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, uuid: str, **kw) -> Any:
        """
        Confirm uploaded protocol pack
        POST /dataservice/sdavc/protocol-pack/maintenance/upload/confirm/{uuid}

        :param uuid: Uuid
        :returns: Any
        """
        params = {
            "uuid": uuid,
        }
        return self._request_adapter.request(
            "POST",
            "/dataservice/sdavc/protocol-pack/maintenance/upload/confirm/{uuid}",
            params=params,
            **kw,
        )
