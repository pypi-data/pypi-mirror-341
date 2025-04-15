# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .details.details_builder import DetailsBuilder
    from .invalidate.invalidate_builder import InvalidateBuilder
    from .list.list_builder import ListBuilder
    from .stage.stage_builder import StageBuilder


class DeviceBuilder:
    """
    Builds and executes requests for operations under /certificate/device
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def details(self) -> DetailsBuilder:
        """
        The details property
        """
        from .details.details_builder import DetailsBuilder

        return DetailsBuilder(self._request_adapter)

    @property
    def invalidate(self) -> InvalidateBuilder:
        """
        The invalidate property
        """
        from .invalidate.invalidate_builder import InvalidateBuilder

        return InvalidateBuilder(self._request_adapter)

    @property
    def list(self) -> ListBuilder:
        """
        The list property
        """
        from .list.list_builder import ListBuilder

        return ListBuilder(self._request_adapter)

    @property
    def stage(self) -> StageBuilder:
        """
        The stage property
        """
        from .stage.stage_builder import StageBuilder

        return StageBuilder(self._request_adapter)
