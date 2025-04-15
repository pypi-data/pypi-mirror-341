# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .fetchv_manage_list.fetchv_manage_list_builder import FetchvManageListBuilder
    from .file.file_builder import FileBuilder
    from .filelist.filelist_builder import FilelistBuilder


class DownloadBuilder:
    """
    Builds and executes requests for operations under /statistics/download
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def fetchv_manage_list(self) -> FetchvManageListBuilder:
        """
        The fetchvManageList property
        """
        from .fetchv_manage_list.fetchv_manage_list_builder import FetchvManageListBuilder

        return FetchvManageListBuilder(self._request_adapter)

    @property
    def file(self) -> FileBuilder:
        """
        The file property
        """
        from .file.file_builder import FileBuilder

        return FileBuilder(self._request_adapter)

    @property
    def filelist(self) -> FilelistBuilder:
        """
        The filelist property
        """
        from .filelist.filelist_builder import FilelistBuilder

        return FilelistBuilder(self._request_adapter)
