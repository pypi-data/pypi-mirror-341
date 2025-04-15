# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .signed_cert.signed_cert_builder import SignedCertBuilder


class InstallBuilder:
    """
    Builds and executes requests for operations under /certificate/install
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def signed_cert(self) -> SignedCertBuilder:
        """
        The signedCert property
        """
        from .signed_cert.signed_cert_builder import SignedCertBuilder

        return SignedCertBuilder(self._request_adapter)
