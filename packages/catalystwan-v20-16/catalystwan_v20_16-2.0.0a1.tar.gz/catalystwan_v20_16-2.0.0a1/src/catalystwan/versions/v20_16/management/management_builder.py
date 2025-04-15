# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .category.category_builder import CategoryBuilder
    from .v_manage_resource_utilization.v_manage_resource_utilization_builder import (
        VManageResourceUtilizationBuilder,
    )


class ManagementBuilder:
    """
    Builds and executes requests for operations under /management
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def category(self) -> CategoryBuilder:
        """
        The category property
        """
        from .category.category_builder import CategoryBuilder

        return CategoryBuilder(self._request_adapter)

    @property
    def v_manage_resource_utilization(self) -> VManageResourceUtilizationBuilder:
        """
        The vManageResourceUtilization property
        """
        from .v_manage_resource_utilization.v_manage_resource_utilization_builder import (
            VManageResourceUtilizationBuilder,
        )

        return VManageResourceUtilizationBuilder(self._request_adapter)
