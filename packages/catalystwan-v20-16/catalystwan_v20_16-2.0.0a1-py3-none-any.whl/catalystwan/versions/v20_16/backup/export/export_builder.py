# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import InlineResponse200, LocalBackupInfo


class ExportBuilder:
    """
    Builds and executes requests for operations under /backup/export
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def post(self, payload: LocalBackupInfo, **kw) -> InlineResponse200:
        """
        Trigger a backup of configuration database and statstics database and store it in vManage
        POST /dataservice/backup/export

        :param payload: backup request information
        :returns: InlineResponse200
        """
        return self._request_adapter.request(
            "POST",
            "/dataservice/backup/export",
            return_type=InlineResponse200,
            payload=payload,
            **kw,
        )
