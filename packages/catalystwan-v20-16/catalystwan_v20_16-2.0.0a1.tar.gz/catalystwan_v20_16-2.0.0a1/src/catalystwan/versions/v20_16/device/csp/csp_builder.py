# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .containers.containers_builder import ContainersBuilder
    from .pnic.pnic_builder import PnicBuilder
    from .rbac.rbac_builder import RbacBuilder
    from .resources.resources_builder import ResourcesBuilder
    from .system.system_builder import SystemBuilder


class CspBuilder:
    """
    Builds and executes requests for operations under /device/csp
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def containers(self) -> ContainersBuilder:
        """
        The containers property
        """
        from .containers.containers_builder import ContainersBuilder

        return ContainersBuilder(self._request_adapter)

    @property
    def pnic(self) -> PnicBuilder:
        """
        The pnic property
        """
        from .pnic.pnic_builder import PnicBuilder

        return PnicBuilder(self._request_adapter)

    @property
    def rbac(self) -> RbacBuilder:
        """
        The rbac property
        """
        from .rbac.rbac_builder import RbacBuilder

        return RbacBuilder(self._request_adapter)

    @property
    def resources(self) -> ResourcesBuilder:
        """
        The resources property
        """
        from .resources.resources_builder import ResourcesBuilder

        return ResourcesBuilder(self._request_adapter)

    @property
    def system(self) -> SystemBuilder:
        """
        The system property
        """
        from .system.system_builder import SystemBuilder

        return SystemBuilder(self._request_adapter)
