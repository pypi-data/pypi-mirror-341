# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .enterprise.enterprise_builder import EnterpriseBuilder


class RevokeBuilder:
    """
    Builds and executes requests for operations under /certificate/revoke
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def enterprise(self) -> EnterpriseBuilder:
        """
        The enterprise property
        """
        from .enterprise.enterprise_builder import EnterpriseBuilder

        return EnterpriseBuilder(self._request_adapter)
