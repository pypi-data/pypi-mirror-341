# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .approute.approute_builder import ApprouteBuilder


class DefinitionBuilder:
    """
    Builds and executes requests for operations under /dca/template/policy/definition
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def approute(self) -> ApprouteBuilder:
        """
        The approute property
        """
        from .approute.approute_builder import ApprouteBuilder

        return ApprouteBuilder(self._request_adapter)
