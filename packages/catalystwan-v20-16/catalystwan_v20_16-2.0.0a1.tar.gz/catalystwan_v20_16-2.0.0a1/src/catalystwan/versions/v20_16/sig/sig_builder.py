# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .datacenters.datacenters_builder import DatacentersBuilder
    from .sig_global_credentials.sig_global_credentials_builder import SigGlobalCredentialsBuilder
    from .umbrella.umbrella_builder import UmbrellaBuilder


class SigBuilder:
    """
    Builds and executes requests for operations under /sig
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def datacenters(self) -> DatacentersBuilder:
        """
        The datacenters property
        """
        from .datacenters.datacenters_builder import DatacentersBuilder

        return DatacentersBuilder(self._request_adapter)

    @property
    def sig_global_credentials(self) -> SigGlobalCredentialsBuilder:
        """
        The sigGlobalCredentials property
        """
        from .sig_global_credentials.sig_global_credentials_builder import (
            SigGlobalCredentialsBuilder,
        )

        return SigGlobalCredentialsBuilder(self._request_adapter)

    @property
    def umbrella(self) -> UmbrellaBuilder:
        """
        The umbrella property
        """
        from .umbrella.umbrella_builder import UmbrellaBuilder

        return UmbrellaBuilder(self._request_adapter)
