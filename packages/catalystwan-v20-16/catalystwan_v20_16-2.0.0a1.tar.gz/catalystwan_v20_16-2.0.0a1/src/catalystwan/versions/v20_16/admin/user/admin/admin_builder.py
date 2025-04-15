# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .password.password_builder import PasswordBuilder


class AdminBuilder:
    """
    Builds and executes requests for operations under /admin/user/admin
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def password(self) -> PasswordBuilder:
        """
        The password property
        """
        from .password.password_builder import PasswordBuilder

        return PasswordBuilder(self._request_adapter)
