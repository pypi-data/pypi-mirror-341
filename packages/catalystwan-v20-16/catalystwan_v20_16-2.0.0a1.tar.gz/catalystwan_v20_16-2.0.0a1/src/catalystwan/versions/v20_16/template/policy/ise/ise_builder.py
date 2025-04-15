# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .identity.identity_builder import IdentityBuilder


class IseBuilder:
    """
    Builds and executes requests for operations under /template/policy/ise
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def identity(self) -> IdentityBuilder:
        """
        The identity property
        """
        from .identity.identity_builder import IdentityBuilder

        return IdentityBuilder(self._request_adapter)
