# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .activate.activate_builder import ActivateBuilder
    from .deactivate.deactivate_builder import DeactivateBuilder
    from .does_valid_image_exist.does_valid_image_exist_builder import DoesValidImageExistBuilder
    from .inspect.inspect_builder import InspectBuilder
    from .settings.settings_builder import SettingsBuilder


class ContainerManagerBuilder:
    """
    Builds and executes requests for operations under /container-manager
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def activate(self) -> ActivateBuilder:
        """
        The activate property
        """
        from .activate.activate_builder import ActivateBuilder

        return ActivateBuilder(self._request_adapter)

    @property
    def deactivate(self) -> DeactivateBuilder:
        """
        The deactivate property
        """
        from .deactivate.deactivate_builder import DeactivateBuilder

        return DeactivateBuilder(self._request_adapter)

    @property
    def does_valid_image_exist(self) -> DoesValidImageExistBuilder:
        """
        The doesValidImageExist property
        """
        from .does_valid_image_exist.does_valid_image_exist_builder import (
            DoesValidImageExistBuilder,
        )

        return DoesValidImageExistBuilder(self._request_adapter)

    @property
    def inspect(self) -> InspectBuilder:
        """
        The inspect property
        """
        from .inspect.inspect_builder import InspectBuilder

        return InspectBuilder(self._request_adapter)

    @property
    def settings(self) -> SettingsBuilder:
        """
        The settings property
        """
        from .settings.settings_builder import SettingsBuilder

        return SettingsBuilder(self._request_adapter)
