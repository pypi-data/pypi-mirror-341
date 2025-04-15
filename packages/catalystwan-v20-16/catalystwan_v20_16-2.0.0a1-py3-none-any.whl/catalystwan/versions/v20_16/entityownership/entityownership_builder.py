# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .list.list_builder import ListBuilder
    from .tree.tree_builder import TreeBuilder


class EntityownershipBuilder:
    """
    Builds and executes requests for operations under /entityownership
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def list(self) -> ListBuilder:
        """
        The list property
        """
        from .list.list_builder import ListBuilder

        return ListBuilder(self._request_adapter)

    @property
    def tree(self) -> TreeBuilder:
        """
        The tree property
        """
        from .tree.tree_builder import TreeBuilder

        return TreeBuilder(self._request_adapter)
