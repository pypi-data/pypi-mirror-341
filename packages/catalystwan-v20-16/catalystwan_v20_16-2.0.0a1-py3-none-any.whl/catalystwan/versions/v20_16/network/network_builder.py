# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .connectionssummary.connectionssummary_builder import ConnectionssummaryBuilder
    from .issues.issues_builder import IssuesBuilder
    from .status.status_builder import StatusBuilder


class NetworkBuilder:
    """
    Builds and executes requests for operations under /network
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def connectionssummary(self) -> ConnectionssummaryBuilder:
        """
        The connectionssummary property
        """
        from .connectionssummary.connectionssummary_builder import ConnectionssummaryBuilder

        return ConnectionssummaryBuilder(self._request_adapter)

    @property
    def issues(self) -> IssuesBuilder:
        """
        The issues property
        """
        from .issues.issues_builder import IssuesBuilder

        return IssuesBuilder(self._request_adapter)

    @property
    def status(self) -> StatusBuilder:
        """
        The status property
        """
        from .status.status_builder import StatusBuilder

        return StatusBuilder(self._request_adapter)
