# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .download.download_builder import DownloadBuilder


class PreviewBuilder:
    """
    Builds and executes requests for operations under /v1/reports/preview
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
