# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .database.database_builder import DatabaseBuilder
    from .local.local_builder import LocalBuilder
    from .remotemep.remotemep_builder import RemotemepBuilder


class MpBuilder:
    """
    Builds and executes requests for operations under /device/cfm/mp
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def database(self) -> DatabaseBuilder:
        """
        The database property
        """
        from .database.database_builder import DatabaseBuilder

        return DatabaseBuilder(self._request_adapter)

    @property
    def local(self) -> LocalBuilder:
        """
        The local property
        """
        from .local.local_builder import LocalBuilder

        return LocalBuilder(self._request_adapter)

    @property
    def remotemep(self) -> RemotemepBuilder:
        """
        The remotemep property
        """
        from .remotemep.remotemep_builder import RemotemepBuilder

        return RemotemepBuilder(self._request_adapter)
