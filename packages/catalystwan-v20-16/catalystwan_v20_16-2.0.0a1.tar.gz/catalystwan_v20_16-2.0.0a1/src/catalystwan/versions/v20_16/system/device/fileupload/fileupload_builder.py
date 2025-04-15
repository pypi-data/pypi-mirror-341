# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import FormPostResp


class FileuploadBuilder:
    """
    Builds and executes requests for operations under /system/device/fileupload
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: Any, **kw) -> FormPostResp:
        """
        Upload file to vEdge
        POST /dataservice/system/device/fileupload

        :param payload: Request body for Upload file to vEdge
        :returns: FormPostResp
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/system/device/fileupload",
            return_type=FormPostResp,
            payload=payload,
            **kw,
        )
