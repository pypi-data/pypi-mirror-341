# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import ActivationStatusRes


class ListActivationStatusBuilder:
    """
    Builds and executes requests for operations under /wani/{listType}/{listId}/listActivationStatus
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, list_type: str, list_id: str, **kw) -> ActivationStatusRes:
        """
        Get if specified list is apart of a activated centralized policy, if it is the response also gives the centralized policy id, the users original defined centralized policy id, and if current list is apart of a active wani policy.
        GET /dataservice/wani/{listType}/{listId}/listActivationStatus

        :param list_type: List type
        :param list_id: List id
        :returns: ActivationStatusRes
        """
        params = {
            "listType": list_type,
            "listId": list_id,
        }
        return self._request_adapter.request(
            "GET",
            "/dataservice/wani/{listType}/{listId}/listActivationStatus",
            return_type=ActivationStatusRes,
            params=params,
            **kw,
        )
