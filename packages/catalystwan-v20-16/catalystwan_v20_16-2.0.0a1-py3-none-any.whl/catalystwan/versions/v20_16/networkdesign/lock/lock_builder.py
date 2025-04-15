# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .edit.edit_builder import EditBuilder


class LockBuilder:
    """
    Builds and executes requests for operations under /networkdesign/lock
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def edit(self) -> EditBuilder:
        """
        The edit property
        """
        from .edit.edit_builder import EditBuilder

        return EditBuilder(self._request_adapter)
