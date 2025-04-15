# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .download.download_builder import DownloadBuilder
    from .export.export_builder import ExportBuilder
    from .import_.import_builder import ImportBuilder
    from .migration_token.migration_token_builder import MigrationTokenBuilder
    from .network_migration.network_migration_builder import NetworkMigrationBuilder


class TenantmigrationBuilder:
    """
    Builds and executes requests for operations under /tenantmigration
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def download(self) -> DownloadBuilder:
        """
        The download property
        """
        from .download.download_builder import DownloadBuilder

        return DownloadBuilder(self._request_adapter)

    @property
    def export(self) -> ExportBuilder:
        """
        The export property
        """
        from .export.export_builder import ExportBuilder

        return ExportBuilder(self._request_adapter)

    @property
    def import_(self) -> ImportBuilder:
        """
        The import property
        """
        from .import_.import_builder import ImportBuilder

        return ImportBuilder(self._request_adapter)

    @property
    def migration_token(self) -> MigrationTokenBuilder:
        """
        The migrationToken property
        """
        from .migration_token.migration_token_builder import MigrationTokenBuilder

        return MigrationTokenBuilder(self._request_adapter)

    @property
    def network_migration(self) -> NetworkMigrationBuilder:
        """
        The networkMigration property
        """
        from .network_migration.network_migration_builder import NetworkMigrationBuilder

        return NetworkMigrationBuilder(self._request_adapter)
