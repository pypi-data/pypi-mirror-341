# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING

from catalystwan.abc import RequestAdapterInterface

if TYPE_CHECKING:
    from .service_chain_mapping.service_chain_mapping_builder import ServiceChainMappingBuilder


class ServiceInsertionBuilder:
    """
    Builds and executes requests for operations under /v1/service-insertion
    """

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @property
    def service_chain_mapping(self) -> ServiceChainMappingBuilder:
        """
        The service-chain-mapping property
        """
        from .service_chain_mapping.service_chain_mapping_builder import ServiceChainMappingBuilder

        return ServiceChainMappingBuilder(self._request_adapter)
