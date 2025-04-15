# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .backupinfo.backupinfo_builder import BackupinfoBuilder
    from .download.download_builder import DownloadBuilder
    from .export.export_builder import ExportBuilder
    from .list.list_builder import ListBuilder


class BackupBuilder:
    """
    Builds and executes requests for operations under /backup
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def backupinfo(self) -> BackupinfoBuilder:
        """
        The backupinfo property
        """
        from .backupinfo.backupinfo_builder import BackupinfoBuilder

        return BackupinfoBuilder(self._request_adapter)

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
    def list(self) -> ListBuilder:
        """
        The list property
        """
        from .list.list_builder import ListBuilder

        return ListBuilder(self._request_adapter)
