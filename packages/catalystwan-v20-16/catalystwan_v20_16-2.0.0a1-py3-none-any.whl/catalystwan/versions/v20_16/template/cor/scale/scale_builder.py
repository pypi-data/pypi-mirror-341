# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .down.down_builder import DownBuilder
    from .up.up_builder import UpBuilder


class ScaleBuilder:
    """
    Builds and executes requests for operations under /template/cor/scale
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def down(self) -> DownBuilder:
        """
        The down property
        """
        from .down.down_builder import DownBuilder

        return DownBuilder(self._request_adapter)

    @property
    def up(self) -> UpBuilder:
        """
        The up property
        """
        from .up.up_builder import UpBuilder

        return UpBuilder(self._request_adapter)
