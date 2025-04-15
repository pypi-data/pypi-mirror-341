# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .assembly.assembly_builder import AssemblyBuilder
    from .clouddiscoveredapp.clouddiscoveredapp_builder import ClouddiscoveredappBuilder
    from .customapp.customapp_builder import CustomappBuilder
    from .definition.definition_builder import DefinitionBuilder
    from .ise.ise_builder import IseBuilder
    from .list.list_builder import ListBuilder
    from .security.security_builder import SecurityBuilder
    from .vedge.vedge_builder import VedgeBuilder
    from .voice.voice_builder import VoiceBuilder
    from .vsmart.vsmart_builder import VsmartBuilder


class PolicyBuilder:
    """
    Builds and executes requests for operations under /template/policy
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def assembly(self) -> AssemblyBuilder:
        """
        The assembly property
        """
        from .assembly.assembly_builder import AssemblyBuilder

        return AssemblyBuilder(self._request_adapter)

    @property
    def clouddiscoveredapp(self) -> ClouddiscoveredappBuilder:
        """
        The clouddiscoveredapp property
        """
        from .clouddiscoveredapp.clouddiscoveredapp_builder import ClouddiscoveredappBuilder

        return ClouddiscoveredappBuilder(self._request_adapter)

    @property
    def customapp(self) -> CustomappBuilder:
        """
        The customapp property
        """
        from .customapp.customapp_builder import CustomappBuilder

        return CustomappBuilder(self._request_adapter)

    @property
    def definition(self) -> DefinitionBuilder:
        """
        The definition property
        """
        from .definition.definition_builder import DefinitionBuilder

        return DefinitionBuilder(self._request_adapter)

    @property
    def ise(self) -> IseBuilder:
        """
        The ise property
        """
        from .ise.ise_builder import IseBuilder

        return IseBuilder(self._request_adapter)

    @property
    def list(self) -> ListBuilder:
        """
        The list property
        """
        from .list.list_builder import ListBuilder

        return ListBuilder(self._request_adapter)

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
