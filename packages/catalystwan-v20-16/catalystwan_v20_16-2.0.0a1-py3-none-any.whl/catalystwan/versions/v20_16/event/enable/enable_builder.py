# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .fileprocess.fileprocess_builder import FileprocessBuilder


class EnableBuilder:
    """
    Builds and executes requests for operations under /event/enable
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def fileprocess(self) -> FileprocessBuilder:
        """
        The fileprocess property
        """
        from .fileprocess.fileprocess_builder import FileprocessBuilder

        return FileprocessBuilder(self._request_adapter)
