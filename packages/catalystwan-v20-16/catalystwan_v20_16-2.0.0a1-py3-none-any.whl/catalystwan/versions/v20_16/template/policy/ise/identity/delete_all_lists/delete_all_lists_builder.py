# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import Optional

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import DeleteAllListsBody


class DeleteAllListsBuilder:
    """
    Builds and executes requests for operations under /template/policy/ise/identity/deleteAllLists
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def delete(self, payload: Optional[DeleteAllListsBody] = None, **kw) -> bool:
        """
        Delete all lists of the specified list type
        DELETE /dataservice/template/policy/ise/identity/deleteAllLists

        :param payload: type of list
        :returns: bool
        """
        return self._request_adapter.request(
            "DELETE",
            "/dataservice/template/policy/ise/identity/deleteAllLists",
            return_type=bool,
            payload=payload,
            **kw,
        )
