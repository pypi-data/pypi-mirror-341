# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class UnlockBuilder:
    """
    Builds and executes requests for operations under /system/device/{uuid}/unlock
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, uuid: str, payload: Any, **kw):
        """
        Unlock device
        POST /dataservice/system/device/{uuid}/unlock

        :param uuid: Device uuid
        :param payload: Device config
        :returns: None
        """
        params = {
            "uuid": uuid,
        }
        return self._request_adapter.request(
            "POST", "/dataservice/system/device/{uuid}/unlock", params=params, payload=payload, **kw
        )
