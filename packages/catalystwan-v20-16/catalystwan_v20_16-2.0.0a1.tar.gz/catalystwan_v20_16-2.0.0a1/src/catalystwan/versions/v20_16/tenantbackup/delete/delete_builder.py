# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Any

from catalystwan.abc import RequestAdapterInterface


class DeleteBuilder:
    """
    Builds and executes requests for operations under /tenantbackup/delete
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def delete(self, file_name: str, **kw) -> Any:
        """
        Delete all or a specific backup file stored in vManage


        Note: In a multitenant vManage system, this API is only available in the Provider view.
        DELETE /dataservice/tenantbackup/delete

        :param file_name: File name
        :returns: Any
        """
        params = {
            "fileName": file_name,
        }
        return self._request_adapter.request(
            "DELETE", "/dataservice/tenantbackup/delete", params=params, **kw
        )
