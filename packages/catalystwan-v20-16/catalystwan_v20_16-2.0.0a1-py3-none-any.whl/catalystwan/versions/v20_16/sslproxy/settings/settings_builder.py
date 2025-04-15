# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .certificate.certificate_builder import CertificateBuilder
    from .enterprise.enterprise_builder import EnterpriseBuilder
    from .vmanage.vmanage_builder import VmanageBuilder


class SettingsBuilder:
    """
    Builds and executes requests for operations under /sslproxy/settings
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def certificate(self) -> CertificateBuilder:
        """
        The certificate property
        """
        from .certificate.certificate_builder import CertificateBuilder

        return CertificateBuilder(self._request_adapter)

    @property
    def enterprise(self) -> EnterpriseBuilder:
        """
        The enterprise property
        """
        from .enterprise.enterprise_builder import EnterpriseBuilder

        return EnterpriseBuilder(self._request_adapter)

    @property
    def vmanage(self) -> VmanageBuilder:
        """
        The vmanage property
        """
        from .vmanage.vmanage_builder import VmanageBuilder

        return VmanageBuilder(self._request_adapter)
