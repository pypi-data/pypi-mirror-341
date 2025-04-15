# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .certificate.certificate_builder import CertificateBuilder
    from .csr.csr_builder import CsrBuilder
    from .rootca.rootca_builder import RootcaBuilder


class VmanageBuilder:
    """
    Builds and executes requests for operations under /sslproxy/settings/vmanage
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
    def csr(self) -> CsrBuilder:
        """
        The csr property
        """
        from .csr.csr_builder import CsrBuilder

        return CsrBuilder(self._request_adapter)

    @property
    def rootca(self) -> RootcaBuilder:
        """
        The rootca property
        """
        from .rootca.rootca_builder import RootcaBuilder

        return RootcaBuilder(self._request_adapter)
