# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .accesslistassociations.accesslistassociations_builder import AccesslistassociationsBuilder
    from .accesslistcounters.accesslistcounters_builder import AccesslistcountersBuilder
    from .accesslistnames.accesslistnames_builder import AccesslistnamesBuilder
    from .accesslistpolicers.accesslistpolicers_builder import AccesslistpolicersBuilder


class Ipv6Builder:
    """
    Builds and executes requests for operations under /device/policy/ipv6
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def accesslistassociations(self) -> AccesslistassociationsBuilder:
        """
        The accesslistassociations property
        """
        from .accesslistassociations.accesslistassociations_builder import (
            AccesslistassociationsBuilder,
        )

        return AccesslistassociationsBuilder(self._request_adapter)

    @property
    def accesslistcounters(self) -> AccesslistcountersBuilder:
        """
        The accesslistcounters property
        """
        from .accesslistcounters.accesslistcounters_builder import AccesslistcountersBuilder

        return AccesslistcountersBuilder(self._request_adapter)

    @property
    def accesslistnames(self) -> AccesslistnamesBuilder:
        """
        The accesslistnames property
        """
        from .accesslistnames.accesslistnames_builder import AccesslistnamesBuilder

        return AccesslistnamesBuilder(self._request_adapter)

    @property
    def accesslistpolicers(self) -> AccesslistpolicersBuilder:
        """
        The accesslistpolicers property
        """
        from .accesslistpolicers.accesslistpolicers_builder import AccesslistpolicersBuilder

        return AccesslistpolicersBuilder(self._request_adapter)
