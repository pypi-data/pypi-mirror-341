# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List, Optional

from catalystwan.abc import RequestAdapterInterface


class RecordBuilder:
    """
    Builds and executes requests for operations under /certificate/record
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self, request_id: Optional[str] = None, data_object: Optional[str] = None, **kw
    ) -> List[str]:
        """
        get device certificate data
        GET /dataservice/certificate/record

        :param request_id: Request ID parameter
        :param data_object: Device property as DataObject parameter
        :returns: List[str]
        """
        params = {
            "requestID": request_id,
            "dataObject": data_object,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/certificate/record", return_type=List[str], params=params, **kw
        )
