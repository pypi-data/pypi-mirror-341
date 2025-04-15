# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import ResetVedgeCloud


class ResetBuilder:
    """
    Builds and executes requests for operations under /system/device/reset
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def put(self, uuid: str, **kw) -> ResetVedgeCloud:
        """
        Reset vEdge device
        PUT /dataservice/system/device/reset/{uuid}

        :param uuid: Device uuid
        :returns: ResetVedgeCloud
        """
        params = {
            "uuid": uuid,
        }
        return self._request_adapter.request(
            "PUT",
            "/dataservice/system/device/reset/{uuid}",
            return_type=ResetVedgeCloud,
            params=params,
            **kw,
        )
