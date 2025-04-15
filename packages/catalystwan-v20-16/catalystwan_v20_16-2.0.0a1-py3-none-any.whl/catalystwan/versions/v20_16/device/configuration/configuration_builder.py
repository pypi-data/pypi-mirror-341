# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .commit_list.commit_list_builder import CommitListBuilder


class ConfigurationBuilder:
    """
    Builds and executes requests for operations under /device/configuration
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def commit_list(self) -> CommitListBuilder:
        """
        The commit-list property
        """
        from .commit_list.commit_list_builder import CommitListBuilder

        return CommitListBuilder(self._request_adapter)
