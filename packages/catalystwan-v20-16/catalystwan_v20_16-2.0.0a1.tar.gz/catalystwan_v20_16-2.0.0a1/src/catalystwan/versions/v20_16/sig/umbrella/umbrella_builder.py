# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .child_org.child_org_builder import ChildOrgBuilder


class UmbrellaBuilder:
    """
    Builds and executes requests for operations under /sig/umbrella
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def child_org(self) -> ChildOrgBuilder:
        """
        The childOrg property
        """
        from .child_org.child_org_builder import ChildOrgBuilder

        return ChildOrgBuilder(self._request_adapter)
