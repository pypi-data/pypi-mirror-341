# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .connect.connect_builder import ConnectBuilder
    from .credentials.credentials_builder import CredentialsBuilder
    from .pxgrid.pxgrid_builder import PxgridBuilder


class IseBuilder:
    """
    Builds and executes requests for operations under /ise
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def connect(self) -> ConnectBuilder:
        """
        The connect property
        """
        from .connect.connect_builder import ConnectBuilder

        return ConnectBuilder(self._request_adapter)

    @property
    def credentials(self) -> CredentialsBuilder:
        """
        The credentials property
        """
        from .credentials.credentials_builder import CredentialsBuilder

        return CredentialsBuilder(self._request_adapter)

    @property
    def pxgrid(self) -> PxgridBuilder:
        """
        The pxgrid property
        """
        from .pxgrid.pxgrid_builder import PxgridBuilder

        return PxgridBuilder(self._request_adapter)
