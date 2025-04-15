# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import GetStatQueryFields


class FieldsBuilder:
    """
    Builds and executes requests for operations under /auditlog/query/fields
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[GetStatQueryFields]:
        """
        Get query fields
        GET /dataservice/auditlog/query/fields

        :returns: List[GetStatQueryFields]
        """
        return self._request_adapter.request(
            "GET", "/dataservice/auditlog/query/fields", return_type=List[GetStatQueryFields], **kw
        )
