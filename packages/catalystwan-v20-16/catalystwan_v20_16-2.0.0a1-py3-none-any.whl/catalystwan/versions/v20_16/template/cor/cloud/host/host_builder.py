# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .accountdetails.accountdetails_builder import AccountdetailsBuilder


class HostBuilder:
    """
    Builds and executes requests for operations under /template/cor/cloud/host
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def accountdetails(self) -> AccountdetailsBuilder:
        """
        The accountdetails property
        """
        from .accountdetails.accountdetails_builder import AccountdetailsBuilder

        return AccountdetailsBuilder(self._request_adapter)
