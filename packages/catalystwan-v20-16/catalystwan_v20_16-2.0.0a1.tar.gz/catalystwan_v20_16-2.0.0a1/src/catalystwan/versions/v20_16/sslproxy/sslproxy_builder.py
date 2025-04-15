# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .certificate.certificate_builder import CertificateBuilder
    from .certificates.certificates_builder import CertificatesBuilder
    from .csr.csr_builder import CsrBuilder
    from .devicecertificates.devicecertificates_builder import DevicecertificatesBuilder
    from .devicecsr.devicecsr_builder import DevicecsrBuilder
    from .generate.generate_builder import GenerateBuilder
    from .list.list_builder import ListBuilder
    from .renew.renew_builder import RenewBuilder
    from .revoke.revoke_builder import RevokeBuilder
    from .revokerenew.revokerenew_builder import RevokerenewBuilder
    from .settings.settings_builder import SettingsBuilder


class SslproxyBuilder:
    """
    Builds and executes requests for operations under /sslproxy
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
    def certificates(self) -> CertificatesBuilder:
        """
        The certificates property
        """
        from .certificates.certificates_builder import CertificatesBuilder

        return CertificatesBuilder(self._request_adapter)

    @property
    def csr(self) -> CsrBuilder:
        """
        The csr property
        """
        from .csr.csr_builder import CsrBuilder

        return CsrBuilder(self._request_adapter)

    @property
    def devicecertificates(self) -> DevicecertificatesBuilder:
        """
        The devicecertificates property
        """
        from .devicecertificates.devicecertificates_builder import DevicecertificatesBuilder

        return DevicecertificatesBuilder(self._request_adapter)

    @property
    def devicecsr(self) -> DevicecsrBuilder:
        """
        The devicecsr property
        """
        from .devicecsr.devicecsr_builder import DevicecsrBuilder

        return DevicecsrBuilder(self._request_adapter)

    @property
    def generate(self) -> GenerateBuilder:
        """
        The generate property
        """
        from .generate.generate_builder import GenerateBuilder

        return GenerateBuilder(self._request_adapter)

    @property
    def list(self) -> ListBuilder:
        """
        The list property
        """
        from .list.list_builder import ListBuilder

        return ListBuilder(self._request_adapter)

    @property
    def renew(self) -> RenewBuilder:
        """
        The renew property
        """
        from .renew.renew_builder import RenewBuilder

        return RenewBuilder(self._request_adapter)

    @property
    def revoke(self) -> RevokeBuilder:
        """
        The revoke property
        """
        from .revoke.revoke_builder import RevokeBuilder

        return RevokeBuilder(self._request_adapter)

    @property
    def revokerenew(self) -> RevokerenewBuilder:
        """
        The revokerenew property
        """
        from .revokerenew.revokerenew_builder import RevokerenewBuilder

        return RevokerenewBuilder(self._request_adapter)

    @property
    def settings(self) -> SettingsBuilder:
        """
        The settings property
        """
        from .settings.settings_builder import SettingsBuilder

        return SettingsBuilder(self._request_adapter)
