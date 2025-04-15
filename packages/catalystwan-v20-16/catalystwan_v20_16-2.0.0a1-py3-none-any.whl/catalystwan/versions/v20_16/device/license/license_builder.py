# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .evaluation.evaluation_builder import EvaluationBuilder
    from .pak.pak_builder import PakBuilder
    from .privacy.privacy_builder import PrivacyBuilder
    from .registration.registration_builder import RegistrationBuilder
    from .udi.udi_builder import UdiBuilder
    from .usage.usage_builder import UsageBuilder


class LicenseBuilder:
    """
    Builds and executes requests for operations under /device/license
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def evaluation(self) -> EvaluationBuilder:
        """
        The evaluation property
        """
        from .evaluation.evaluation_builder import EvaluationBuilder

        return EvaluationBuilder(self._request_adapter)

    @property
    def pak(self) -> PakBuilder:
        """
        The pak property
        """
        from .pak.pak_builder import PakBuilder

        return PakBuilder(self._request_adapter)

    @property
    def privacy(self) -> PrivacyBuilder:
        """
        The privacy property
        """
        from .privacy.privacy_builder import PrivacyBuilder

        return PrivacyBuilder(self._request_adapter)

    @property
    def registration(self) -> RegistrationBuilder:
        """
        The registration property
        """
        from .registration.registration_builder import RegistrationBuilder

        return RegistrationBuilder(self._request_adapter)

    @property
    def udi(self) -> UdiBuilder:
        """
        The udi property
        """
        from .udi.udi_builder import UdiBuilder

        return UdiBuilder(self._request_adapter)

    @property
    def usage(self) -> UsageBuilder:
        """
        The usage property
        """
        from .usage.usage_builder import UsageBuilder

        return UsageBuilder(self._request_adapter)
