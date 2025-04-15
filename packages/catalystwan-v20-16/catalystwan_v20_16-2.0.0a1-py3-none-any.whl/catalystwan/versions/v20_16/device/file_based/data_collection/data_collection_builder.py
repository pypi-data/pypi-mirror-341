# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .all_statuses.all_statuses_builder import AllStatusesBuilder
    from .download.download_builder import DownloadBuilder
    from .file_generation_status.file_generation_status_builder import FileGenerationStatusBuilder
    from .initiate_file_generation.initiate_file_generation_builder import (
        InitiateFileGenerationBuilder,
    )
    from .status.status_builder import StatusBuilder
    from .supported_commands.supported_commands_builder import SupportedCommandsBuilder


class DataCollectionBuilder:
    """
    Builds and executes requests for operations under /device/file-based/data-collection
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def all_statuses(self) -> AllStatusesBuilder:
        """
        The all-statuses property
        """
        from .all_statuses.all_statuses_builder import AllStatusesBuilder

        return AllStatusesBuilder(self._request_adapter)

    @property
    def download(self) -> DownloadBuilder:
        """
        The download property
        """
        from .download.download_builder import DownloadBuilder

        return DownloadBuilder(self._request_adapter)

    @property
    def file_generation_status(self) -> FileGenerationStatusBuilder:
        """
        The file-generation-status property
        """
        from .file_generation_status.file_generation_status_builder import (
            FileGenerationStatusBuilder,
        )

        return FileGenerationStatusBuilder(self._request_adapter)

    @property
    def initiate_file_generation(self) -> InitiateFileGenerationBuilder:
        """
        The initiate-file-generation property
        """
        from .initiate_file_generation.initiate_file_generation_builder import (
            InitiateFileGenerationBuilder,
        )

        return InitiateFileGenerationBuilder(self._request_adapter)

    @property
    def status(self) -> StatusBuilder:
        """
        The status property
        """
        from .status.status_builder import StatusBuilder

        return StatusBuilder(self._request_adapter)

    @property
    def supported_commands(self) -> SupportedCommandsBuilder:
        """
        The supported-commands property
        """
        from .supported_commands.supported_commands_builder import SupportedCommandsBuilder

        return SupportedCommandsBuilder(self._request_adapter)
