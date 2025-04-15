# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .swversion.swversion_builder import SwversionBuilder


class RemotedcBuilder:
    """
    Builds and executes requests for operations under /disasterrecovery/remotedc
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    def get(self, **kw) -> List[Any]:
        """
        Get remote data center details
        GET /dataservice/disasterrecovery/remotedc

        :returns: List[Any]
        """
        return self._request_adapter.request(
            "GET", "/dataservice/disasterrecovery/remotedc", return_type=List[Any], **kw
        )

    @property
    def swversion(self) -> SwversionBuilder:
        """
        The swversion property
        """
        from .swversion.swversion_builder import SwversionBuilder

        return SwversionBuilder(self._request_adapter)
