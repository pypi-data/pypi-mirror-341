# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .addcloudx.addcloudx_builder import AddcloudxBuilder
    from .attachedclient.attachedclient_builder import AttachedclientBuilder
    from .attacheddia.attacheddia_builder import AttacheddiaBuilder
    from .attachedgateway.attachedgateway_builder import AttachedgatewayBuilder
    from .availableapps.availableapps_builder import AvailableappsBuilder
    from .clientlist.clientlist_builder import ClientlistBuilder
    from .dialist.dialist_builder import DialistBuilder
    from .gatewaylist.gatewaylist_builder import GatewaylistBuilder
    from .interfaces.interfaces_builder import InterfacesBuilder
    from .manage.manage_builder import ManageBuilder
    from .sig_tunnels.sig_tunnels_builder import SigTunnelsBuilder
    from .status.status_builder import StatusBuilder


class CloudxBuilder:
    """
    Builds and executes requests for operations under /template/cloudx
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[Any]:
        """
        Get CloudX feature list
        GET /dataservice/template/cloudx

        :returns: List[Any]
        """
        return self._request_adapter.request(
            "GET", "/dataservice/template/cloudx", return_type=List[Any], **kw
        )

    @property
    def addcloudx(self) -> AddcloudxBuilder:
        """
        The addcloudx property
        """
        from .addcloudx.addcloudx_builder import AddcloudxBuilder

        return AddcloudxBuilder(self._request_adapter)

    @property
    def attachedclient(self) -> AttachedclientBuilder:
        """
        The attachedclient property
        """
        from .attachedclient.attachedclient_builder import AttachedclientBuilder

        return AttachedclientBuilder(self._request_adapter)

    @property
    def attacheddia(self) -> AttacheddiaBuilder:
        """
        The attacheddia property
        """
        from .attacheddia.attacheddia_builder import AttacheddiaBuilder

        return AttacheddiaBuilder(self._request_adapter)

    @property
    def attachedgateway(self) -> AttachedgatewayBuilder:
        """
        The attachedgateway property
        """
        from .attachedgateway.attachedgateway_builder import AttachedgatewayBuilder

        return AttachedgatewayBuilder(self._request_adapter)

    @property
    def availableapps(self) -> AvailableappsBuilder:
        """
        The availableapps property
        """
        from .availableapps.availableapps_builder import AvailableappsBuilder

        return AvailableappsBuilder(self._request_adapter)

    @property
    def clientlist(self) -> ClientlistBuilder:
        """
        The clientlist property
        """
        from .clientlist.clientlist_builder import ClientlistBuilder

        return ClientlistBuilder(self._request_adapter)

    @property
    def dialist(self) -> DialistBuilder:
        """
        The dialist property
        """
        from .dialist.dialist_builder import DialistBuilder

        return DialistBuilder(self._request_adapter)

    @property
    def gatewaylist(self) -> GatewaylistBuilder:
        """
        The gatewaylist property
        """
        from .gatewaylist.gatewaylist_builder import GatewaylistBuilder

        return GatewaylistBuilder(self._request_adapter)

    @property
    def interfaces(self) -> InterfacesBuilder:
        """
        The interfaces property
        """
        from .interfaces.interfaces_builder import InterfacesBuilder

        return InterfacesBuilder(self._request_adapter)

    @property
    def manage(self) -> ManageBuilder:
        """
        The manage property
        """
        from .manage.manage_builder import ManageBuilder

        return ManageBuilder(self._request_adapter)

    @property
    def sig_tunnels(self) -> SigTunnelsBuilder:
        """
        The sig_tunnels property
        """
        from .sig_tunnels.sig_tunnels_builder import SigTunnelsBuilder

        return SigTunnelsBuilder(self._request_adapter)

    @property
    def status(self) -> StatusBuilder:
        """
        The status property
        """
        from .status.status_builder import StatusBuilder

        return StatusBuilder(self._request_adapter)
