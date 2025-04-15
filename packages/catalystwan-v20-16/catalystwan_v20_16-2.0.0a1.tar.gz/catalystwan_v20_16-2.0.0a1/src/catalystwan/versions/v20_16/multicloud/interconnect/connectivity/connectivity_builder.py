# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .cloud_onramp_gateway_connections.cloud_onramp_gateway_connections_builder import (
        CloudOnrampGatewayConnectionsBuilder,
    )
    from .connections.connections_builder import ConnectionsBuilder
    from .device_links.device_links_builder import DeviceLinksBuilder
    from .virtual_cross_connections.virtual_cross_connections_builder import (
        VirtualCrossConnectionsBuilder,
    )
    from .virtual_network_connections.virtual_network_connections_builder import (
        VirtualNetworkConnectionsBuilder,
    )


class ConnectivityBuilder:
    """
    Builds and executes requests for operations under /multicloud/interconnect/connectivity
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def cloud_onramp_gateway_connections(self) -> CloudOnrampGatewayConnectionsBuilder:
        """
        The cloud-onramp-gateway-connections property
        """
        from .cloud_onramp_gateway_connections.cloud_onramp_gateway_connections_builder import (
            CloudOnrampGatewayConnectionsBuilder,
        )

        return CloudOnrampGatewayConnectionsBuilder(self._request_adapter)

    @property
    def connections(self) -> ConnectionsBuilder:
        """
        The connections property
        """
        from .connections.connections_builder import ConnectionsBuilder

        return ConnectionsBuilder(self._request_adapter)

    @property
    def device_links(self) -> DeviceLinksBuilder:
        """
        The device-links property
        """
        from .device_links.device_links_builder import DeviceLinksBuilder

        return DeviceLinksBuilder(self._request_adapter)

    @property
    def virtual_cross_connections(self) -> VirtualCrossConnectionsBuilder:
        """
        The virtual-cross-connections property
        """
        from .virtual_cross_connections.virtual_cross_connections_builder import (
            VirtualCrossConnectionsBuilder,
        )

        return VirtualCrossConnectionsBuilder(self._request_adapter)

    @property
    def virtual_network_connections(self) -> VirtualNetworkConnectionsBuilder:
        """
        The virtual-network-connections property
        """
        from .virtual_network_connections.virtual_network_connections_builder import (
            VirtualNetworkConnectionsBuilder,
        )

        return VirtualNetworkConnectionsBuilder(self._request_adapter)
