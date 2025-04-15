# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .certificate.certificate_builder import CertificateBuilder
    from .devicecsr.devicecsr_builder import DevicecsrBuilder
    from .revoke.revoke_builder import RevokeBuilder
    from .syslogconfig.syslogconfig_builder import SyslogconfigBuilder


class FeaturecertificateBuilder:
    """
    Builds and executes requests for operations under /featurecertificate
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
    def devicecsr(self) -> DevicecsrBuilder:
        """
        The devicecsr property
        """
        from .devicecsr.devicecsr_builder import DevicecsrBuilder

        return DevicecsrBuilder(self._request_adapter)

    @property
    def revoke(self) -> RevokeBuilder:
        """
        The revoke property
        """
        from .revoke.revoke_builder import RevokeBuilder

        return RevokeBuilder(self._request_adapter)

    @property
    def syslogconfig(self) -> SyslogconfigBuilder:
        """
        The syslogconfig property
        """
        from .syslogconfig.syslogconfig_builder import SyslogconfigBuilder

        return SyslogconfigBuilder(self._request_adapter)
