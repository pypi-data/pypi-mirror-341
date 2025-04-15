# Copyright 2024 Cisco Systems, Inc. and its affiliates
from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Union, overload

from catalystwan.abc import RequestAdapterInterface

from . import models
from .models import GetMobilityGlobalFeatureProfileGetResponse, GetSingleMobilityGlobalPayload

if TYPE_CHECKING:
    from .aaaservers.aaaservers_builder import AaaserversBuilder
    from .basic.basic_builder import BasicBuilder
    from .cellular.cellular_builder import CellularBuilder
    from .esimcellular.esimcellular_builder import EsimcellularBuilder
    from .ethernet.ethernet_builder import EthernetBuilder
    from .logging.logging_builder import LoggingBuilder
    from .network_protocol.network_protocol_builder import NetworkProtocolBuilder
    from .qos.qos_builder import QosBuilder
    from .security_policy.security_policy_builder import SecurityPolicyBuilder
    from .vpn.vpn_builder import VpnBuilder
    from .wifi.wifi_builder import WifiBuilder


class GlobalBuilder:
    """
    Builds and executes requests for operations under /v1/feature-profile/mobility/global
    """

    m = models

    def __init__(self, request_adapter: RequestAdapterInterface) -> None:
        self._request_adapter = request_adapter

    @overload
    def get(self, *, global_id: str, **kw) -> GetSingleMobilityGlobalPayload:
        """
        Get a Mobility Global Feature Profile by profileId
        GET /dataservice/v1/feature-profile/mobility/global/{globalId}

        :param global_id: Feature Profile Id
        :returns: GetSingleMobilityGlobalPayload
        """
        ...

    @overload
    def get(
        self,
        *,
        offset: Optional[int] = None,
        limit: Optional[int] = 0,
        reference_count: Optional[bool] = False,
        **kw,
    ) -> List[GetMobilityGlobalFeatureProfileGetResponse]:
        """
        Get Mobility Global Feature Profiles
        GET /dataservice/v1/feature-profile/mobility/global

        :param offset: Pagination offset
        :param limit: Pagination limit
        :param reference_count: get associated group details
        :returns: List[GetMobilityGlobalFeatureProfileGetResponse]
        """
        ...

    def get(
        self,
        *,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        reference_count: Optional[bool] = None,
        global_id: Optional[str] = None,
        **kw,
    ) -> Union[List[GetMobilityGlobalFeatureProfileGetResponse], GetSingleMobilityGlobalPayload]:
        # /dataservice/v1/feature-profile/mobility/global/{globalId}
        if self._request_adapter.param_checker(
            [(global_id, str)], [offset, limit, reference_count]
        ):
            params = {
                "globalId": global_id,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/mobility/global/{globalId}",
                return_type=GetSingleMobilityGlobalPayload,
                params=params,
                **kw,
            )
        # /dataservice/v1/feature-profile/mobility/global
        if self._request_adapter.param_checker([], [global_id]):
            params = {
                "offset": offset,
                "limit": limit,
                "referenceCount": reference_count,
            }
            return self._request_adapter.request(
                "GET",
                "/dataservice/v1/feature-profile/mobility/global",
                return_type=List[GetMobilityGlobalFeatureProfileGetResponse],
                params=params,
                **kw,
            )
        raise RuntimeError("Provided arguments do not match any signature")

    @property
    def aaaservers(self) -> AaaserversBuilder:
        """
        The aaaservers property
        """
        from .aaaservers.aaaservers_builder import AaaserversBuilder

        return AaaserversBuilder(self._request_adapter)

    @property
    def basic(self) -> BasicBuilder:
        """
        The basic property
        """
        from .basic.basic_builder import BasicBuilder

        return BasicBuilder(self._request_adapter)

    @property
    def cellular(self) -> CellularBuilder:
        """
        The cellular property
        """
        from .cellular.cellular_builder import CellularBuilder

        return CellularBuilder(self._request_adapter)

    @property
    def esimcellular(self) -> EsimcellularBuilder:
        """
        The esimcellular property
        """
        from .esimcellular.esimcellular_builder import EsimcellularBuilder

        return EsimcellularBuilder(self._request_adapter)

    @property
    def ethernet(self) -> EthernetBuilder:
        """
        The ethernet property
        """
        from .ethernet.ethernet_builder import EthernetBuilder

        return EthernetBuilder(self._request_adapter)

    @property
    def logging(self) -> LoggingBuilder:
        """
        The logging property
        """
        from .logging.logging_builder import LoggingBuilder

        return LoggingBuilder(self._request_adapter)

    @property
    def network_protocol(self) -> NetworkProtocolBuilder:
        """
        The networkProtocol property
        """
        from .network_protocol.network_protocol_builder import NetworkProtocolBuilder

        return NetworkProtocolBuilder(self._request_adapter)

    @property
    def qos(self) -> QosBuilder:
        """
        The qos property
        """
        from .qos.qos_builder import QosBuilder

        return QosBuilder(self._request_adapter)

    @property
    def security_policy(self) -> SecurityPolicyBuilder:
        """
        The securityPolicy property
        """
        from .security_policy.security_policy_builder import SecurityPolicyBuilder

        return SecurityPolicyBuilder(self._request_adapter)

    @property
    def vpn(self) -> VpnBuilder:
        """
        The vpn property
        """
        from .vpn.vpn_builder import VpnBuilder

        return VpnBuilder(self._request_adapter)

    @property
    def wifi(self) -> WifiBuilder:
        """
        The wifi property
        """
        from .wifi.wifi_builder import WifiBuilder

        return WifiBuilder(self._request_adapter)
