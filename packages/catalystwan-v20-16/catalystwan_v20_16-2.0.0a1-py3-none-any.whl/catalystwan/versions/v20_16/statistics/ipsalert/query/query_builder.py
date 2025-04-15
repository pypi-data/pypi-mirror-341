# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .fields.fields_builder import FieldsBuilder


class QueryBuilder:
    """
    Builds and executes requests for operations under /statistics/ipsalert/query
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def fields(self) -> FieldsBuilder:
        """
        The fields property
        """
        from .fields.fields_builder import FieldsBuilder

        return FieldsBuilder(self._request_adapter)
