# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import GetStatDataFields


class FieldsBuilder:
    """
    Builds and executes requests for operations under /auditlog/fields
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[GetStatDataFields]:
        """
        Get fields and type
        GET /dataservice/auditlog/fields

        :returns: List[GetStatDataFields]
        """
        return self._request_adapter.request(
            "GET", "/dataservice/auditlog/fields", return_type=List[GetStatDataFields], **kw
        )
