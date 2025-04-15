# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .status.status_builder import StatusBuilder


class PolicyBuilder:
    """
    Builds and executes requests for operations under /sdavc/protocol-pack/compliance/policy
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(
        self,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        protocol_pack_name: Optional[str] = None,
        old_application_source: Optional[str] = None,
        **kw,
    ) -> Any:
        """
        Get all policy compliance details
        GET /dataservice/sdavc/protocol-pack/compliance/policy

        :param offset: Starting position of records
        :param limit: Total records to query after offset
        :param protocol_pack_name: Protocol pack name
        :param old_application_source: Old application source
        :returns: Any
        """
        params = {
            "offset": offset,
            "limit": limit,
            "protocolPackName": protocol_pack_name,
            "oldApplicationSource": old_application_source,
        }
        return self._request_adapter.request(
            "GET", "/dataservice/sdavc/protocol-pack/compliance/policy", params=params, **kw
        )

    @property
    def status(self) -> StatusBuilder:
        """
        The status property
        """
        from .status.status_builder import StatusBuilder

        return StatusBuilder(self._request_adapter)
