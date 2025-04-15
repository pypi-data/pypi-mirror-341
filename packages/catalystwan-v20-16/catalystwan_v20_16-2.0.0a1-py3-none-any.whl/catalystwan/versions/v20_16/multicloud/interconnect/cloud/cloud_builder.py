# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .accounts.accounts_builder import AccountsBuilder
    from .cloud_connectivity_gateways.cloud_connectivity_gateways_builder import (
        CloudConnectivityGatewaysBuilder,
    )


class CloudBuilder:
    """
    Builds and executes requests for operations under /multicloud/interconnect/cloud
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def accounts(self) -> AccountsBuilder:
        """
        The accounts property
        """
        from .accounts.accounts_builder import AccountsBuilder

        return AccountsBuilder(self._request_adapter)

    @property
    def cloud_connectivity_gateways(self) -> CloudConnectivityGatewaysBuilder:
        """
        The cloud-connectivity-gateways property
        """
        from .cloud_connectivity_gateways.cloud_connectivity_gateways_builder import (
            CloudConnectivityGatewaysBuilder,
        )

        return CloudConnectivityGatewaysBuilder(self._request_adapter)
