# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface


class IseandpxgridBuilder:
    """
    Builds and executes requests for operations under /ise/credentials/iseandpxgrid
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def delete(self, **kw) -> bool:
        """
        Delete PxGrid and Ise information on vManage. Also Deletes PxGrid Client on ISE
        DELETE /dataservice/ise/credentials/iseandpxgrid

        :returns: bool
        """
        return self._request_adapter.request(
            "DELETE", "/dataservice/ise/credentials/iseandpxgrid", return_type=bool, **kw
        )
