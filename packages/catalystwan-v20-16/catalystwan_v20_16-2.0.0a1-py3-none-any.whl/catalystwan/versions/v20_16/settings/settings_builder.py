# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .banner.banner_builder import BannerBuilder
    from .client_session_timeout.client_session_timeout_builder import ClientSessionTimeoutBuilder
    from .configuration.configuration_builder import ConfigurationBuilder
    from .password_policy.password_policy_builder import PasswordPolicyBuilder


class SettingsBuilder:
    """
    Builds and executes requests for operations under /settings
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def banner(self) -> BannerBuilder:
        """
        The banner property
        """
        from .banner.banner_builder import BannerBuilder

        return BannerBuilder(self._request_adapter)

    @property
    def client_session_timeout(self) -> ClientSessionTimeoutBuilder:
        """
        The clientSessionTimeout property
        """
        from .client_session_timeout.client_session_timeout_builder import (
            ClientSessionTimeoutBuilder,
        )

        return ClientSessionTimeoutBuilder(self._request_adapter)

    @property
    def configuration(self) -> ConfigurationBuilder:
        """
        The configuration property
        """
        from .configuration.configuration_builder import ConfigurationBuilder

        return ConfigurationBuilder(self._request_adapter)

    @property
    def password_policy(self) -> PasswordPolicyBuilder:
        """
        The passwordPolicy property
        """
        from .password_policy.password_policy_builder import PasswordPolicyBuilder

        return PasswordPolicyBuilder(self._request_adapter)
