# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .input.input_builder import InputBuilder


class ProcessBuilder:
    """
    Builds and executes requests for operations under /template/device/config/process
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def input(self) -> InputBuilder:
        """
        The input property
        """
        from .input.input_builder import InputBuilder

        return InputBuilder(self._request_adapter)
