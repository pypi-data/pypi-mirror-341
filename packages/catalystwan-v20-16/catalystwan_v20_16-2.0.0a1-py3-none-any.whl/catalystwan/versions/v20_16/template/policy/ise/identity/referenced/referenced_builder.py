# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import List

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import ReferencedList


class ReferencedBuilder:
    """
    Builds and executes requests for operations under /template/policy/ise/identity/referenced
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, list_type: str, **kw) -> List[ReferencedList]:
        """
        Get all referenced Lists
        GET /dataservice/template/policy/ise/identity/referenced/{listType}

        :param list_type: List type
        :returns: List[ReferencedList]
        """
        params = {
            "listType": list_type,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/template/policy/ise/identity/referenced/{listType}",
            return_type=List[ReferencedList],
            params=params,
            **kw,
        )
