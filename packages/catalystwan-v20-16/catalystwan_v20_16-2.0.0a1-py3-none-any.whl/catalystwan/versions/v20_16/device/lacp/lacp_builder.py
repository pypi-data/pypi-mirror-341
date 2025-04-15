# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .info.info_builder import InfoBuilder
    from .members.members_builder import MembersBuilder


class LacpBuilder:
    """
    Builds and executes requests for operations under /device/lacp
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def info(self) -> InfoBuilder:
        """
        The info property
        """
        from .info.info_builder import InfoBuilder

        return InfoBuilder(self._request_adapter)

    @property
    def members(self) -> MembersBuilder:
        """
        The members property
        """
        from .members.members_builder import MembersBuilder

        return MembersBuilder(self._request_adapter)
