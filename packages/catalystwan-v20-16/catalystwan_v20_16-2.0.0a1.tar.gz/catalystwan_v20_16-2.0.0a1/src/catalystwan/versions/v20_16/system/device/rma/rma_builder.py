# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .candidates.candidates_builder import CandidatesBuilder


class RmaBuilder:
    """
    Builds and executes requests for operations under /system/device/rma
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def candidates(self) -> CandidatesBuilder:
        """
        The candidates property
        """
        from .candidates.candidates_builder import CandidatesBuilder

        return CandidatesBuilder(self._request_adapter)
