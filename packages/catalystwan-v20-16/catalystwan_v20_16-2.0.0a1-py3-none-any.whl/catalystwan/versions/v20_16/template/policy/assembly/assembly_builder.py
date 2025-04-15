# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .security.security_builder import SecurityBuilder
    from .vedge.vedge_builder import VedgeBuilder
    from .voice.voice_builder import VoiceBuilder
    from .vsmart.vsmart_builder import VsmartBuilder


class AssemblyBuilder:
    """
    Builds and executes requests for operations under /template/policy/assembly
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def security(self) -> SecurityBuilder:
        """
        The security property
        """
        from .security.security_builder import SecurityBuilder

        return SecurityBuilder(self._request_adapter)

    @property
    def vedge(self) -> VedgeBuilder:
        """
        The vedge property
        """
        from .vedge.vedge_builder import VedgeBuilder

        return VedgeBuilder(self._request_adapter)

    @property
    def voice(self) -> VoiceBuilder:
        """
        The voice property
        """
        from .voice.voice_builder import VoiceBuilder

        return VoiceBuilder(self._request_adapter)

    @property
    def vsmart(self) -> VsmartBuilder:
        """
        The vsmart property
        """
        from .vsmart.vsmart_builder import VsmartBuilder

        return VsmartBuilder(self._request_adapter)
