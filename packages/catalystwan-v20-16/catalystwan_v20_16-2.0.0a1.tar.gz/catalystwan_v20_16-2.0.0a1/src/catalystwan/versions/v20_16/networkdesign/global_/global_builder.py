# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .parameters.parameters_builder import ParametersBuilder
    from .template.template_builder import TemplateBuilder


class GlobalBuilder:
    """
    Builds and executes requests for operations under /networkdesign/global
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def parameters(self) -> ParametersBuilder:
        """
        The parameters property
        """
        from .parameters.parameters_builder import ParametersBuilder

        return ParametersBuilder(self._request_adapter)

    @property
    def template(self) -> TemplateBuilder:
        """
        The template property
        """
        from .template.template_builder import TemplateBuilder

        return TemplateBuilder(self._request_adapter)
