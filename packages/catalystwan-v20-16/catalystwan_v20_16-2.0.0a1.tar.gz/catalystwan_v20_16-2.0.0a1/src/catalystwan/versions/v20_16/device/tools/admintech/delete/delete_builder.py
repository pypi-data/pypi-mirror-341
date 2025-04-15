# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import AdminTechReq


class DeleteBuilder:
    """
    Builds and executes requests for operations under /device/tools/admintech/delete
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def delete(self, payload: Optional[AdminTechReq] = None, **kw):
        """
        delete admin tech logs
        DELETE /dataservice/device/tools/admintech/delete

        :param payload: Admin tech delete request
        :returns: None
        """
        return self._request_adapter.request(
            "DELETE", "/dataservice/device/tools/admintech/delete", payload=payload, **kw
        )
