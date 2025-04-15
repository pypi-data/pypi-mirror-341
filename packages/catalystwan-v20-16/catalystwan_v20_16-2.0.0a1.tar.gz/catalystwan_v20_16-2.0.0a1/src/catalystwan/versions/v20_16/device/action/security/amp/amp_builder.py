# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .apikey.apikey_builder import ApikeyBuilder
    from .rekey.rekey_builder import RekeyBuilder


class AmpBuilder:
    """
    Builds and executes requests for operations under /device/action/security/amp
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def apikey(self) -> ApikeyBuilder:
        """
        The apikey property
        """
        from .apikey.apikey_builder import ApikeyBuilder

        return ApikeyBuilder(self._request_adapter)

    @property
    def rekey(self) -> RekeyBuilder:
        """
        The rekey property
        """
        from .rekey.rekey_builder import RekeyBuilder

        return RekeyBuilder(self._request_adapter)
