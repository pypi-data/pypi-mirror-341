# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

VariableOptionTypeDef = Literal["variable"]

DefaultOptionTypeDef = Literal["default"]

Ipv4SubnetMaskDef = Literal[
    "0.0.0.0",
    "128.0.0.0",
    "192.0.0.0",
    "224.0.0.0",
    "240.0.0.0",
    "248.0.0.0",
    "252.0.0.0",
    "254.0.0.0",
    "255.0.0.0",
    "255.128.0.0",
    "255.192.0.0",
    "255.224.0.0",
    "255.240.0.0",
    "255.252.0.0",
    "255.254.0.0",
    "255.255.0.0",
    "255.255.128.0",
    "255.255.192.0",
    "255.255.224.0",
    "255.255.240.0",
    "255.255.248.0",
    "255.255.252.0",
    "255.255.254.0",
    "255.255.255.0",
    "255.255.255.128",
    "255.255.255.192",
    "255.255.255.224",
    "255.255.255.240",
    "255.255.255.248",
    "255.255.255.252",
    "255.255.255.254",
    "255.255.255.255",
]

Value = Literal["ipv4-unicast"]

BgpValue = Literal["disable-peer", "warning-only"]

RoutingBgpValue = Literal["ipv6-unicast"]

Ipv4AddressFamilyRedistributeProtocolDef = Literal["connected", "ospf", "ospfv3", "static"]

OspfMatchRouteListDef = Literal["External-type1", "External-type2", "Internal"]

Ipv6AddressFamilyRedistributeProtocolDef = Literal["connected", "ospf", "static"]

GlobalVrfRoutingBgpValue = Literal["disable-peer", "warning-only"]

TransportGlobalVrfRoutingBgpValue = Literal["disable-peer", "warning-only"]

SdRoutingTransportGlobalVrfRoutingBgpValue = Literal["ipv6-unicast"]

FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpValue = Literal["disable-peer", "warning-only"]

V1FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpValue = Literal["disable-peer", "warning-only"]

BgpIpv4AddressFamilyRedistributeProtocolDef = Literal[
    "connected", "eigrp", "ospf", "ospfv3", "static"
]

BgpOspfMatchRouteListDef = Literal["External-type1", "External-type2", "Internal"]

BgpIpv6AddressFamilyRedistributeProtocolDef = Literal["connected", "ospf", "static"]

RoutingBgpOspfMatchRouteListDef = Literal["External-type1", "External-type2", "Internal"]

Value1 = Literal["disable-peer", "warning-only"]

Value2 = Literal["disable-peer", "warning-only"]

Value3 = Literal["disable-peer", "warning-only"]

Value4 = Literal["disable-peer", "warning-only"]

RoutingBgpIpv4AddressFamilyRedistributeProtocolDef = Literal[
    "connected", "eigrp", "ospf", "ospfv3", "static"
]

GlobalVrfRoutingBgpOspfMatchRouteListDef = Literal["External-type1", "External-type2", "Internal"]

RoutingBgpIpv6AddressFamilyRedistributeProtocolDef = Literal["connected", "ospf", "static"]

TransportGlobalVrfRoutingBgpOspfMatchRouteListDef = Literal[
    "External-type1", "External-type2", "Internal"
]


@dataclass
class OneOfAsNumOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Union[int, str]


@dataclass
class OneOfAsNumOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfRouterIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfRouterIdOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfRouterIdOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfExternalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfExternalOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfExternalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfInternalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfInternalOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInternalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfLocalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfLocalOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfLocalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfKeepaliveOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfKeepaliveOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfKeepaliveOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfHoldtimeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfHoldtimeOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfHoldtimeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfOnBooleanDefaultFalseOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfOnBooleanDefaultFalseOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfOnBooleanDefaultFalseOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfMaxListenPrefixNumOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfMaxListenPrefixNumOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfMaxListenPrefixNumOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNeighborPeerGroupNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfIpV4AddressOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpV4AddressOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfIpV4SubnetMaskOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpV4SubnetMaskOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Ipv4SubnetMaskDef  # pytype: disable=annotation-type-mismatch


@dataclass
class Ipv4AddressAndMaskDef:
    address: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2]
    mask: Union[OneOfIpV4SubnetMaskOptionsDef1, OneOfIpV4SubnetMaskOptionsDef2]


@dataclass
class Ipv4Address:
    address: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2]


@dataclass
class Ipv4PeerGroup:
    peer_group_name: OneOfNeighborPeerGroupNameOptionsDef = _field(
        metadata={"alias": "peerGroupName"}
    )
    # Peer Group IPv4 subnet range
    range: List[Ipv4AddressAndMaskDef]
    # Peer Group IPv4 Address list
    ipv4_address: Optional[List[Ipv4Address]] = _field(
        default=None, metadata={"alias": "ipv4Address"}
    )


@dataclass
class OneOfIpv6PrefixGlobalVariableWithoutDefault1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfIpv6PrefixGlobalVariableWithoutDefault2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class Range:
    prefix: Union[
        OneOfIpv6PrefixGlobalVariableWithoutDefault1, OneOfIpv6PrefixGlobalVariableWithoutDefault2
    ]


@dataclass
class OneOfIpv6AddrGlobalVariableOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfIpv6AddrGlobalVariableOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class Ipv6Address:
    address: Union[OneOfIpv6AddrGlobalVariableOptionsDef1, OneOfIpv6AddrGlobalVariableOptionsDef2]


@dataclass
class Ipv6PeerGroup:
    peer_group_name: OneOfNeighborPeerGroupNameOptionsDef = _field(
        metadata={"alias": "peerGroupName"}
    )
    # Peer Group IPv6 prefix range
    range: List[Range]
    # Peer Group IPv6 Address list
    ipv6_address: Optional[List[Ipv6Address]] = _field(
        default=None, metadata={"alias": "ipv6Address"}
    )


@dataclass
class DynamicNeighbor1:
    # IPv4 Peer groups
    ipv4_peer_group: List[Ipv4PeerGroup] = _field(metadata={"alias": "ipv4PeerGroup"})
    max_listen_prefix_limit: Union[
        OneOfMaxListenPrefixNumOptionsDef1,
        OneOfMaxListenPrefixNumOptionsDef2,
        OneOfMaxListenPrefixNumOptionsDef3,
    ] = _field(metadata={"alias": "maxListenPrefixLimit"})
    # IPv6 Peer groups
    ipv6_peer_group: Optional[List[Ipv6PeerGroup]] = _field(
        default=None, metadata={"alias": "ipv6PeerGroup"}
    )


@dataclass
class DynamicNeighbor2:
    # IPv6 Peer groups
    ipv6_peer_group: List[Ipv6PeerGroup] = _field(metadata={"alias": "ipv6PeerGroup"})
    max_listen_prefix_limit: Union[
        OneOfMaxListenPrefixNumOptionsDef1,
        OneOfMaxListenPrefixNumOptionsDef2,
        OneOfMaxListenPrefixNumOptionsDef3,
    ] = _field(metadata={"alias": "maxListenPrefixLimit"})
    # IPv4 Peer groups
    ipv4_peer_group: Optional[List[Ipv4PeerGroup]] = _field(
        default=None, metadata={"alias": "ipv4PeerGroup"}
    )


@dataclass
class DynamicNeighbor3:
    # IPv4 Peer groups
    ipv4_peer_group: List[Ipv4PeerGroup] = _field(metadata={"alias": "ipv4PeerGroup"})
    # IPv6 Peer groups
    ipv6_peer_group: List[Ipv6PeerGroup] = _field(metadata={"alias": "ipv6PeerGroup"})
    max_listen_prefix_limit: Union[
        OneOfMaxListenPrefixNumOptionsDef1,
        OneOfMaxListenPrefixNumOptionsDef2,
        OneOfMaxListenPrefixNumOptionsDef3,
    ] = _field(metadata={"alias": "maxListenPrefixLimit"})


@dataclass
class OneOfNeighborDescriptionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfNeighborDescriptionOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfNeighborDescriptionOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfLocalAsOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Union[int, str]


@dataclass
class OneOfLocalAsOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfLocalAsOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfInterfaceNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfInterfaceNameOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceNameOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfOnBooleanDefaultTrueOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfOnBooleanDefaultTrueOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfOnBooleanDefaultTrueOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfNeighborEbgpMultihopOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNeighborEbgpMultihopOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfNeighborEbgpMultihopOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNeighborPasswordOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfNeighborPasswordOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfNeighborPasswordOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfNeighborAsNumberOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNeighborAsNumberOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfNeighborAsNumberOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class WanIpv4NeighborAfTypeDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Value


@dataclass
class PolicyType:
    """
    Neighbor received maximum prefix policy is disabled.
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class NeighborMaxPrefixConfigDef1:
    # Neighbor received maximum prefix policy is disabled.
    policy_type: PolicyType = _field(metadata={"alias": "policyType"})


@dataclass
class BgpPolicyType:
    """
    Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is restarting device.
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfNeighborMaxPrefixNumOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNeighborMaxPrefixNumOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfNeighborAddressFamilyThresholdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNeighborAddressFamilyThresholdOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfNeighborAddressFamilyThresholdOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNeighborMaxPrefixExceedRestartTimeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNeighborMaxPrefixExceedRestartTimeOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class NeighborMaxPrefixConfigDef2:
    # Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is restarting device.
    policy_type: BgpPolicyType = _field(metadata={"alias": "policyType"})
    prefix_num: Union[
        OneOfNeighborMaxPrefixNumOptionsDef1, OneOfNeighborMaxPrefixNumOptionsDef2
    ] = _field(metadata={"alias": "prefixNum"})
    restart_interval: Union[
        OneOfNeighborMaxPrefixExceedRestartTimeOptionsDef1,
        OneOfNeighborMaxPrefixExceedRestartTimeOptionsDef2,
    ] = _field(metadata={"alias": "restartInterval"})
    threshold: Union[
        OneOfNeighborAddressFamilyThresholdOptionsDef1,
        OneOfNeighborAddressFamilyThresholdOptionsDef2,
        OneOfNeighborAddressFamilyThresholdOptionsDef3,
    ]


@dataclass
class RoutingBgpPolicyType:
    """
    Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is warning-only or disable-peer.
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: BgpValue  # pytype: disable=annotation-type-mismatch


@dataclass
class NeighborMaxPrefixConfigDef3:
    # Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is warning-only or disable-peer.
    policy_type: RoutingBgpPolicyType = _field(metadata={"alias": "policyType"})
    prefix_num: Union[
        OneOfNeighborMaxPrefixNumOptionsDef1, OneOfNeighborMaxPrefixNumOptionsDef2
    ] = _field(metadata={"alias": "prefixNum"})
    threshold: Union[
        OneOfNeighborAddressFamilyThresholdOptionsDef1,
        OneOfNeighborAddressFamilyThresholdOptionsDef2,
        OneOfNeighborAddressFamilyThresholdOptionsDef3,
    ]


@dataclass
class OneOfRoutePolicyNameOptionsDef1:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class RefId:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfRoutePolicyNameOptionsDef2:
    ref_id: RefId = _field(metadata={"alias": "refId"})


@dataclass
class AddressFamily:
    family_type: WanIpv4NeighborAfTypeDef = _field(metadata={"alias": "familyType"})
    in_route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "inRoutePolicy"})
    max_prefix_config: Optional[
        Union[NeighborMaxPrefixConfigDef1, NeighborMaxPrefixConfigDef2, NeighborMaxPrefixConfigDef3]
    ] = _field(default=None, metadata={"alias": "maxPrefixConfig"})
    out_route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "outRoutePolicy"})


@dataclass
class Neighbor1:
    address: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2]
    remote_as: Union[OneOfAsNumOptionsDef1, OneOfAsNumOptionsDef2] = _field(
        metadata={"alias": "remoteAs"}
    )
    # Set BGP address family
    address_family: Optional[List[AddressFamily]] = _field(
        default=None, metadata={"alias": "addressFamily"}
    )
    as_number: Optional[
        Union[
            OneOfNeighborAsNumberOptionsDef1,
            OneOfNeighborAsNumberOptionsDef2,
            OneOfNeighborAsNumberOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "asNumber"})
    as_override: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "asOverride"})
    description: Optional[
        Union[
            OneOfNeighborDescriptionOptionsDef1,
            OneOfNeighborDescriptionOptionsDef2,
            OneOfNeighborDescriptionOptionsDef3,
        ]
    ] = _field(default=None)
    ebgp_multihop: Optional[
        Union[
            OneOfNeighborEbgpMultihopOptionsDef1,
            OneOfNeighborEbgpMultihopOptionsDef2,
            OneOfNeighborEbgpMultihopOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ebgpMultihop"})
    fall_over_bfd: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "fallOverBfd"})
    holdtime: Optional[
        Union[OneOfHoldtimeOptionsDef1, OneOfHoldtimeOptionsDef2, OneOfHoldtimeOptionsDef3]
    ] = _field(default=None)
    if_name: Optional[
        Union[
            OneOfInterfaceNameOptionsDef1,
            OneOfInterfaceNameOptionsDef2,
            OneOfInterfaceNameOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ifName"})
    keepalive: Optional[
        Union[OneOfKeepaliveOptionsDef1, OneOfKeepaliveOptionsDef2, OneOfKeepaliveOptionsDef3]
    ] = _field(default=None)
    local_as: Optional[
        Union[OneOfLocalAsOptionsDef1, OneOfLocalAsOptionsDef2, OneOfLocalAsOptionsDef3]
    ] = _field(default=None, metadata={"alias": "localAs"})
    next_hop_self: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "nextHopSelf"})
    password: Optional[
        Union[
            OneOfNeighborPasswordOptionsDef1,
            OneOfNeighborPasswordOptionsDef2,
            OneOfNeighborPasswordOptionsDef3,
        ]
    ] = _field(default=None)
    peer_group: Optional[OneOfNeighborPeerGroupNameOptionsDef] = _field(
        default=None, metadata={"alias": "peerGroup"}
    )
    route_reflect_client: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "routeReflectClient"})
    send_community: Optional[
        Union[
            OneOfOnBooleanDefaultTrueOptionsDef1,
            OneOfOnBooleanDefaultTrueOptionsDef2,
            OneOfOnBooleanDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sendCommunity"})
    send_ext_community: Optional[
        Union[
            OneOfOnBooleanDefaultTrueOptionsDef1,
            OneOfOnBooleanDefaultTrueOptionsDef2,
            OneOfOnBooleanDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sendExtCommunity"})
    shutdown: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class Neighbor2:
    peer_group: OneOfNeighborPeerGroupNameOptionsDef = _field(metadata={"alias": "peerGroup"})
    remote_as: Union[OneOfAsNumOptionsDef1, OneOfAsNumOptionsDef2] = _field(
        metadata={"alias": "remoteAs"}
    )
    address: Optional[Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2]] = _field(
        default=None
    )
    # Set BGP address family
    address_family: Optional[List[AddressFamily]] = _field(
        default=None, metadata={"alias": "addressFamily"}
    )
    as_number: Optional[
        Union[
            OneOfNeighborAsNumberOptionsDef1,
            OneOfNeighborAsNumberOptionsDef2,
            OneOfNeighborAsNumberOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "asNumber"})
    as_override: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "asOverride"})
    description: Optional[
        Union[
            OneOfNeighborDescriptionOptionsDef1,
            OneOfNeighborDescriptionOptionsDef2,
            OneOfNeighborDescriptionOptionsDef3,
        ]
    ] = _field(default=None)
    ebgp_multihop: Optional[
        Union[
            OneOfNeighborEbgpMultihopOptionsDef1,
            OneOfNeighborEbgpMultihopOptionsDef2,
            OneOfNeighborEbgpMultihopOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ebgpMultihop"})
    fall_over_bfd: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "fallOverBfd"})
    holdtime: Optional[
        Union[OneOfHoldtimeOptionsDef1, OneOfHoldtimeOptionsDef2, OneOfHoldtimeOptionsDef3]
    ] = _field(default=None)
    if_name: Optional[
        Union[
            OneOfInterfaceNameOptionsDef1,
            OneOfInterfaceNameOptionsDef2,
            OneOfInterfaceNameOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ifName"})
    keepalive: Optional[
        Union[OneOfKeepaliveOptionsDef1, OneOfKeepaliveOptionsDef2, OneOfKeepaliveOptionsDef3]
    ] = _field(default=None)
    local_as: Optional[
        Union[OneOfLocalAsOptionsDef1, OneOfLocalAsOptionsDef2, OneOfLocalAsOptionsDef3]
    ] = _field(default=None, metadata={"alias": "localAs"})
    next_hop_self: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "nextHopSelf"})
    password: Optional[
        Union[
            OneOfNeighborPasswordOptionsDef1,
            OneOfNeighborPasswordOptionsDef2,
            OneOfNeighborPasswordOptionsDef3,
        ]
    ] = _field(default=None)
    route_reflect_client: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "routeReflectClient"})
    send_community: Optional[
        Union[
            OneOfOnBooleanDefaultTrueOptionsDef1,
            OneOfOnBooleanDefaultTrueOptionsDef2,
            OneOfOnBooleanDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sendCommunity"})
    send_ext_community: Optional[
        Union[
            OneOfOnBooleanDefaultTrueOptionsDef1,
            OneOfOnBooleanDefaultTrueOptionsDef2,
            OneOfOnBooleanDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sendExtCommunity"})
    shutdown: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class WanIpv6NeighborAfTypeDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: RoutingBgpValue


@dataclass
class BgpAddressFamily:
    family_type: WanIpv6NeighborAfTypeDef = _field(metadata={"alias": "familyType"})
    in_route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "inRoutePolicy"})
    max_prefix_config: Optional[
        Union[NeighborMaxPrefixConfigDef1, NeighborMaxPrefixConfigDef2, NeighborMaxPrefixConfigDef3]
    ] = _field(default=None, metadata={"alias": "maxPrefixConfig"})
    out_route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "outRoutePolicy"})


@dataclass
class Ipv6Neighbor1:
    address: Union[OneOfIpv6AddrGlobalVariableOptionsDef1, OneOfIpv6AddrGlobalVariableOptionsDef2]
    remote_as: Union[OneOfAsNumOptionsDef1, OneOfAsNumOptionsDef2] = _field(
        metadata={"alias": "remoteAs"}
    )
    # Set IPv6 BGP address family
    address_family: Optional[List[BgpAddressFamily]] = _field(
        default=None, metadata={"alias": "addressFamily"}
    )
    as_number: Optional[
        Union[
            OneOfNeighborAsNumberOptionsDef1,
            OneOfNeighborAsNumberOptionsDef2,
            OneOfNeighborAsNumberOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "asNumber"})
    as_override: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "asOverride"})
    description: Optional[
        Union[
            OneOfNeighborDescriptionOptionsDef1,
            OneOfNeighborDescriptionOptionsDef2,
            OneOfNeighborDescriptionOptionsDef3,
        ]
    ] = _field(default=None)
    ebgp_multihop: Optional[
        Union[
            OneOfNeighborEbgpMultihopOptionsDef1,
            OneOfNeighborEbgpMultihopOptionsDef2,
            OneOfNeighborEbgpMultihopOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ebgpMultihop"})
    fall_over_bfd: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "fallOverBfd"})
    holdtime: Optional[
        Union[OneOfHoldtimeOptionsDef1, OneOfHoldtimeOptionsDef2, OneOfHoldtimeOptionsDef3]
    ] = _field(default=None)
    if_name: Optional[
        Union[
            OneOfInterfaceNameOptionsDef1,
            OneOfInterfaceNameOptionsDef2,
            OneOfInterfaceNameOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ifName"})
    keepalive: Optional[
        Union[OneOfKeepaliveOptionsDef1, OneOfKeepaliveOptionsDef2, OneOfKeepaliveOptionsDef3]
    ] = _field(default=None)
    local_as: Optional[
        Union[OneOfLocalAsOptionsDef1, OneOfLocalAsOptionsDef2, OneOfLocalAsOptionsDef3]
    ] = _field(default=None, metadata={"alias": "localAs"})
    next_hop_self: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "nextHopSelf"})
    password: Optional[
        Union[
            OneOfNeighborPasswordOptionsDef1,
            OneOfNeighborPasswordOptionsDef2,
            OneOfNeighborPasswordOptionsDef3,
        ]
    ] = _field(default=None)
    peer_group: Optional[OneOfNeighborPeerGroupNameOptionsDef] = _field(
        default=None, metadata={"alias": "peerGroup"}
    )
    route_reflect_client: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "routeReflectClient"})
    send_community: Optional[
        Union[
            OneOfOnBooleanDefaultTrueOptionsDef1,
            OneOfOnBooleanDefaultTrueOptionsDef2,
            OneOfOnBooleanDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sendCommunity"})
    send_ext_community: Optional[
        Union[
            OneOfOnBooleanDefaultTrueOptionsDef1,
            OneOfOnBooleanDefaultTrueOptionsDef2,
            OneOfOnBooleanDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sendExtCommunity"})
    shutdown: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class RoutingBgpAddressFamily:
    family_type: WanIpv6NeighborAfTypeDef = _field(metadata={"alias": "familyType"})
    in_route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "inRoutePolicy"})
    max_prefix_config: Optional[
        Union[NeighborMaxPrefixConfigDef1, NeighborMaxPrefixConfigDef2, NeighborMaxPrefixConfigDef3]
    ] = _field(default=None, metadata={"alias": "maxPrefixConfig"})
    out_route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "outRoutePolicy"})


@dataclass
class Ipv6Neighbor2:
    peer_group: OneOfNeighborPeerGroupNameOptionsDef = _field(metadata={"alias": "peerGroup"})
    remote_as: Union[OneOfAsNumOptionsDef1, OneOfAsNumOptionsDef2] = _field(
        metadata={"alias": "remoteAs"}
    )
    address: Optional[
        Union[OneOfIpv6AddrGlobalVariableOptionsDef1, OneOfIpv6AddrGlobalVariableOptionsDef2]
    ] = _field(default=None)
    # Set IPv6 BGP address family
    address_family: Optional[List[RoutingBgpAddressFamily]] = _field(
        default=None, metadata={"alias": "addressFamily"}
    )
    as_number: Optional[
        Union[
            OneOfNeighborAsNumberOptionsDef1,
            OneOfNeighborAsNumberOptionsDef2,
            OneOfNeighborAsNumberOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "asNumber"})
    as_override: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "asOverride"})
    description: Optional[
        Union[
            OneOfNeighborDescriptionOptionsDef1,
            OneOfNeighborDescriptionOptionsDef2,
            OneOfNeighborDescriptionOptionsDef3,
        ]
    ] = _field(default=None)
    ebgp_multihop: Optional[
        Union[
            OneOfNeighborEbgpMultihopOptionsDef1,
            OneOfNeighborEbgpMultihopOptionsDef2,
            OneOfNeighborEbgpMultihopOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ebgpMultihop"})
    fall_over_bfd: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "fallOverBfd"})
    holdtime: Optional[
        Union[OneOfHoldtimeOptionsDef1, OneOfHoldtimeOptionsDef2, OneOfHoldtimeOptionsDef3]
    ] = _field(default=None)
    if_name: Optional[
        Union[
            OneOfInterfaceNameOptionsDef1,
            OneOfInterfaceNameOptionsDef2,
            OneOfInterfaceNameOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ifName"})
    keepalive: Optional[
        Union[OneOfKeepaliveOptionsDef1, OneOfKeepaliveOptionsDef2, OneOfKeepaliveOptionsDef3]
    ] = _field(default=None)
    local_as: Optional[
        Union[OneOfLocalAsOptionsDef1, OneOfLocalAsOptionsDef2, OneOfLocalAsOptionsDef3]
    ] = _field(default=None, metadata={"alias": "localAs"})
    next_hop_self: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "nextHopSelf"})
    password: Optional[
        Union[
            OneOfNeighborPasswordOptionsDef1,
            OneOfNeighborPasswordOptionsDef2,
            OneOfNeighborPasswordOptionsDef3,
        ]
    ] = _field(default=None)
    route_reflect_client: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "routeReflectClient"})
    send_community: Optional[
        Union[
            OneOfOnBooleanDefaultTrueOptionsDef1,
            OneOfOnBooleanDefaultTrueOptionsDef2,
            OneOfOnBooleanDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sendCommunity"})
    send_ext_community: Optional[
        Union[
            OneOfOnBooleanDefaultTrueOptionsDef1,
            OneOfOnBooleanDefaultTrueOptionsDef2,
            OneOfOnBooleanDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sendExtCommunity"})
    shutdown: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class AggregateAddress:
    prefix: Ipv4AddressAndMaskDef
    as_set: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "asSet"})
    summary_only: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "summaryOnly"})


@dataclass
class Network:
    prefix: Ipv4AddressAndMaskDef


@dataclass
class OneOfAddressFamilyPathsOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfAddressFamilyPathsOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAddressFamilyPathsOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfIpv4AddressFamilyRedistributeProtocolOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Ipv4AddressFamilyRedistributeProtocolDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfIpv4AddressFamilyRedistributeProtocolOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfMetricOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfMetricOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfMetricOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfOspfMatchRouteOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[OspfMatchRouteListDef]  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfOspfMatchRouteOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfOspfMatchRouteOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class Redistribute:
    protocol: Union[
        OneOfIpv4AddressFamilyRedistributeProtocolOptionsDef1,
        OneOfIpv4AddressFamilyRedistributeProtocolOptionsDef2,
    ]
    metric: Optional[
        Union[OneOfMetricOptionsDef1, OneOfMetricOptionsDef2, OneOfMetricOptionsDef3]
    ] = _field(default=None)
    ospf_match_route: Optional[
        Union[
            OneOfOspfMatchRouteOptionsDef1,
            OneOfOspfMatchRouteOptionsDef2,
            OneOfOspfMatchRouteOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ospfMatchRoute"})
    route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "routePolicy"})


@dataclass
class GlobalVrfRoutingBgpAddressFamily:
    """
    Set IPv4 unicast BGP address family
    """

    # Aggregate prefixes in specific range
    aggregate_address: Optional[List[AggregateAddress]] = _field(
        default=None, metadata={"alias": "aggregateAddress"}
    )
    filter: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)
    name: Optional[Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]] = (
        _field(default=None)
    )
    # Configure the networks for BGP to advertise
    network: Optional[List[Network]] = _field(default=None)
    originate: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)
    paths: Optional[
        Union[
            OneOfAddressFamilyPathsOptionsDef1,
            OneOfAddressFamilyPathsOptionsDef2,
            OneOfAddressFamilyPathsOptionsDef3,
        ]
    ] = _field(default=None)
    # Redistribute routes into BGP
    redistribute: Optional[List[Redistribute]] = _field(default=None)


@dataclass
class OneOfIpv6PrefixOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfIpv6PrefixOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class Ipv6AggregateAddress:
    prefix: Union[OneOfIpv6PrefixOptionsDef1, OneOfIpv6PrefixOptionsDef2]
    as_set: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "asSet"})
    summary_only: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "summaryOnly"})


@dataclass
class Ipv6Network:
    prefix: Union[OneOfIpv6PrefixOptionsDef1, OneOfIpv6PrefixOptionsDef2]


@dataclass
class OneOfIpv6AddressFamilyRedistributeProtocolOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Ipv6AddressFamilyRedistributeProtocolDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfIpv6AddressFamilyRedistributeProtocolOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class BgpRedistribute:
    protocol: Union[
        OneOfIpv6AddressFamilyRedistributeProtocolOptionsDef1,
        OneOfIpv6AddressFamilyRedistributeProtocolOptionsDef2,
    ]
    metric: Optional[
        Union[OneOfMetricOptionsDef1, OneOfMetricOptionsDef2, OneOfMetricOptionsDef3]
    ] = _field(default=None)
    ospf_match_route: Optional[
        Union[
            OneOfOspfMatchRouteOptionsDef1,
            OneOfOspfMatchRouteOptionsDef2,
            OneOfOspfMatchRouteOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ospfMatchRoute"})
    route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "routePolicy"})


@dataclass
class Ipv6AddressFamily:
    """
    Set BGP address family
    """

    filter: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)
    # IPv6 Aggregate prefixes in specific range
    ipv6_aggregate_address: Optional[List[Ipv6AggregateAddress]] = _field(
        default=None, metadata={"alias": "ipv6AggregateAddress"}
    )
    # Configure the networks for BGP to advertise
    ipv6_network: Optional[List[Ipv6Network]] = _field(
        default=None, metadata={"alias": "ipv6Network"}
    )
    name: Optional[Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]] = (
        _field(default=None)
    )
    originate: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)
    paths: Optional[
        Union[
            OneOfAddressFamilyPathsOptionsDef1,
            OneOfAddressFamilyPathsOptionsDef2,
            OneOfAddressFamilyPathsOptionsDef3,
        ]
    ] = _field(default=None)
    # Redistribute routes into BGP
    redistribute: Optional[List[BgpRedistribute]] = _field(default=None)


@dataclass
class BgpData:
    as_num: Union[OneOfAsNumOptionsDef1, OneOfAsNumOptionsDef2] = _field(
        metadata={"alias": "asNum"}
    )
    # Set IPv4 unicast BGP address family
    address_family: Optional[GlobalVrfRoutingBgpAddressFamily] = _field(
        default=None, metadata={"alias": "addressFamily"}
    )
    always_compare: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "alwaysCompare"})
    compare_router_id: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "compareRouterId"})
    deterministic: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)
    # BGP dynamic neighbor configuration
    dynamic_neighbor: Optional[Union[DynamicNeighbor1, DynamicNeighbor2, DynamicNeighbor3]] = (
        _field(default=None, metadata={"alias": "dynamicNeighbor"})
    )
    external: Optional[
        Union[OneOfExternalOptionsDef1, OneOfExternalOptionsDef2, OneOfExternalOptionsDef3]
    ] = _field(default=None)
    holdtime: Optional[
        Union[OneOfHoldtimeOptionsDef1, OneOfHoldtimeOptionsDef2, OneOfHoldtimeOptionsDef3]
    ] = _field(default=None)
    internal: Optional[
        Union[OneOfInternalOptionsDef1, OneOfInternalOptionsDef2, OneOfInternalOptionsDef3]
    ] = _field(default=None)
    # Set BGP address family
    ipv6_address_family: Optional[Ipv6AddressFamily] = _field(
        default=None, metadata={"alias": "ipv6AddressFamily"}
    )
    # Set BGP IPv6 neighbors
    ipv6_neighbor: Optional[List[Union[Ipv6Neighbor1, Ipv6Neighbor2]]] = _field(
        default=None, metadata={"alias": "ipv6Neighbor"}
    )
    keepalive: Optional[
        Union[OneOfKeepaliveOptionsDef1, OneOfKeepaliveOptionsDef2, OneOfKeepaliveOptionsDef3]
    ] = _field(default=None)
    local: Optional[Union[OneOfLocalOptionsDef1, OneOfLocalOptionsDef2, OneOfLocalOptionsDef3]] = (
        _field(default=None)
    )
    missing_as_worst: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "missingAsWorst"})
    multipath_relax: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "multipathRelax"})
    # Set BGP IPv4 neighbors
    neighbor: Optional[List[Union[Neighbor1, Neighbor2]]] = _field(default=None)
    router_id: Optional[
        Union[OneOfRouterIdOptionsDef1, OneOfRouterIdOptionsDef2, OneOfRouterIdOptionsDef3]
    ] = _field(default=None, metadata={"alias": "routerId"})


@dataclass
class Payload:
    """
    SD-Routing BGP for global VRF feature schema
    """

    data: BgpData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class Data:
    # User who last created this.
    created_by: Optional[str] = _field(default=None, metadata={"alias": "createdBy"})
    # Timestamp of creation
    created_on: Optional[int] = _field(default=None, metadata={"alias": "createdOn"})
    # User who last updated this.
    last_updated_by: Optional[str] = _field(default=None, metadata={"alias": "lastUpdatedBy"})
    # Timestamp of last update
    last_updated_on: Optional[int] = _field(default=None, metadata={"alias": "lastUpdatedOn"})
    parcel_id: Optional[str] = _field(default=None, metadata={"alias": "parcelId"})
    parcel_type: Optional[str] = _field(default=None, metadata={"alias": "parcelType"})
    # SD-Routing BGP for global VRF feature schema
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdRoutingTransportGlobalVrfRoutingBgpPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateSdroutingTransportGlobalVrfBgpFeaturePostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class TransportGlobalVrfRoutingBgpAddressFamily:
    """
    Set IPv4 unicast BGP address family
    """

    # Aggregate prefixes in specific range
    aggregate_address: Optional[List[AggregateAddress]] = _field(
        default=None, metadata={"alias": "aggregateAddress"}
    )
    filter: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)
    name: Optional[Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]] = (
        _field(default=None)
    )
    # Configure the networks for BGP to advertise
    network: Optional[List[Network]] = _field(default=None)
    originate: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)
    paths: Optional[
        Union[
            OneOfAddressFamilyPathsOptionsDef1,
            OneOfAddressFamilyPathsOptionsDef2,
            OneOfAddressFamilyPathsOptionsDef3,
        ]
    ] = _field(default=None)
    # Redistribute routes into BGP
    redistribute: Optional[List[Redistribute]] = _field(default=None)


@dataclass
class RoutingBgpData:
    as_num: Union[OneOfAsNumOptionsDef1, OneOfAsNumOptionsDef2] = _field(
        metadata={"alias": "asNum"}
    )
    # Set IPv4 unicast BGP address family
    address_family: Optional[TransportGlobalVrfRoutingBgpAddressFamily] = _field(
        default=None, metadata={"alias": "addressFamily"}
    )
    always_compare: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "alwaysCompare"})
    compare_router_id: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "compareRouterId"})
    deterministic: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)
    # BGP dynamic neighbor configuration
    dynamic_neighbor: Optional[Union[DynamicNeighbor1, DynamicNeighbor2, DynamicNeighbor3]] = (
        _field(default=None, metadata={"alias": "dynamicNeighbor"})
    )
    external: Optional[
        Union[OneOfExternalOptionsDef1, OneOfExternalOptionsDef2, OneOfExternalOptionsDef3]
    ] = _field(default=None)
    holdtime: Optional[
        Union[OneOfHoldtimeOptionsDef1, OneOfHoldtimeOptionsDef2, OneOfHoldtimeOptionsDef3]
    ] = _field(default=None)
    internal: Optional[
        Union[OneOfInternalOptionsDef1, OneOfInternalOptionsDef2, OneOfInternalOptionsDef3]
    ] = _field(default=None)
    # Set BGP address family
    ipv6_address_family: Optional[Ipv6AddressFamily] = _field(
        default=None, metadata={"alias": "ipv6AddressFamily"}
    )
    # Set BGP IPv6 neighbors
    ipv6_neighbor: Optional[List[Union[Ipv6Neighbor1, Ipv6Neighbor2]]] = _field(
        default=None, metadata={"alias": "ipv6Neighbor"}
    )
    keepalive: Optional[
        Union[OneOfKeepaliveOptionsDef1, OneOfKeepaliveOptionsDef2, OneOfKeepaliveOptionsDef3]
    ] = _field(default=None)
    local: Optional[Union[OneOfLocalOptionsDef1, OneOfLocalOptionsDef2, OneOfLocalOptionsDef3]] = (
        _field(default=None)
    )
    missing_as_worst: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "missingAsWorst"})
    multipath_relax: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "multipathRelax"})
    # Set BGP IPv4 neighbors
    neighbor: Optional[List[Union[Neighbor1, Neighbor2]]] = _field(default=None)
    router_id: Optional[
        Union[OneOfRouterIdOptionsDef1, OneOfRouterIdOptionsDef2, OneOfRouterIdOptionsDef3]
    ] = _field(default=None, metadata={"alias": "routerId"})


@dataclass
class CreateSdroutingTransportGlobalVrfBgpFeaturePostRequest:
    """
    SD-Routing BGP for global VRF feature schema
    """

    data: RoutingBgpData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class GetSingleSdRoutingTransportGlobalVrfRoutingBgpPayload:
    # User who last created this.
    created_by: Optional[str] = _field(default=None, metadata={"alias": "createdBy"})
    # Timestamp of creation
    created_on: Optional[int] = _field(default=None, metadata={"alias": "createdOn"})
    # User who last updated this.
    last_updated_by: Optional[str] = _field(default=None, metadata={"alias": "lastUpdatedBy"})
    # Timestamp of last update
    last_updated_on: Optional[int] = _field(default=None, metadata={"alias": "lastUpdatedOn"})
    parcel_id: Optional[str] = _field(default=None, metadata={"alias": "parcelId"})
    parcel_type: Optional[str] = _field(default=None, metadata={"alias": "parcelType"})
    # SD-Routing BGP for global VRF feature schema
    payload: Optional[Payload] = _field(default=None)


@dataclass
class EditSdroutingTransportGlobalVrfBgpFeaturePutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SdRoutingTransportGlobalVrfRoutingBgpAddressFamily:
    """
    Set IPv4 unicast BGP address family
    """

    # Aggregate prefixes in specific range
    aggregate_address: Optional[List[AggregateAddress]] = _field(
        default=None, metadata={"alias": "aggregateAddress"}
    )
    filter: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)
    name: Optional[Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]] = (
        _field(default=None)
    )
    # Configure the networks for BGP to advertise
    network: Optional[List[Network]] = _field(default=None)
    originate: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)
    paths: Optional[
        Union[
            OneOfAddressFamilyPathsOptionsDef1,
            OneOfAddressFamilyPathsOptionsDef2,
            OneOfAddressFamilyPathsOptionsDef3,
        ]
    ] = _field(default=None)
    # Redistribute routes into BGP
    redistribute: Optional[List[Redistribute]] = _field(default=None)


@dataclass
class GlobalVrfRoutingBgpData:
    as_num: Union[OneOfAsNumOptionsDef1, OneOfAsNumOptionsDef2] = _field(
        metadata={"alias": "asNum"}
    )
    # Set IPv4 unicast BGP address family
    address_family: Optional[SdRoutingTransportGlobalVrfRoutingBgpAddressFamily] = _field(
        default=None, metadata={"alias": "addressFamily"}
    )
    always_compare: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "alwaysCompare"})
    compare_router_id: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "compareRouterId"})
    deterministic: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)
    # BGP dynamic neighbor configuration
    dynamic_neighbor: Optional[Union[DynamicNeighbor1, DynamicNeighbor2, DynamicNeighbor3]] = (
        _field(default=None, metadata={"alias": "dynamicNeighbor"})
    )
    external: Optional[
        Union[OneOfExternalOptionsDef1, OneOfExternalOptionsDef2, OneOfExternalOptionsDef3]
    ] = _field(default=None)
    holdtime: Optional[
        Union[OneOfHoldtimeOptionsDef1, OneOfHoldtimeOptionsDef2, OneOfHoldtimeOptionsDef3]
    ] = _field(default=None)
    internal: Optional[
        Union[OneOfInternalOptionsDef1, OneOfInternalOptionsDef2, OneOfInternalOptionsDef3]
    ] = _field(default=None)
    # Set BGP address family
    ipv6_address_family: Optional[Ipv6AddressFamily] = _field(
        default=None, metadata={"alias": "ipv6AddressFamily"}
    )
    # Set BGP IPv6 neighbors
    ipv6_neighbor: Optional[List[Union[Ipv6Neighbor1, Ipv6Neighbor2]]] = _field(
        default=None, metadata={"alias": "ipv6Neighbor"}
    )
    keepalive: Optional[
        Union[OneOfKeepaliveOptionsDef1, OneOfKeepaliveOptionsDef2, OneOfKeepaliveOptionsDef3]
    ] = _field(default=None)
    local: Optional[Union[OneOfLocalOptionsDef1, OneOfLocalOptionsDef2, OneOfLocalOptionsDef3]] = (
        _field(default=None)
    )
    missing_as_worst: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "missingAsWorst"})
    multipath_relax: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "multipathRelax"})
    # Set BGP IPv4 neighbors
    neighbor: Optional[List[Union[Neighbor1, Neighbor2]]] = _field(default=None)
    router_id: Optional[
        Union[OneOfRouterIdOptionsDef1, OneOfRouterIdOptionsDef2, OneOfRouterIdOptionsDef3]
    ] = _field(default=None, metadata={"alias": "routerId"})


@dataclass
class EditSdroutingTransportGlobalVrfBgpFeaturePutRequest:
    """
    SD-Routing BGP for global VRF feature schema
    """

    data: GlobalVrfRoutingBgpData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class BgpOneOfAsNumOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Union[int, str]


@dataclass
class BgpOneOfExternalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class BgpOneOfExternalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class BgpOneOfInternalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class BgpOneOfInternalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class BgpOneOfLocalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class BgpOneOfLocalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class BgpOneOfKeepaliveOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class BgpOneOfKeepaliveOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class BgpOneOfHoldtimeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class BgpOneOfHoldtimeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class BgpOneOfMaxListenPrefixNumOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class BgpOneOfMaxListenPrefixNumOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class BgpOneOfNeighborPeerGroupNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class BgpIpv4PeerGroup:
    peer_group_name: BgpOneOfNeighborPeerGroupNameOptionsDef = _field(
        metadata={"alias": "peerGroupName"}
    )
    # Peer Group IPv4 subnet range
    range: List[Ipv4AddressAndMaskDef]
    # Peer Group IPv4 Address list
    ipv4_address: Optional[List[Ipv4Address]] = _field(
        default=None, metadata={"alias": "ipv4Address"}
    )


@dataclass
class RoutingBgpOneOfNeighborPeerGroupNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class BgpIpv6PeerGroup:
    peer_group_name: RoutingBgpOneOfNeighborPeerGroupNameOptionsDef = _field(
        metadata={"alias": "peerGroupName"}
    )
    # Peer Group IPv6 prefix range
    range: List[Range]
    # Peer Group IPv6 Address list
    ipv6_address: Optional[List[Ipv6Address]] = _field(
        default=None, metadata={"alias": "ipv6Address"}
    )


@dataclass
class BgpDynamicNeighbor1:
    # IPv4 Peer groups
    ipv4_peer_group: List[BgpIpv4PeerGroup] = _field(metadata={"alias": "ipv4PeerGroup"})
    max_listen_prefix_limit: Union[
        BgpOneOfMaxListenPrefixNumOptionsDef1,
        OneOfMaxListenPrefixNumOptionsDef2,
        BgpOneOfMaxListenPrefixNumOptionsDef3,
    ] = _field(metadata={"alias": "maxListenPrefixLimit"})
    # IPv6 Peer groups
    ipv6_peer_group: Optional[List[BgpIpv6PeerGroup]] = _field(
        default=None, metadata={"alias": "ipv6PeerGroup"}
    )


@dataclass
class RoutingBgpOneOfMaxListenPrefixNumOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class RoutingBgpOneOfMaxListenPrefixNumOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class GlobalVrfRoutingBgpOneOfNeighborPeerGroupNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class RoutingBgpIpv4PeerGroup:
    peer_group_name: GlobalVrfRoutingBgpOneOfNeighborPeerGroupNameOptionsDef = _field(
        metadata={"alias": "peerGroupName"}
    )
    # Peer Group IPv4 subnet range
    range: List[Ipv4AddressAndMaskDef]
    # Peer Group IPv4 Address list
    ipv4_address: Optional[List[Ipv4Address]] = _field(
        default=None, metadata={"alias": "ipv4Address"}
    )


@dataclass
class TransportGlobalVrfRoutingBgpOneOfNeighborPeerGroupNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class RoutingBgpIpv6PeerGroup:
    peer_group_name: TransportGlobalVrfRoutingBgpOneOfNeighborPeerGroupNameOptionsDef = _field(
        metadata={"alias": "peerGroupName"}
    )
    # Peer Group IPv6 prefix range
    range: List[Range]
    # Peer Group IPv6 Address list
    ipv6_address: Optional[List[Ipv6Address]] = _field(
        default=None, metadata={"alias": "ipv6Address"}
    )


@dataclass
class BgpDynamicNeighbor2:
    # IPv6 Peer groups
    ipv6_peer_group: List[RoutingBgpIpv6PeerGroup] = _field(metadata={"alias": "ipv6PeerGroup"})
    max_listen_prefix_limit: Union[
        RoutingBgpOneOfMaxListenPrefixNumOptionsDef1,
        OneOfMaxListenPrefixNumOptionsDef2,
        RoutingBgpOneOfMaxListenPrefixNumOptionsDef3,
    ] = _field(metadata={"alias": "maxListenPrefixLimit"})
    # IPv4 Peer groups
    ipv4_peer_group: Optional[List[RoutingBgpIpv4PeerGroup]] = _field(
        default=None, metadata={"alias": "ipv4PeerGroup"}
    )


@dataclass
class GlobalVrfRoutingBgpOneOfMaxListenPrefixNumOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class GlobalVrfRoutingBgpOneOfMaxListenPrefixNumOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborPeerGroupNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class GlobalVrfRoutingBgpIpv4PeerGroup:
    peer_group_name: SdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborPeerGroupNameOptionsDef = (
        _field(metadata={"alias": "peerGroupName"})
    )
    # Peer Group IPv4 subnet range
    range: List[Ipv4AddressAndMaskDef]
    # Peer Group IPv4 Address list
    ipv4_address: Optional[List[Ipv4Address]] = _field(
        default=None, metadata={"alias": "ipv4Address"}
    )


@dataclass
class FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborPeerGroupNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class GlobalVrfRoutingBgpIpv6PeerGroup:
    peer_group_name: FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborPeerGroupNameOptionsDef = _field(
        metadata={"alias": "peerGroupName"}
    )
    # Peer Group IPv6 prefix range
    range: List[Range]
    # Peer Group IPv6 Address list
    ipv6_address: Optional[List[Ipv6Address]] = _field(
        default=None, metadata={"alias": "ipv6Address"}
    )


@dataclass
class BgpDynamicNeighbor3:
    # IPv4 Peer groups
    ipv4_peer_group: List[GlobalVrfRoutingBgpIpv4PeerGroup] = _field(
        metadata={"alias": "ipv4PeerGroup"}
    )
    # IPv6 Peer groups
    ipv6_peer_group: List[GlobalVrfRoutingBgpIpv6PeerGroup] = _field(
        metadata={"alias": "ipv6PeerGroup"}
    )
    max_listen_prefix_limit: Union[
        GlobalVrfRoutingBgpOneOfMaxListenPrefixNumOptionsDef1,
        OneOfMaxListenPrefixNumOptionsDef2,
        GlobalVrfRoutingBgpOneOfMaxListenPrefixNumOptionsDef3,
    ] = _field(metadata={"alias": "maxListenPrefixLimit"})


@dataclass
class V1FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborPeerGroupNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class BgpOneOfNeighborDescriptionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class RoutingBgpOneOfAsNumOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Union[int, str]


@dataclass
class BgpOneOfLocalAsOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Union[int, str]


@dataclass
class RoutingBgpOneOfKeepaliveOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class RoutingBgpOneOfKeepaliveOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class RoutingBgpOneOfHoldtimeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class RoutingBgpOneOfHoldtimeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class BgpOneOfNeighborEbgpMultihopOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class BgpOneOfNeighborEbgpMultihopOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class BgpOneOfNeighborPasswordOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class BgpOneOfNeighborAsNumberOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class LanIpv4NeighborAfTypeDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Value


@dataclass
class GlobalVrfRoutingBgpPolicyType:
    """
    Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is restarting device.
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class BgpOneOfNeighborMaxPrefixNumOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class BgpOneOfNeighborAddressFamilyThresholdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class BgpOneOfNeighborAddressFamilyThresholdOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class BgpOneOfNeighborMaxPrefixExceedRestartTimeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class BgpNeighborMaxPrefixConfigDef2:
    # Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is restarting device.
    policy_type: GlobalVrfRoutingBgpPolicyType = _field(metadata={"alias": "policyType"})
    prefix_num: Union[
        BgpOneOfNeighborMaxPrefixNumOptionsDef1, OneOfNeighborMaxPrefixNumOptionsDef2
    ] = _field(metadata={"alias": "prefixNum"})
    restart_interval: Union[
        BgpOneOfNeighborMaxPrefixExceedRestartTimeOptionsDef1,
        OneOfNeighborMaxPrefixExceedRestartTimeOptionsDef2,
    ] = _field(metadata={"alias": "restartInterval"})
    threshold: Union[
        BgpOneOfNeighborAddressFamilyThresholdOptionsDef1,
        OneOfNeighborAddressFamilyThresholdOptionsDef2,
        BgpOneOfNeighborAddressFamilyThresholdOptionsDef3,
    ]


@dataclass
class TransportGlobalVrfRoutingBgpPolicyType:
    """
    Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is warning-only or disable-peer.
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: GlobalVrfRoutingBgpValue  # pytype: disable=annotation-type-mismatch


@dataclass
class RoutingBgpOneOfNeighborMaxPrefixNumOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class RoutingBgpOneOfNeighborAddressFamilyThresholdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class RoutingBgpOneOfNeighborAddressFamilyThresholdOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class BgpNeighborMaxPrefixConfigDef3:
    # Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is warning-only or disable-peer.
    policy_type: TransportGlobalVrfRoutingBgpPolicyType = _field(metadata={"alias": "policyType"})
    prefix_num: Union[
        RoutingBgpOneOfNeighborMaxPrefixNumOptionsDef1, OneOfNeighborMaxPrefixNumOptionsDef2
    ] = _field(metadata={"alias": "prefixNum"})
    threshold: Union[
        RoutingBgpOneOfNeighborAddressFamilyThresholdOptionsDef1,
        OneOfNeighborAddressFamilyThresholdOptionsDef2,
        RoutingBgpOneOfNeighborAddressFamilyThresholdOptionsDef3,
    ]


@dataclass
class FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpAddressFamily:
    family_type: LanIpv4NeighborAfTypeDef = _field(metadata={"alias": "familyType"})
    in_route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "inRoutePolicy"})
    max_prefix_config: Optional[
        Union[
            NeighborMaxPrefixConfigDef1,
            BgpNeighborMaxPrefixConfigDef2,
            BgpNeighborMaxPrefixConfigDef3,
        ]
    ] = _field(default=None, metadata={"alias": "maxPrefixConfig"})
    out_route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "outRoutePolicy"})


@dataclass
class BgpNeighbor1:
    address: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2]
    remote_as: Union[RoutingBgpOneOfAsNumOptionsDef1, OneOfAsNumOptionsDef2] = _field(
        metadata={"alias": "remoteAs"}
    )
    # Set BGP address family
    address_family: Optional[
        List[FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpAddressFamily]
    ] = _field(default=None, metadata={"alias": "addressFamily"})
    as_number: Optional[
        Union[
            BgpOneOfNeighborAsNumberOptionsDef1,
            OneOfNeighborAsNumberOptionsDef2,
            OneOfNeighborAsNumberOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "asNumber"})
    as_override: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "asOverride"})
    description: Optional[
        Union[
            BgpOneOfNeighborDescriptionOptionsDef1,
            OneOfNeighborDescriptionOptionsDef2,
            OneOfNeighborDescriptionOptionsDef3,
        ]
    ] = _field(default=None)
    ebgp_multihop: Optional[
        Union[
            BgpOneOfNeighborEbgpMultihopOptionsDef1,
            OneOfNeighborEbgpMultihopOptionsDef2,
            BgpOneOfNeighborEbgpMultihopOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ebgpMultihop"})
    fall_over_bfd: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "fallOverBfd"})
    holdtime: Optional[
        Union[
            RoutingBgpOneOfHoldtimeOptionsDef1,
            OneOfHoldtimeOptionsDef2,
            RoutingBgpOneOfHoldtimeOptionsDef3,
        ]
    ] = _field(default=None)
    if_name: Optional[
        Union[
            OneOfInterfaceNameOptionsDef1,
            OneOfInterfaceNameOptionsDef2,
            OneOfInterfaceNameOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ifName"})
    keepalive: Optional[
        Union[
            RoutingBgpOneOfKeepaliveOptionsDef1,
            OneOfKeepaliveOptionsDef2,
            RoutingBgpOneOfKeepaliveOptionsDef3,
        ]
    ] = _field(default=None)
    local_as: Optional[
        Union[BgpOneOfLocalAsOptionsDef1, OneOfLocalAsOptionsDef2, OneOfLocalAsOptionsDef3]
    ] = _field(default=None, metadata={"alias": "localAs"})
    next_hop_self: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "nextHopSelf"})
    password: Optional[
        Union[
            BgpOneOfNeighborPasswordOptionsDef1,
            OneOfNeighborPasswordOptionsDef2,
            OneOfNeighborPasswordOptionsDef3,
        ]
    ] = _field(default=None)
    peer_group: Optional[
        V1FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborPeerGroupNameOptionsDef
    ] = _field(default=None, metadata={"alias": "peerGroup"})
    route_reflect_client: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "routeReflectClient"})
    send_community: Optional[
        Union[
            OneOfOnBooleanDefaultTrueOptionsDef1,
            OneOfOnBooleanDefaultTrueOptionsDef2,
            OneOfOnBooleanDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sendCommunity"})
    send_ext_community: Optional[
        Union[
            OneOfOnBooleanDefaultTrueOptionsDef1,
            OneOfOnBooleanDefaultTrueOptionsDef2,
            OneOfOnBooleanDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sendExtCommunity"})
    shutdown: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class OneOfNeighborPeerGroupNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class RoutingBgpOneOfNeighborDescriptionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class GlobalVrfRoutingBgpOneOfAsNumOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Union[int, str]


@dataclass
class RoutingBgpOneOfLocalAsOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Union[int, str]


@dataclass
class GlobalVrfRoutingBgpOneOfKeepaliveOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class GlobalVrfRoutingBgpOneOfKeepaliveOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class GlobalVrfRoutingBgpOneOfHoldtimeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class GlobalVrfRoutingBgpOneOfHoldtimeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class RoutingBgpOneOfNeighborEbgpMultihopOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class RoutingBgpOneOfNeighborEbgpMultihopOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class RoutingBgpOneOfNeighborPasswordOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class RoutingBgpOneOfNeighborAsNumberOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SdRoutingTransportGlobalVrfRoutingBgpPolicyType:
    """
    Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is restarting device.
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class GlobalVrfRoutingBgpOneOfNeighborMaxPrefixNumOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class GlobalVrfRoutingBgpOneOfNeighborAddressFamilyThresholdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class GlobalVrfRoutingBgpOneOfNeighborAddressFamilyThresholdOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class RoutingBgpOneOfNeighborMaxPrefixExceedRestartTimeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class RoutingBgpNeighborMaxPrefixConfigDef2:
    # Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is restarting device.
    policy_type: SdRoutingTransportGlobalVrfRoutingBgpPolicyType = _field(
        metadata={"alias": "policyType"}
    )
    prefix_num: Union[
        GlobalVrfRoutingBgpOneOfNeighborMaxPrefixNumOptionsDef1,
        OneOfNeighborMaxPrefixNumOptionsDef2,
    ] = _field(metadata={"alias": "prefixNum"})
    restart_interval: Union[
        RoutingBgpOneOfNeighborMaxPrefixExceedRestartTimeOptionsDef1,
        OneOfNeighborMaxPrefixExceedRestartTimeOptionsDef2,
    ] = _field(metadata={"alias": "restartInterval"})
    threshold: Union[
        GlobalVrfRoutingBgpOneOfNeighborAddressFamilyThresholdOptionsDef1,
        OneOfNeighborAddressFamilyThresholdOptionsDef2,
        GlobalVrfRoutingBgpOneOfNeighborAddressFamilyThresholdOptionsDef3,
    ]


@dataclass
class FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpPolicyType:
    """
    Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is warning-only or disable-peer.
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: TransportGlobalVrfRoutingBgpValue  # pytype: disable=annotation-type-mismatch


@dataclass
class TransportGlobalVrfRoutingBgpOneOfNeighborMaxPrefixNumOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class TransportGlobalVrfRoutingBgpOneOfNeighborAddressFamilyThresholdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class TransportGlobalVrfRoutingBgpOneOfNeighborAddressFamilyThresholdOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class RoutingBgpNeighborMaxPrefixConfigDef3:
    # Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is warning-only or disable-peer.
    policy_type: FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpPolicyType = _field(
        metadata={"alias": "policyType"}
    )
    prefix_num: Union[
        TransportGlobalVrfRoutingBgpOneOfNeighborMaxPrefixNumOptionsDef1,
        OneOfNeighborMaxPrefixNumOptionsDef2,
    ] = _field(metadata={"alias": "prefixNum"})
    threshold: Union[
        TransportGlobalVrfRoutingBgpOneOfNeighborAddressFamilyThresholdOptionsDef1,
        OneOfNeighborAddressFamilyThresholdOptionsDef2,
        TransportGlobalVrfRoutingBgpOneOfNeighborAddressFamilyThresholdOptionsDef3,
    ]


@dataclass
class V1FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpAddressFamily:
    family_type: LanIpv4NeighborAfTypeDef = _field(metadata={"alias": "familyType"})
    in_route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "inRoutePolicy"})
    max_prefix_config: Optional[
        Union[
            NeighborMaxPrefixConfigDef1,
            RoutingBgpNeighborMaxPrefixConfigDef2,
            RoutingBgpNeighborMaxPrefixConfigDef3,
        ]
    ] = _field(default=None, metadata={"alias": "maxPrefixConfig"})
    out_route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "outRoutePolicy"})


@dataclass
class BgpNeighbor2:
    peer_group: OneOfNeighborPeerGroupNameOptionsDef1 = _field(metadata={"alias": "peerGroup"})
    remote_as: Union[GlobalVrfRoutingBgpOneOfAsNumOptionsDef1, OneOfAsNumOptionsDef2] = _field(
        metadata={"alias": "remoteAs"}
    )
    address: Optional[Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2]] = _field(
        default=None
    )
    # Set BGP address family
    address_family: Optional[
        List[V1FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpAddressFamily]
    ] = _field(default=None, metadata={"alias": "addressFamily"})
    as_number: Optional[
        Union[
            RoutingBgpOneOfNeighborAsNumberOptionsDef1,
            OneOfNeighborAsNumberOptionsDef2,
            OneOfNeighborAsNumberOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "asNumber"})
    as_override: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "asOverride"})
    description: Optional[
        Union[
            RoutingBgpOneOfNeighborDescriptionOptionsDef1,
            OneOfNeighborDescriptionOptionsDef2,
            OneOfNeighborDescriptionOptionsDef3,
        ]
    ] = _field(default=None)
    ebgp_multihop: Optional[
        Union[
            RoutingBgpOneOfNeighborEbgpMultihopOptionsDef1,
            OneOfNeighborEbgpMultihopOptionsDef2,
            RoutingBgpOneOfNeighborEbgpMultihopOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ebgpMultihop"})
    fall_over_bfd: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "fallOverBfd"})
    holdtime: Optional[
        Union[
            GlobalVrfRoutingBgpOneOfHoldtimeOptionsDef1,
            OneOfHoldtimeOptionsDef2,
            GlobalVrfRoutingBgpOneOfHoldtimeOptionsDef3,
        ]
    ] = _field(default=None)
    if_name: Optional[
        Union[
            OneOfInterfaceNameOptionsDef1,
            OneOfInterfaceNameOptionsDef2,
            OneOfInterfaceNameOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ifName"})
    keepalive: Optional[
        Union[
            GlobalVrfRoutingBgpOneOfKeepaliveOptionsDef1,
            OneOfKeepaliveOptionsDef2,
            GlobalVrfRoutingBgpOneOfKeepaliveOptionsDef3,
        ]
    ] = _field(default=None)
    local_as: Optional[
        Union[RoutingBgpOneOfLocalAsOptionsDef1, OneOfLocalAsOptionsDef2, OneOfLocalAsOptionsDef3]
    ] = _field(default=None, metadata={"alias": "localAs"})
    next_hop_self: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "nextHopSelf"})
    password: Optional[
        Union[
            RoutingBgpOneOfNeighborPasswordOptionsDef1,
            OneOfNeighborPasswordOptionsDef2,
            OneOfNeighborPasswordOptionsDef3,
        ]
    ] = _field(default=None)
    route_reflect_client: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "routeReflectClient"})
    send_community: Optional[
        Union[
            OneOfOnBooleanDefaultTrueOptionsDef1,
            OneOfOnBooleanDefaultTrueOptionsDef2,
            OneOfOnBooleanDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sendCommunity"})
    send_ext_community: Optional[
        Union[
            OneOfOnBooleanDefaultTrueOptionsDef1,
            OneOfOnBooleanDefaultTrueOptionsDef2,
            OneOfOnBooleanDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sendExtCommunity"})
    shutdown: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class OneOfNeighborPeerGroupNameOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class GlobalVrfRoutingBgpOneOfNeighborDescriptionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class TransportGlobalVrfRoutingBgpOneOfAsNumOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Union[int, str]


@dataclass
class GlobalVrfRoutingBgpOneOfLocalAsOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Union[int, str]


@dataclass
class TransportGlobalVrfRoutingBgpOneOfKeepaliveOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class TransportGlobalVrfRoutingBgpOneOfKeepaliveOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class TransportGlobalVrfRoutingBgpOneOfHoldtimeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class TransportGlobalVrfRoutingBgpOneOfHoldtimeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class GlobalVrfRoutingBgpOneOfNeighborEbgpMultihopOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class GlobalVrfRoutingBgpOneOfNeighborEbgpMultihopOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class GlobalVrfRoutingBgpOneOfNeighborPasswordOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class GlobalVrfRoutingBgpOneOfNeighborAsNumberOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class LanIpv6NeighborAfTypeDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SdRoutingTransportGlobalVrfRoutingBgpValue


@dataclass
class V1FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpPolicyType:
    """
    Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is restarting device.
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class SdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborMaxPrefixNumOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborAddressFamilyThresholdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborAddressFamilyThresholdOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class GlobalVrfRoutingBgpOneOfNeighborMaxPrefixExceedRestartTimeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class GlobalVrfRoutingBgpNeighborMaxPrefixConfigDef2:
    # Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is restarting device.
    policy_type: V1FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpPolicyType = _field(
        metadata={"alias": "policyType"}
    )
    prefix_num: Union[
        SdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborMaxPrefixNumOptionsDef1,
        OneOfNeighborMaxPrefixNumOptionsDef2,
    ] = _field(metadata={"alias": "prefixNum"})
    restart_interval: Union[
        GlobalVrfRoutingBgpOneOfNeighborMaxPrefixExceedRestartTimeOptionsDef1,
        OneOfNeighborMaxPrefixExceedRestartTimeOptionsDef2,
    ] = _field(metadata={"alias": "restartInterval"})
    threshold: Union[
        SdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborAddressFamilyThresholdOptionsDef1,
        OneOfNeighborAddressFamilyThresholdOptionsDef2,
        SdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborAddressFamilyThresholdOptionsDef3,
    ]


@dataclass
class PolicyType1:
    """
    Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is warning-only or disable-peer.
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpValue  # pytype: disable=annotation-type-mismatch


@dataclass
class FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborMaxPrefixNumOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborAddressFamilyThresholdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborAddressFamilyThresholdOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class GlobalVrfRoutingBgpNeighborMaxPrefixConfigDef3:
    # Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is warning-only or disable-peer.
    policy_type: PolicyType1 = _field(metadata={"alias": "policyType"})
    prefix_num: Union[
        FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborMaxPrefixNumOptionsDef1,
        OneOfNeighborMaxPrefixNumOptionsDef2,
    ] = _field(metadata={"alias": "prefixNum"})
    threshold: Union[
        FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborAddressFamilyThresholdOptionsDef1,
        OneOfNeighborAddressFamilyThresholdOptionsDef2,
        FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborAddressFamilyThresholdOptionsDef3,
    ]


@dataclass
class AddressFamily1:
    family_type: LanIpv6NeighborAfTypeDef = _field(metadata={"alias": "familyType"})
    in_route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "inRoutePolicy"})
    max_prefix_config: Optional[
        Union[
            NeighborMaxPrefixConfigDef1,
            GlobalVrfRoutingBgpNeighborMaxPrefixConfigDef2,
            GlobalVrfRoutingBgpNeighborMaxPrefixConfigDef3,
        ]
    ] = _field(default=None, metadata={"alias": "maxPrefixConfig"})
    out_route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "outRoutePolicy"})


@dataclass
class BgpIpv6Neighbor1:
    address: Union[OneOfIpv6AddrGlobalVariableOptionsDef1, OneOfIpv6AddrGlobalVariableOptionsDef2]
    remote_as: Union[TransportGlobalVrfRoutingBgpOneOfAsNumOptionsDef1, OneOfAsNumOptionsDef2] = (
        _field(metadata={"alias": "remoteAs"})
    )
    # Set IPv6 BGP address family
    address_family: Optional[List[AddressFamily1]] = _field(
        default=None, metadata={"alias": "addressFamily"}
    )
    as_number: Optional[
        Union[
            GlobalVrfRoutingBgpOneOfNeighborAsNumberOptionsDef1,
            OneOfNeighborAsNumberOptionsDef2,
            OneOfNeighborAsNumberOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "asNumber"})
    as_override: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "asOverride"})
    description: Optional[
        Union[
            GlobalVrfRoutingBgpOneOfNeighborDescriptionOptionsDef1,
            OneOfNeighborDescriptionOptionsDef2,
            OneOfNeighborDescriptionOptionsDef3,
        ]
    ] = _field(default=None)
    ebgp_multihop: Optional[
        Union[
            GlobalVrfRoutingBgpOneOfNeighborEbgpMultihopOptionsDef1,
            OneOfNeighborEbgpMultihopOptionsDef2,
            GlobalVrfRoutingBgpOneOfNeighborEbgpMultihopOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ebgpMultihop"})
    fall_over_bfd: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "fallOverBfd"})
    holdtime: Optional[
        Union[
            TransportGlobalVrfRoutingBgpOneOfHoldtimeOptionsDef1,
            OneOfHoldtimeOptionsDef2,
            TransportGlobalVrfRoutingBgpOneOfHoldtimeOptionsDef3,
        ]
    ] = _field(default=None)
    if_name: Optional[
        Union[
            OneOfInterfaceNameOptionsDef1,
            OneOfInterfaceNameOptionsDef2,
            OneOfInterfaceNameOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ifName"})
    keepalive: Optional[
        Union[
            TransportGlobalVrfRoutingBgpOneOfKeepaliveOptionsDef1,
            OneOfKeepaliveOptionsDef2,
            TransportGlobalVrfRoutingBgpOneOfKeepaliveOptionsDef3,
        ]
    ] = _field(default=None)
    local_as: Optional[
        Union[
            GlobalVrfRoutingBgpOneOfLocalAsOptionsDef1,
            OneOfLocalAsOptionsDef2,
            OneOfLocalAsOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "localAs"})
    next_hop_self: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "nextHopSelf"})
    password: Optional[
        Union[
            GlobalVrfRoutingBgpOneOfNeighborPasswordOptionsDef1,
            OneOfNeighborPasswordOptionsDef2,
            OneOfNeighborPasswordOptionsDef3,
        ]
    ] = _field(default=None)
    peer_group: Optional[OneOfNeighborPeerGroupNameOptionsDef2] = _field(
        default=None, metadata={"alias": "peerGroup"}
    )
    route_reflect_client: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "routeReflectClient"})
    send_community: Optional[
        Union[
            OneOfOnBooleanDefaultTrueOptionsDef1,
            OneOfOnBooleanDefaultTrueOptionsDef2,
            OneOfOnBooleanDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sendCommunity"})
    send_ext_community: Optional[
        Union[
            OneOfOnBooleanDefaultTrueOptionsDef1,
            OneOfOnBooleanDefaultTrueOptionsDef2,
            OneOfOnBooleanDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sendExtCommunity"})
    shutdown: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class OneOfNeighborPeerGroupNameOptionsDef3:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class TransportGlobalVrfRoutingBgpOneOfNeighborDescriptionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SdRoutingTransportGlobalVrfRoutingBgpOneOfAsNumOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Union[int, str]


@dataclass
class TransportGlobalVrfRoutingBgpOneOfLocalAsOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Union[int, str]


@dataclass
class SdRoutingTransportGlobalVrfRoutingBgpOneOfKeepaliveOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SdRoutingTransportGlobalVrfRoutingBgpOneOfKeepaliveOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SdRoutingTransportGlobalVrfRoutingBgpOneOfHoldtimeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SdRoutingTransportGlobalVrfRoutingBgpOneOfHoldtimeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class TransportGlobalVrfRoutingBgpOneOfNeighborEbgpMultihopOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class TransportGlobalVrfRoutingBgpOneOfNeighborEbgpMultihopOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class TransportGlobalVrfRoutingBgpOneOfNeighborPasswordOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class TransportGlobalVrfRoutingBgpOneOfNeighborAsNumberOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class PolicyType2:
    """
    Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is restarting device.
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class V1FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborMaxPrefixNumOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class V1FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborAddressFamilyThresholdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class V1FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborAddressFamilyThresholdOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class TransportGlobalVrfRoutingBgpOneOfNeighborMaxPrefixExceedRestartTimeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class TransportGlobalVrfRoutingBgpNeighborMaxPrefixConfigDef2:
    # Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is restarting device.
    policy_type: PolicyType2 = _field(metadata={"alias": "policyType"})
    prefix_num: Union[
        V1FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborMaxPrefixNumOptionsDef1,
        OneOfNeighborMaxPrefixNumOptionsDef2,
    ] = _field(metadata={"alias": "prefixNum"})
    restart_interval: Union[
        TransportGlobalVrfRoutingBgpOneOfNeighborMaxPrefixExceedRestartTimeOptionsDef1,
        OneOfNeighborMaxPrefixExceedRestartTimeOptionsDef2,
    ] = _field(metadata={"alias": "restartInterval"})
    threshold: Union[
        V1FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborAddressFamilyThresholdOptionsDef1,
        OneOfNeighborAddressFamilyThresholdOptionsDef2,
        V1FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborAddressFamilyThresholdOptionsDef3,
    ]


@dataclass
class PolicyType3:
    """
    Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is warning-only or disable-peer.
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: V1FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpValue  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfNeighborMaxPrefixNumOptionsDef11:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNeighborAddressFamilyThresholdOptionsDef11:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNeighborAddressFamilyThresholdOptionsDef31:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class TransportGlobalVrfRoutingBgpNeighborMaxPrefixConfigDef3:
    # Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is warning-only or disable-peer.
    policy_type: PolicyType3 = _field(metadata={"alias": "policyType"})
    prefix_num: Union[
        OneOfNeighborMaxPrefixNumOptionsDef11, OneOfNeighborMaxPrefixNumOptionsDef2
    ] = _field(metadata={"alias": "prefixNum"})
    threshold: Union[
        OneOfNeighborAddressFamilyThresholdOptionsDef11,
        OneOfNeighborAddressFamilyThresholdOptionsDef2,
        OneOfNeighborAddressFamilyThresholdOptionsDef31,
    ]


@dataclass
class AddressFamily2:
    family_type: LanIpv6NeighborAfTypeDef = _field(metadata={"alias": "familyType"})
    in_route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "inRoutePolicy"})
    max_prefix_config: Optional[
        Union[
            NeighborMaxPrefixConfigDef1,
            TransportGlobalVrfRoutingBgpNeighborMaxPrefixConfigDef2,
            TransportGlobalVrfRoutingBgpNeighborMaxPrefixConfigDef3,
        ]
    ] = _field(default=None, metadata={"alias": "maxPrefixConfig"})
    out_route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "outRoutePolicy"})


@dataclass
class BgpIpv6Neighbor2:
    peer_group: OneOfNeighborPeerGroupNameOptionsDef3 = _field(metadata={"alias": "peerGroup"})
    remote_as: Union[
        SdRoutingTransportGlobalVrfRoutingBgpOneOfAsNumOptionsDef1, OneOfAsNumOptionsDef2
    ] = _field(metadata={"alias": "remoteAs"})
    address: Optional[
        Union[OneOfIpv6AddrGlobalVariableOptionsDef1, OneOfIpv6AddrGlobalVariableOptionsDef2]
    ] = _field(default=None)
    # Set IPv6 BGP address family
    address_family: Optional[List[AddressFamily2]] = _field(
        default=None, metadata={"alias": "addressFamily"}
    )
    as_number: Optional[
        Union[
            TransportGlobalVrfRoutingBgpOneOfNeighborAsNumberOptionsDef1,
            OneOfNeighborAsNumberOptionsDef2,
            OneOfNeighborAsNumberOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "asNumber"})
    as_override: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "asOverride"})
    description: Optional[
        Union[
            TransportGlobalVrfRoutingBgpOneOfNeighborDescriptionOptionsDef1,
            OneOfNeighborDescriptionOptionsDef2,
            OneOfNeighborDescriptionOptionsDef3,
        ]
    ] = _field(default=None)
    ebgp_multihop: Optional[
        Union[
            TransportGlobalVrfRoutingBgpOneOfNeighborEbgpMultihopOptionsDef1,
            OneOfNeighborEbgpMultihopOptionsDef2,
            TransportGlobalVrfRoutingBgpOneOfNeighborEbgpMultihopOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ebgpMultihop"})
    fall_over_bfd: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "fallOverBfd"})
    holdtime: Optional[
        Union[
            SdRoutingTransportGlobalVrfRoutingBgpOneOfHoldtimeOptionsDef1,
            OneOfHoldtimeOptionsDef2,
            SdRoutingTransportGlobalVrfRoutingBgpOneOfHoldtimeOptionsDef3,
        ]
    ] = _field(default=None)
    if_name: Optional[
        Union[
            OneOfInterfaceNameOptionsDef1,
            OneOfInterfaceNameOptionsDef2,
            OneOfInterfaceNameOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ifName"})
    keepalive: Optional[
        Union[
            SdRoutingTransportGlobalVrfRoutingBgpOneOfKeepaliveOptionsDef1,
            OneOfKeepaliveOptionsDef2,
            SdRoutingTransportGlobalVrfRoutingBgpOneOfKeepaliveOptionsDef3,
        ]
    ] = _field(default=None)
    local_as: Optional[
        Union[
            TransportGlobalVrfRoutingBgpOneOfLocalAsOptionsDef1,
            OneOfLocalAsOptionsDef2,
            OneOfLocalAsOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "localAs"})
    next_hop_self: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "nextHopSelf"})
    password: Optional[
        Union[
            TransportGlobalVrfRoutingBgpOneOfNeighborPasswordOptionsDef1,
            OneOfNeighborPasswordOptionsDef2,
            OneOfNeighborPasswordOptionsDef3,
        ]
    ] = _field(default=None)
    route_reflect_client: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "routeReflectClient"})
    send_community: Optional[
        Union[
            OneOfOnBooleanDefaultTrueOptionsDef1,
            OneOfOnBooleanDefaultTrueOptionsDef2,
            OneOfOnBooleanDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sendCommunity"})
    send_ext_community: Optional[
        Union[
            OneOfOnBooleanDefaultTrueOptionsDef1,
            OneOfOnBooleanDefaultTrueOptionsDef2,
            OneOfOnBooleanDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sendExtCommunity"})
    shutdown: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class BgpOneOfAddressFamilyPathsOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class BgpOneOfIpv4AddressFamilyRedistributeProtocolOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: BgpIpv4AddressFamilyRedistributeProtocolDef  # pytype: disable=annotation-type-mismatch


@dataclass
class BgpOneOfMetricOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class BgpOneOfOspfMatchRouteOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[BgpOspfMatchRouteListDef]  # pytype: disable=annotation-type-mismatch


@dataclass
class RoutingBgpRedistribute:
    protocol: Union[
        BgpOneOfIpv4AddressFamilyRedistributeProtocolOptionsDef1,
        OneOfIpv4AddressFamilyRedistributeProtocolOptionsDef2,
    ]
    metric: Optional[
        Union[BgpOneOfMetricOptionsDef1, OneOfMetricOptionsDef2, OneOfMetricOptionsDef3]
    ] = _field(default=None)
    ospf_match_route: Optional[
        Union[
            BgpOneOfOspfMatchRouteOptionsDef1,
            OneOfOspfMatchRouteOptionsDef2,
            OneOfOspfMatchRouteOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ospfMatchRoute"})
    route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "routePolicy"})


@dataclass
class AddressFamily3:
    """
    Set IPv4 unicast BGP address family
    """

    # Aggregate prefixes in specific range
    aggregate_address: Optional[List[AggregateAddress]] = _field(
        default=None, metadata={"alias": "aggregateAddress"}
    )
    filter: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)
    name: Optional[Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]] = (
        _field(default=None)
    )
    # Configure the networks for BGP to advertise
    network: Optional[List[Network]] = _field(default=None)
    originate: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)
    paths: Optional[
        Union[
            BgpOneOfAddressFamilyPathsOptionsDef1,
            OneOfAddressFamilyPathsOptionsDef2,
            OneOfAddressFamilyPathsOptionsDef3,
        ]
    ] = _field(default=None)
    # Redistribute routes into BGP
    redistribute: Optional[List[RoutingBgpRedistribute]] = _field(default=None)


@dataclass
class RoutingBgpOneOfAddressFamilyPathsOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class BgpOneOfIpv6AddressFamilyRedistributeProtocolOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: BgpIpv6AddressFamilyRedistributeProtocolDef  # pytype: disable=annotation-type-mismatch


@dataclass
class RoutingBgpOneOfMetricOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class RoutingBgpOneOfOspfMatchRouteOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[RoutingBgpOspfMatchRouteListDef]  # pytype: disable=annotation-type-mismatch


@dataclass
class GlobalVrfRoutingBgpRedistribute:
    protocol: Union[
        BgpOneOfIpv6AddressFamilyRedistributeProtocolOptionsDef1,
        OneOfIpv6AddressFamilyRedistributeProtocolOptionsDef2,
    ]
    metric: Optional[
        Union[RoutingBgpOneOfMetricOptionsDef1, OneOfMetricOptionsDef2, OneOfMetricOptionsDef3]
    ] = _field(default=None)
    ospf_match_route: Optional[
        Union[
            RoutingBgpOneOfOspfMatchRouteOptionsDef1,
            OneOfOspfMatchRouteOptionsDef2,
            OneOfOspfMatchRouteOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ospfMatchRoute"})
    route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "routePolicy"})


@dataclass
class BgpIpv6AddressFamily:
    """
    Set BGP address family
    """

    filter: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)
    # IPv6 Aggregate prefixes in specific range
    ipv6_aggregate_address: Optional[List[Ipv6AggregateAddress]] = _field(
        default=None, metadata={"alias": "ipv6AggregateAddress"}
    )
    # Configure the networks for BGP to advertise
    ipv6_network: Optional[List[Ipv6Network]] = _field(
        default=None, metadata={"alias": "ipv6Network"}
    )
    name: Optional[Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]] = (
        _field(default=None)
    )
    originate: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)
    paths: Optional[
        Union[
            RoutingBgpOneOfAddressFamilyPathsOptionsDef1,
            OneOfAddressFamilyPathsOptionsDef2,
            OneOfAddressFamilyPathsOptionsDef3,
        ]
    ] = _field(default=None)
    # Redistribute routes into BGP
    redistribute: Optional[List[GlobalVrfRoutingBgpRedistribute]] = _field(default=None)


@dataclass
class TransportGlobalVrfRoutingBgpData:
    as_num: Union[BgpOneOfAsNumOptionsDef1, OneOfAsNumOptionsDef2] = _field(
        metadata={"alias": "asNum"}
    )
    # Set IPv4 unicast BGP address family
    address_family: Optional[AddressFamily3] = _field(
        default=None, metadata={"alias": "addressFamily"}
    )
    always_compare: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "alwaysCompare"})
    compare_router_id: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "compareRouterId"})
    deterministic: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)
    # BGP dynamic neighbor configuration
    dynamic_neighbor: Optional[
        Union[BgpDynamicNeighbor1, BgpDynamicNeighbor2, BgpDynamicNeighbor3]
    ] = _field(default=None, metadata={"alias": "dynamicNeighbor"})
    external: Optional[
        Union[BgpOneOfExternalOptionsDef1, OneOfExternalOptionsDef2, BgpOneOfExternalOptionsDef3]
    ] = _field(default=None)
    holdtime: Optional[
        Union[BgpOneOfHoldtimeOptionsDef1, OneOfHoldtimeOptionsDef2, BgpOneOfHoldtimeOptionsDef3]
    ] = _field(default=None)
    internal: Optional[
        Union[BgpOneOfInternalOptionsDef1, OneOfInternalOptionsDef2, BgpOneOfInternalOptionsDef3]
    ] = _field(default=None)
    # Set BGP address family
    ipv6_address_family: Optional[BgpIpv6AddressFamily] = _field(
        default=None, metadata={"alias": "ipv6AddressFamily"}
    )
    # Set BGP IPv6 neighbors
    ipv6_neighbor: Optional[List[Union[BgpIpv6Neighbor1, BgpIpv6Neighbor2]]] = _field(
        default=None, metadata={"alias": "ipv6Neighbor"}
    )
    keepalive: Optional[
        Union[BgpOneOfKeepaliveOptionsDef1, OneOfKeepaliveOptionsDef2, BgpOneOfKeepaliveOptionsDef3]
    ] = _field(default=None)
    local: Optional[
        Union[BgpOneOfLocalOptionsDef1, OneOfLocalOptionsDef2, BgpOneOfLocalOptionsDef3]
    ] = _field(default=None)
    missing_as_worst: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "missingAsWorst"})
    multipath_relax: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "multipathRelax"})
    # Set BGP IPv4 neighbors
    neighbor: Optional[List[Union[BgpNeighbor1, BgpNeighbor2]]] = _field(default=None)
    router_id: Optional[
        Union[OneOfRouterIdOptionsDef1, OneOfRouterIdOptionsDef2, OneOfRouterIdOptionsDef3]
    ] = _field(default=None, metadata={"alias": "routerId"})


@dataclass
class BgpPayload:
    """
    SD-Routing BGP for VRF feature schema
    """

    data: TransportGlobalVrfRoutingBgpData
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetTransportVrfAssociatedRoutingBgpFeaturesGetResponse:
    # User who last created this.
    created_by: Optional[str] = _field(default=None, metadata={"alias": "createdBy"})
    # Timestamp of creation
    created_on: Optional[int] = _field(default=None, metadata={"alias": "createdOn"})
    # User who last updated this.
    last_updated_by: Optional[str] = _field(default=None, metadata={"alias": "lastUpdatedBy"})
    # Timestamp of last update
    last_updated_on: Optional[int] = _field(default=None, metadata={"alias": "lastUpdatedOn"})
    parcel_id: Optional[str] = _field(default=None, metadata={"alias": "parcelId"})
    parcel_type: Optional[str] = _field(default=None, metadata={"alias": "parcelType"})
    # SD-Routing BGP for VRF feature schema
    payload: Optional[BgpPayload] = _field(default=None)


@dataclass
class CreateTransportGlobalVrfAndRoutingBgpFeatureAssociationPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class CreateTransportGlobalVrfAndRoutingBgpFeatureAssociationPostRequest:
    """
    Profile Parcel POST Request schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfAsNumOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Union[int, str]


@dataclass
class RoutingBgpOneOfExternalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class RoutingBgpOneOfExternalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class RoutingBgpOneOfInternalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class RoutingBgpOneOfInternalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class RoutingBgpOneOfLocalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class RoutingBgpOneOfLocalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfKeepaliveOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfKeepaliveOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfHoldtimeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfHoldtimeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class TransportGlobalVrfRoutingBgpOneOfMaxListenPrefixNumOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class TransportGlobalVrfRoutingBgpOneOfMaxListenPrefixNumOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNeighborPeerGroupNameOptionsDef4:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class TransportGlobalVrfRoutingBgpIpv4PeerGroup:
    peer_group_name: OneOfNeighborPeerGroupNameOptionsDef4 = _field(
        metadata={"alias": "peerGroupName"}
    )
    # Peer Group IPv4 subnet range
    range: List[Ipv4AddressAndMaskDef]
    # Peer Group IPv4 Address list
    ipv4_address: Optional[List[Ipv4Address]] = _field(
        default=None, metadata={"alias": "ipv4Address"}
    )


@dataclass
class OneOfNeighborPeerGroupNameOptionsDef5:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class TransportGlobalVrfRoutingBgpIpv6PeerGroup:
    peer_group_name: OneOfNeighborPeerGroupNameOptionsDef5 = _field(
        metadata={"alias": "peerGroupName"}
    )
    # Peer Group IPv6 prefix range
    range: List[Range]
    # Peer Group IPv6 Address list
    ipv6_address: Optional[List[Ipv6Address]] = _field(
        default=None, metadata={"alias": "ipv6Address"}
    )


@dataclass
class RoutingBgpDynamicNeighbor1:
    # IPv4 Peer groups
    ipv4_peer_group: List[TransportGlobalVrfRoutingBgpIpv4PeerGroup] = _field(
        metadata={"alias": "ipv4PeerGroup"}
    )
    max_listen_prefix_limit: Union[
        TransportGlobalVrfRoutingBgpOneOfMaxListenPrefixNumOptionsDef1,
        OneOfMaxListenPrefixNumOptionsDef2,
        TransportGlobalVrfRoutingBgpOneOfMaxListenPrefixNumOptionsDef3,
    ] = _field(metadata={"alias": "maxListenPrefixLimit"})
    # IPv6 Peer groups
    ipv6_peer_group: Optional[List[TransportGlobalVrfRoutingBgpIpv6PeerGroup]] = _field(
        default=None, metadata={"alias": "ipv6PeerGroup"}
    )


@dataclass
class SdRoutingTransportGlobalVrfRoutingBgpOneOfMaxListenPrefixNumOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SdRoutingTransportGlobalVrfRoutingBgpOneOfMaxListenPrefixNumOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNeighborPeerGroupNameOptionsDef6:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SdRoutingTransportGlobalVrfRoutingBgpIpv4PeerGroup:
    peer_group_name: OneOfNeighborPeerGroupNameOptionsDef6 = _field(
        metadata={"alias": "peerGroupName"}
    )
    # Peer Group IPv4 subnet range
    range: List[Ipv4AddressAndMaskDef]
    # Peer Group IPv4 Address list
    ipv4_address: Optional[List[Ipv4Address]] = _field(
        default=None, metadata={"alias": "ipv4Address"}
    )


@dataclass
class OneOfNeighborPeerGroupNameOptionsDef7:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SdRoutingTransportGlobalVrfRoutingBgpIpv6PeerGroup:
    peer_group_name: OneOfNeighborPeerGroupNameOptionsDef7 = _field(
        metadata={"alias": "peerGroupName"}
    )
    # Peer Group IPv6 prefix range
    range: List[Range]
    # Peer Group IPv6 Address list
    ipv6_address: Optional[List[Ipv6Address]] = _field(
        default=None, metadata={"alias": "ipv6Address"}
    )


@dataclass
class RoutingBgpDynamicNeighbor2:
    # IPv6 Peer groups
    ipv6_peer_group: List[SdRoutingTransportGlobalVrfRoutingBgpIpv6PeerGroup] = _field(
        metadata={"alias": "ipv6PeerGroup"}
    )
    max_listen_prefix_limit: Union[
        SdRoutingTransportGlobalVrfRoutingBgpOneOfMaxListenPrefixNumOptionsDef1,
        OneOfMaxListenPrefixNumOptionsDef2,
        SdRoutingTransportGlobalVrfRoutingBgpOneOfMaxListenPrefixNumOptionsDef3,
    ] = _field(metadata={"alias": "maxListenPrefixLimit"})
    # IPv4 Peer groups
    ipv4_peer_group: Optional[List[SdRoutingTransportGlobalVrfRoutingBgpIpv4PeerGroup]] = _field(
        default=None, metadata={"alias": "ipv4PeerGroup"}
    )


@dataclass
class FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfMaxListenPrefixNumOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfMaxListenPrefixNumOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNeighborPeerGroupNameOptionsDef8:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpIpv4PeerGroup:
    peer_group_name: OneOfNeighborPeerGroupNameOptionsDef8 = _field(
        metadata={"alias": "peerGroupName"}
    )
    # Peer Group IPv4 subnet range
    range: List[Ipv4AddressAndMaskDef]
    # Peer Group IPv4 Address list
    ipv4_address: Optional[List[Ipv4Address]] = _field(
        default=None, metadata={"alias": "ipv4Address"}
    )


@dataclass
class OneOfNeighborPeerGroupNameOptionsDef9:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpIpv6PeerGroup:
    peer_group_name: OneOfNeighborPeerGroupNameOptionsDef9 = _field(
        metadata={"alias": "peerGroupName"}
    )
    # Peer Group IPv6 prefix range
    range: List[Range]
    # Peer Group IPv6 Address list
    ipv6_address: Optional[List[Ipv6Address]] = _field(
        default=None, metadata={"alias": "ipv6Address"}
    )


@dataclass
class RoutingBgpDynamicNeighbor3:
    # IPv4 Peer groups
    ipv4_peer_group: List[FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpIpv4PeerGroup] = (
        _field(metadata={"alias": "ipv4PeerGroup"})
    )
    # IPv6 Peer groups
    ipv6_peer_group: List[FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpIpv6PeerGroup] = (
        _field(metadata={"alias": "ipv6PeerGroup"})
    )
    max_listen_prefix_limit: Union[
        FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfMaxListenPrefixNumOptionsDef1,
        OneOfMaxListenPrefixNumOptionsDef2,
        FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfMaxListenPrefixNumOptionsDef3,
    ] = _field(metadata={"alias": "maxListenPrefixLimit"})


@dataclass
class OneOfNeighborPeerGroupNameOptionsDef10:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborDescriptionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class V1FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfAsNumOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Union[int, str]


@dataclass
class SdRoutingTransportGlobalVrfRoutingBgpOneOfLocalAsOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Union[int, str]


@dataclass
class V1FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfKeepaliveOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class V1FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfKeepaliveOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class V1FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfHoldtimeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class V1FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfHoldtimeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborEbgpMultihopOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborEbgpMultihopOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborPasswordOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborAsNumberOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class PolicyType4:
    """
    Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is restarting device.
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfNeighborMaxPrefixNumOptionsDef12:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNeighborAddressFamilyThresholdOptionsDef12:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNeighborAddressFamilyThresholdOptionsDef32:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborMaxPrefixExceedRestartTimeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SdRoutingTransportGlobalVrfRoutingBgpNeighborMaxPrefixConfigDef2:
    # Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is restarting device.
    policy_type: PolicyType4 = _field(metadata={"alias": "policyType"})
    prefix_num: Union[
        OneOfNeighborMaxPrefixNumOptionsDef12, OneOfNeighborMaxPrefixNumOptionsDef2
    ] = _field(metadata={"alias": "prefixNum"})
    restart_interval: Union[
        SdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborMaxPrefixExceedRestartTimeOptionsDef1,
        OneOfNeighborMaxPrefixExceedRestartTimeOptionsDef2,
    ] = _field(metadata={"alias": "restartInterval"})
    threshold: Union[
        OneOfNeighborAddressFamilyThresholdOptionsDef12,
        OneOfNeighborAddressFamilyThresholdOptionsDef2,
        OneOfNeighborAddressFamilyThresholdOptionsDef32,
    ]


@dataclass
class PolicyType5:
    """
    Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is warning-only or disable-peer.
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Value1  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfNeighborMaxPrefixNumOptionsDef13:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNeighborAddressFamilyThresholdOptionsDef13:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNeighborAddressFamilyThresholdOptionsDef33:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SdRoutingTransportGlobalVrfRoutingBgpNeighborMaxPrefixConfigDef3:
    # Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is warning-only or disable-peer.
    policy_type: PolicyType5 = _field(metadata={"alias": "policyType"})
    prefix_num: Union[
        OneOfNeighborMaxPrefixNumOptionsDef13, OneOfNeighborMaxPrefixNumOptionsDef2
    ] = _field(metadata={"alias": "prefixNum"})
    threshold: Union[
        OneOfNeighborAddressFamilyThresholdOptionsDef13,
        OneOfNeighborAddressFamilyThresholdOptionsDef2,
        OneOfNeighborAddressFamilyThresholdOptionsDef33,
    ]


@dataclass
class AddressFamily4:
    family_type: LanIpv4NeighborAfTypeDef = _field(metadata={"alias": "familyType"})
    in_route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "inRoutePolicy"})
    max_prefix_config: Optional[
        Union[
            NeighborMaxPrefixConfigDef1,
            SdRoutingTransportGlobalVrfRoutingBgpNeighborMaxPrefixConfigDef2,
            SdRoutingTransportGlobalVrfRoutingBgpNeighborMaxPrefixConfigDef3,
        ]
    ] = _field(default=None, metadata={"alias": "maxPrefixConfig"})
    out_route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "outRoutePolicy"})


@dataclass
class RoutingBgpNeighbor1:
    address: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2]
    remote_as: Union[
        V1FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfAsNumOptionsDef1,
        OneOfAsNumOptionsDef2,
    ] = _field(metadata={"alias": "remoteAs"})
    # Set BGP address family
    address_family: Optional[List[AddressFamily4]] = _field(
        default=None, metadata={"alias": "addressFamily"}
    )
    as_number: Optional[
        Union[
            SdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborAsNumberOptionsDef1,
            OneOfNeighborAsNumberOptionsDef2,
            OneOfNeighborAsNumberOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "asNumber"})
    as_override: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "asOverride"})
    description: Optional[
        Union[
            SdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborDescriptionOptionsDef1,
            OneOfNeighborDescriptionOptionsDef2,
            OneOfNeighborDescriptionOptionsDef3,
        ]
    ] = _field(default=None)
    ebgp_multihop: Optional[
        Union[
            SdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborEbgpMultihopOptionsDef1,
            OneOfNeighborEbgpMultihopOptionsDef2,
            SdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborEbgpMultihopOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ebgpMultihop"})
    fall_over_bfd: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "fallOverBfd"})
    holdtime: Optional[
        Union[
            V1FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfHoldtimeOptionsDef1,
            OneOfHoldtimeOptionsDef2,
            V1FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfHoldtimeOptionsDef3,
        ]
    ] = _field(default=None)
    if_name: Optional[
        Union[
            OneOfInterfaceNameOptionsDef1,
            OneOfInterfaceNameOptionsDef2,
            OneOfInterfaceNameOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ifName"})
    keepalive: Optional[
        Union[
            V1FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfKeepaliveOptionsDef1,
            OneOfKeepaliveOptionsDef2,
            V1FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfKeepaliveOptionsDef3,
        ]
    ] = _field(default=None)
    local_as: Optional[
        Union[
            SdRoutingTransportGlobalVrfRoutingBgpOneOfLocalAsOptionsDef1,
            OneOfLocalAsOptionsDef2,
            OneOfLocalAsOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "localAs"})
    next_hop_self: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "nextHopSelf"})
    password: Optional[
        Union[
            SdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborPasswordOptionsDef1,
            OneOfNeighborPasswordOptionsDef2,
            OneOfNeighborPasswordOptionsDef3,
        ]
    ] = _field(default=None)
    peer_group: Optional[OneOfNeighborPeerGroupNameOptionsDef10] = _field(
        default=None, metadata={"alias": "peerGroup"}
    )
    route_reflect_client: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "routeReflectClient"})
    send_community: Optional[
        Union[
            OneOfOnBooleanDefaultTrueOptionsDef1,
            OneOfOnBooleanDefaultTrueOptionsDef2,
            OneOfOnBooleanDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sendCommunity"})
    send_ext_community: Optional[
        Union[
            OneOfOnBooleanDefaultTrueOptionsDef1,
            OneOfOnBooleanDefaultTrueOptionsDef2,
            OneOfOnBooleanDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sendExtCommunity"})
    shutdown: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class OneOfNeighborPeerGroupNameOptionsDef11:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborDescriptionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfAsNumOptionsDef11:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Union[int, str]


@dataclass
class FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfLocalAsOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Union[int, str]


@dataclass
class OneOfKeepaliveOptionsDef11:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfKeepaliveOptionsDef31:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfHoldtimeOptionsDef11:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfHoldtimeOptionsDef31:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborEbgpMultihopOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborEbgpMultihopOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborPasswordOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborAsNumberOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class PolicyType6:
    """
    Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is restarting device.
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfNeighborMaxPrefixNumOptionsDef14:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNeighborAddressFamilyThresholdOptionsDef14:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNeighborAddressFamilyThresholdOptionsDef34:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborMaxPrefixExceedRestartTimeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpNeighborMaxPrefixConfigDef2:
    # Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is restarting device.
    policy_type: PolicyType6 = _field(metadata={"alias": "policyType"})
    prefix_num: Union[
        OneOfNeighborMaxPrefixNumOptionsDef14, OneOfNeighborMaxPrefixNumOptionsDef2
    ] = _field(metadata={"alias": "prefixNum"})
    restart_interval: Union[
        FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborMaxPrefixExceedRestartTimeOptionsDef1,
        OneOfNeighborMaxPrefixExceedRestartTimeOptionsDef2,
    ] = _field(metadata={"alias": "restartInterval"})
    threshold: Union[
        OneOfNeighborAddressFamilyThresholdOptionsDef14,
        OneOfNeighborAddressFamilyThresholdOptionsDef2,
        OneOfNeighborAddressFamilyThresholdOptionsDef34,
    ]


@dataclass
class PolicyType7:
    """
    Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is warning-only or disable-peer.
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Value2  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfNeighborMaxPrefixNumOptionsDef15:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNeighborAddressFamilyThresholdOptionsDef15:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNeighborAddressFamilyThresholdOptionsDef35:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpNeighborMaxPrefixConfigDef3:
    # Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is warning-only or disable-peer.
    policy_type: PolicyType7 = _field(metadata={"alias": "policyType"})
    prefix_num: Union[
        OneOfNeighborMaxPrefixNumOptionsDef15, OneOfNeighborMaxPrefixNumOptionsDef2
    ] = _field(metadata={"alias": "prefixNum"})
    threshold: Union[
        OneOfNeighborAddressFamilyThresholdOptionsDef15,
        OneOfNeighborAddressFamilyThresholdOptionsDef2,
        OneOfNeighborAddressFamilyThresholdOptionsDef35,
    ]


@dataclass
class AddressFamily5:
    family_type: LanIpv4NeighborAfTypeDef = _field(metadata={"alias": "familyType"})
    in_route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "inRoutePolicy"})
    max_prefix_config: Optional[
        Union[
            NeighborMaxPrefixConfigDef1,
            FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpNeighborMaxPrefixConfigDef2,
            FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpNeighborMaxPrefixConfigDef3,
        ]
    ] = _field(default=None, metadata={"alias": "maxPrefixConfig"})
    out_route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "outRoutePolicy"})


@dataclass
class RoutingBgpNeighbor2:
    peer_group: OneOfNeighborPeerGroupNameOptionsDef11 = _field(metadata={"alias": "peerGroup"})
    remote_as: Union[OneOfAsNumOptionsDef11, OneOfAsNumOptionsDef2] = _field(
        metadata={"alias": "remoteAs"}
    )
    address: Optional[Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2]] = _field(
        default=None
    )
    # Set BGP address family
    address_family: Optional[List[AddressFamily5]] = _field(
        default=None, metadata={"alias": "addressFamily"}
    )
    as_number: Optional[
        Union[
            FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborAsNumberOptionsDef1,
            OneOfNeighborAsNumberOptionsDef2,
            OneOfNeighborAsNumberOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "asNumber"})
    as_override: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "asOverride"})
    description: Optional[
        Union[
            FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborDescriptionOptionsDef1,
            OneOfNeighborDescriptionOptionsDef2,
            OneOfNeighborDescriptionOptionsDef3,
        ]
    ] = _field(default=None)
    ebgp_multihop: Optional[
        Union[
            FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborEbgpMultihopOptionsDef1,
            OneOfNeighborEbgpMultihopOptionsDef2,
            FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborEbgpMultihopOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ebgpMultihop"})
    fall_over_bfd: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "fallOverBfd"})
    holdtime: Optional[
        Union[OneOfHoldtimeOptionsDef11, OneOfHoldtimeOptionsDef2, OneOfHoldtimeOptionsDef31]
    ] = _field(default=None)
    if_name: Optional[
        Union[
            OneOfInterfaceNameOptionsDef1,
            OneOfInterfaceNameOptionsDef2,
            OneOfInterfaceNameOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ifName"})
    keepalive: Optional[
        Union[OneOfKeepaliveOptionsDef11, OneOfKeepaliveOptionsDef2, OneOfKeepaliveOptionsDef31]
    ] = _field(default=None)
    local_as: Optional[
        Union[
            FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfLocalAsOptionsDef1,
            OneOfLocalAsOptionsDef2,
            OneOfLocalAsOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "localAs"})
    next_hop_self: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "nextHopSelf"})
    password: Optional[
        Union[
            FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborPasswordOptionsDef1,
            OneOfNeighborPasswordOptionsDef2,
            OneOfNeighborPasswordOptionsDef3,
        ]
    ] = _field(default=None)
    route_reflect_client: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "routeReflectClient"})
    send_community: Optional[
        Union[
            OneOfOnBooleanDefaultTrueOptionsDef1,
            OneOfOnBooleanDefaultTrueOptionsDef2,
            OneOfOnBooleanDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sendCommunity"})
    send_ext_community: Optional[
        Union[
            OneOfOnBooleanDefaultTrueOptionsDef1,
            OneOfOnBooleanDefaultTrueOptionsDef2,
            OneOfOnBooleanDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sendExtCommunity"})
    shutdown: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class OneOfNeighborPeerGroupNameOptionsDef12:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class V1FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborDescriptionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfAsNumOptionsDef12:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Union[int, str]


@dataclass
class V1FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfLocalAsOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Union[int, str]


@dataclass
class OneOfKeepaliveOptionsDef12:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfKeepaliveOptionsDef32:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfHoldtimeOptionsDef12:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfHoldtimeOptionsDef32:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class V1FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborEbgpMultihopOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class V1FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborEbgpMultihopOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class V1FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborPasswordOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class V1FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborAsNumberOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class PolicyType8:
    """
    Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is restarting device.
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfNeighborMaxPrefixNumOptionsDef16:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNeighborAddressFamilyThresholdOptionsDef16:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNeighborAddressFamilyThresholdOptionsDef36:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class V1FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborMaxPrefixExceedRestartTimeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class V1FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpNeighborMaxPrefixConfigDef2:
    # Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is restarting device.
    policy_type: PolicyType8 = _field(metadata={"alias": "policyType"})
    prefix_num: Union[
        OneOfNeighborMaxPrefixNumOptionsDef16, OneOfNeighborMaxPrefixNumOptionsDef2
    ] = _field(metadata={"alias": "prefixNum"})
    restart_interval: Union[
        V1FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborMaxPrefixExceedRestartTimeOptionsDef1,
        OneOfNeighborMaxPrefixExceedRestartTimeOptionsDef2,
    ] = _field(metadata={"alias": "restartInterval"})
    threshold: Union[
        OneOfNeighborAddressFamilyThresholdOptionsDef16,
        OneOfNeighborAddressFamilyThresholdOptionsDef2,
        OneOfNeighborAddressFamilyThresholdOptionsDef36,
    ]


@dataclass
class PolicyType9:
    """
    Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is warning-only or disable-peer.
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Value3  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfNeighborMaxPrefixNumOptionsDef17:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNeighborAddressFamilyThresholdOptionsDef17:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNeighborAddressFamilyThresholdOptionsDef37:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class V1FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpNeighborMaxPrefixConfigDef3:
    # Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is warning-only or disable-peer.
    policy_type: PolicyType9 = _field(metadata={"alias": "policyType"})
    prefix_num: Union[
        OneOfNeighborMaxPrefixNumOptionsDef17, OneOfNeighborMaxPrefixNumOptionsDef2
    ] = _field(metadata={"alias": "prefixNum"})
    threshold: Union[
        OneOfNeighborAddressFamilyThresholdOptionsDef17,
        OneOfNeighborAddressFamilyThresholdOptionsDef2,
        OneOfNeighborAddressFamilyThresholdOptionsDef37,
    ]


@dataclass
class AddressFamily6:
    family_type: LanIpv6NeighborAfTypeDef = _field(metadata={"alias": "familyType"})
    in_route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "inRoutePolicy"})
    max_prefix_config: Optional[
        Union[
            NeighborMaxPrefixConfigDef1,
            V1FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpNeighborMaxPrefixConfigDef2,
            V1FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpNeighborMaxPrefixConfigDef3,
        ]
    ] = _field(default=None, metadata={"alias": "maxPrefixConfig"})
    out_route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "outRoutePolicy"})


@dataclass
class RoutingBgpIpv6Neighbor1:
    address: Union[OneOfIpv6AddrGlobalVariableOptionsDef1, OneOfIpv6AddrGlobalVariableOptionsDef2]
    remote_as: Union[OneOfAsNumOptionsDef12, OneOfAsNumOptionsDef2] = _field(
        metadata={"alias": "remoteAs"}
    )
    # Set IPv6 BGP address family
    address_family: Optional[List[AddressFamily6]] = _field(
        default=None, metadata={"alias": "addressFamily"}
    )
    as_number: Optional[
        Union[
            V1FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborAsNumberOptionsDef1,
            OneOfNeighborAsNumberOptionsDef2,
            OneOfNeighborAsNumberOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "asNumber"})
    as_override: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "asOverride"})
    description: Optional[
        Union[
            V1FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborDescriptionOptionsDef1,
            OneOfNeighborDescriptionOptionsDef2,
            OneOfNeighborDescriptionOptionsDef3,
        ]
    ] = _field(default=None)
    ebgp_multihop: Optional[
        Union[
            V1FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborEbgpMultihopOptionsDef1,
            OneOfNeighborEbgpMultihopOptionsDef2,
            V1FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborEbgpMultihopOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ebgpMultihop"})
    fall_over_bfd: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "fallOverBfd"})
    holdtime: Optional[
        Union[OneOfHoldtimeOptionsDef12, OneOfHoldtimeOptionsDef2, OneOfHoldtimeOptionsDef32]
    ] = _field(default=None)
    if_name: Optional[
        Union[
            OneOfInterfaceNameOptionsDef1,
            OneOfInterfaceNameOptionsDef2,
            OneOfInterfaceNameOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ifName"})
    keepalive: Optional[
        Union[OneOfKeepaliveOptionsDef12, OneOfKeepaliveOptionsDef2, OneOfKeepaliveOptionsDef32]
    ] = _field(default=None)
    local_as: Optional[
        Union[
            V1FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfLocalAsOptionsDef1,
            OneOfLocalAsOptionsDef2,
            OneOfLocalAsOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "localAs"})
    next_hop_self: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "nextHopSelf"})
    password: Optional[
        Union[
            V1FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfNeighborPasswordOptionsDef1,
            OneOfNeighborPasswordOptionsDef2,
            OneOfNeighborPasswordOptionsDef3,
        ]
    ] = _field(default=None)
    peer_group: Optional[OneOfNeighborPeerGroupNameOptionsDef12] = _field(
        default=None, metadata={"alias": "peerGroup"}
    )
    route_reflect_client: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "routeReflectClient"})
    send_community: Optional[
        Union[
            OneOfOnBooleanDefaultTrueOptionsDef1,
            OneOfOnBooleanDefaultTrueOptionsDef2,
            OneOfOnBooleanDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sendCommunity"})
    send_ext_community: Optional[
        Union[
            OneOfOnBooleanDefaultTrueOptionsDef1,
            OneOfOnBooleanDefaultTrueOptionsDef2,
            OneOfOnBooleanDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sendExtCommunity"})
    shutdown: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class OneOfNeighborPeerGroupNameOptionsDef13:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfNeighborDescriptionOptionsDef11:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfAsNumOptionsDef13:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Union[int, str]


@dataclass
class OneOfLocalAsOptionsDef11:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Union[int, str]


@dataclass
class OneOfKeepaliveOptionsDef13:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfKeepaliveOptionsDef33:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfHoldtimeOptionsDef13:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfHoldtimeOptionsDef33:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNeighborEbgpMultihopOptionsDef11:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNeighborEbgpMultihopOptionsDef31:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNeighborPasswordOptionsDef11:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfNeighborAsNumberOptionsDef11:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class PolicyType10:
    """
    Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is restarting device.
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfNeighborMaxPrefixNumOptionsDef18:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNeighborAddressFamilyThresholdOptionsDef18:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNeighborAddressFamilyThresholdOptionsDef38:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNeighborMaxPrefixExceedRestartTimeOptionsDef11:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class NeighborMaxPrefixConfigDef21:
    # Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is restarting device.
    policy_type: PolicyType10 = _field(metadata={"alias": "policyType"})
    prefix_num: Union[
        OneOfNeighborMaxPrefixNumOptionsDef18, OneOfNeighborMaxPrefixNumOptionsDef2
    ] = _field(metadata={"alias": "prefixNum"})
    restart_interval: Union[
        OneOfNeighborMaxPrefixExceedRestartTimeOptionsDef11,
        OneOfNeighborMaxPrefixExceedRestartTimeOptionsDef2,
    ] = _field(metadata={"alias": "restartInterval"})
    threshold: Union[
        OneOfNeighborAddressFamilyThresholdOptionsDef18,
        OneOfNeighborAddressFamilyThresholdOptionsDef2,
        OneOfNeighborAddressFamilyThresholdOptionsDef38,
    ]


@dataclass
class PolicyType11:
    """
    Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is warning-only or disable-peer.
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Value4  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfNeighborMaxPrefixNumOptionsDef19:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNeighborAddressFamilyThresholdOptionsDef19:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNeighborAddressFamilyThresholdOptionsDef39:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class NeighborMaxPrefixConfigDef31:
    # Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is warning-only or disable-peer.
    policy_type: PolicyType11 = _field(metadata={"alias": "policyType"})
    prefix_num: Union[
        OneOfNeighborMaxPrefixNumOptionsDef19, OneOfNeighborMaxPrefixNumOptionsDef2
    ] = _field(metadata={"alias": "prefixNum"})
    threshold: Union[
        OneOfNeighborAddressFamilyThresholdOptionsDef19,
        OneOfNeighborAddressFamilyThresholdOptionsDef2,
        OneOfNeighborAddressFamilyThresholdOptionsDef39,
    ]


@dataclass
class AddressFamily7:
    family_type: LanIpv6NeighborAfTypeDef = _field(metadata={"alias": "familyType"})
    in_route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "inRoutePolicy"})
    max_prefix_config: Optional[
        Union[
            NeighborMaxPrefixConfigDef1, NeighborMaxPrefixConfigDef21, NeighborMaxPrefixConfigDef31
        ]
    ] = _field(default=None, metadata={"alias": "maxPrefixConfig"})
    out_route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "outRoutePolicy"})


@dataclass
class RoutingBgpIpv6Neighbor2:
    peer_group: OneOfNeighborPeerGroupNameOptionsDef13 = _field(metadata={"alias": "peerGroup"})
    remote_as: Union[OneOfAsNumOptionsDef13, OneOfAsNumOptionsDef2] = _field(
        metadata={"alias": "remoteAs"}
    )
    address: Optional[
        Union[OneOfIpv6AddrGlobalVariableOptionsDef1, OneOfIpv6AddrGlobalVariableOptionsDef2]
    ] = _field(default=None)
    # Set IPv6 BGP address family
    address_family: Optional[List[AddressFamily7]] = _field(
        default=None, metadata={"alias": "addressFamily"}
    )
    as_number: Optional[
        Union[
            OneOfNeighborAsNumberOptionsDef11,
            OneOfNeighborAsNumberOptionsDef2,
            OneOfNeighborAsNumberOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "asNumber"})
    as_override: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "asOverride"})
    description: Optional[
        Union[
            OneOfNeighborDescriptionOptionsDef11,
            OneOfNeighborDescriptionOptionsDef2,
            OneOfNeighborDescriptionOptionsDef3,
        ]
    ] = _field(default=None)
    ebgp_multihop: Optional[
        Union[
            OneOfNeighborEbgpMultihopOptionsDef11,
            OneOfNeighborEbgpMultihopOptionsDef2,
            OneOfNeighborEbgpMultihopOptionsDef31,
        ]
    ] = _field(default=None, metadata={"alias": "ebgpMultihop"})
    fall_over_bfd: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "fallOverBfd"})
    holdtime: Optional[
        Union[OneOfHoldtimeOptionsDef13, OneOfHoldtimeOptionsDef2, OneOfHoldtimeOptionsDef33]
    ] = _field(default=None)
    if_name: Optional[
        Union[
            OneOfInterfaceNameOptionsDef1,
            OneOfInterfaceNameOptionsDef2,
            OneOfInterfaceNameOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ifName"})
    keepalive: Optional[
        Union[OneOfKeepaliveOptionsDef13, OneOfKeepaliveOptionsDef2, OneOfKeepaliveOptionsDef33]
    ] = _field(default=None)
    local_as: Optional[
        Union[OneOfLocalAsOptionsDef11, OneOfLocalAsOptionsDef2, OneOfLocalAsOptionsDef3]
    ] = _field(default=None, metadata={"alias": "localAs"})
    next_hop_self: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "nextHopSelf"})
    password: Optional[
        Union[
            OneOfNeighborPasswordOptionsDef11,
            OneOfNeighborPasswordOptionsDef2,
            OneOfNeighborPasswordOptionsDef3,
        ]
    ] = _field(default=None)
    route_reflect_client: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "routeReflectClient"})
    send_community: Optional[
        Union[
            OneOfOnBooleanDefaultTrueOptionsDef1,
            OneOfOnBooleanDefaultTrueOptionsDef2,
            OneOfOnBooleanDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sendCommunity"})
    send_ext_community: Optional[
        Union[
            OneOfOnBooleanDefaultTrueOptionsDef1,
            OneOfOnBooleanDefaultTrueOptionsDef2,
            OneOfOnBooleanDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sendExtCommunity"})
    shutdown: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class GlobalVrfRoutingBgpOneOfAddressFamilyPathsOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class RoutingBgpOneOfIpv4AddressFamilyRedistributeProtocolOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: RoutingBgpIpv4AddressFamilyRedistributeProtocolDef  # pytype: disable=annotation-type-mismatch


@dataclass
class GlobalVrfRoutingBgpOneOfMetricOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class GlobalVrfRoutingBgpOneOfOspfMatchRouteOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[
        GlobalVrfRoutingBgpOspfMatchRouteListDef
    ]  # pytype: disable=annotation-type-mismatch


@dataclass
class TransportGlobalVrfRoutingBgpRedistribute:
    protocol: Union[
        RoutingBgpOneOfIpv4AddressFamilyRedistributeProtocolOptionsDef1,
        OneOfIpv4AddressFamilyRedistributeProtocolOptionsDef2,
    ]
    metric: Optional[
        Union[
            GlobalVrfRoutingBgpOneOfMetricOptionsDef1,
            OneOfMetricOptionsDef2,
            OneOfMetricOptionsDef3,
        ]
    ] = _field(default=None)
    ospf_match_route: Optional[
        Union[
            GlobalVrfRoutingBgpOneOfOspfMatchRouteOptionsDef1,
            OneOfOspfMatchRouteOptionsDef2,
            OneOfOspfMatchRouteOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ospfMatchRoute"})
    route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "routePolicy"})


@dataclass
class AddressFamily8:
    """
    Set IPv4 unicast BGP address family
    """

    # Aggregate prefixes in specific range
    aggregate_address: Optional[List[AggregateAddress]] = _field(
        default=None, metadata={"alias": "aggregateAddress"}
    )
    filter: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)
    name: Optional[Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]] = (
        _field(default=None)
    )
    # Configure the networks for BGP to advertise
    network: Optional[List[Network]] = _field(default=None)
    originate: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)
    paths: Optional[
        Union[
            GlobalVrfRoutingBgpOneOfAddressFamilyPathsOptionsDef1,
            OneOfAddressFamilyPathsOptionsDef2,
            OneOfAddressFamilyPathsOptionsDef3,
        ]
    ] = _field(default=None)
    # Redistribute routes into BGP
    redistribute: Optional[List[TransportGlobalVrfRoutingBgpRedistribute]] = _field(default=None)


@dataclass
class TransportGlobalVrfRoutingBgpOneOfAddressFamilyPathsOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class RoutingBgpOneOfIpv6AddressFamilyRedistributeProtocolOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: RoutingBgpIpv6AddressFamilyRedistributeProtocolDef  # pytype: disable=annotation-type-mismatch


@dataclass
class TransportGlobalVrfRoutingBgpOneOfMetricOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class TransportGlobalVrfRoutingBgpOneOfOspfMatchRouteOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[
        TransportGlobalVrfRoutingBgpOspfMatchRouteListDef
    ]  # pytype: disable=annotation-type-mismatch


@dataclass
class SdRoutingTransportGlobalVrfRoutingBgpRedistribute:
    protocol: Union[
        RoutingBgpOneOfIpv6AddressFamilyRedistributeProtocolOptionsDef1,
        OneOfIpv6AddressFamilyRedistributeProtocolOptionsDef2,
    ]
    metric: Optional[
        Union[
            TransportGlobalVrfRoutingBgpOneOfMetricOptionsDef1,
            OneOfMetricOptionsDef2,
            OneOfMetricOptionsDef3,
        ]
    ] = _field(default=None)
    ospf_match_route: Optional[
        Union[
            TransportGlobalVrfRoutingBgpOneOfOspfMatchRouteOptionsDef1,
            OneOfOspfMatchRouteOptionsDef2,
            OneOfOspfMatchRouteOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ospfMatchRoute"})
    route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "routePolicy"})


@dataclass
class RoutingBgpIpv6AddressFamily:
    """
    Set BGP address family
    """

    filter: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)
    # IPv6 Aggregate prefixes in specific range
    ipv6_aggregate_address: Optional[List[Ipv6AggregateAddress]] = _field(
        default=None, metadata={"alias": "ipv6AggregateAddress"}
    )
    # Configure the networks for BGP to advertise
    ipv6_network: Optional[List[Ipv6Network]] = _field(
        default=None, metadata={"alias": "ipv6Network"}
    )
    name: Optional[Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]] = (
        _field(default=None)
    )
    originate: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)
    paths: Optional[
        Union[
            TransportGlobalVrfRoutingBgpOneOfAddressFamilyPathsOptionsDef1,
            OneOfAddressFamilyPathsOptionsDef2,
            OneOfAddressFamilyPathsOptionsDef3,
        ]
    ] = _field(default=None)
    # Redistribute routes into BGP
    redistribute: Optional[List[SdRoutingTransportGlobalVrfRoutingBgpRedistribute]] = _field(
        default=None
    )


@dataclass
class SdRoutingTransportGlobalVrfRoutingBgpData:
    as_num: Union[
        FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfAsNumOptionsDef1,
        OneOfAsNumOptionsDef2,
    ] = _field(metadata={"alias": "asNum"})
    # Set IPv4 unicast BGP address family
    address_family: Optional[AddressFamily8] = _field(
        default=None, metadata={"alias": "addressFamily"}
    )
    always_compare: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "alwaysCompare"})
    compare_router_id: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "compareRouterId"})
    deterministic: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)
    # BGP dynamic neighbor configuration
    dynamic_neighbor: Optional[
        Union[RoutingBgpDynamicNeighbor1, RoutingBgpDynamicNeighbor2, RoutingBgpDynamicNeighbor3]
    ] = _field(default=None, metadata={"alias": "dynamicNeighbor"})
    external: Optional[
        Union[
            RoutingBgpOneOfExternalOptionsDef1,
            OneOfExternalOptionsDef2,
            RoutingBgpOneOfExternalOptionsDef3,
        ]
    ] = _field(default=None)
    holdtime: Optional[
        Union[
            FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfHoldtimeOptionsDef1,
            OneOfHoldtimeOptionsDef2,
            FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfHoldtimeOptionsDef3,
        ]
    ] = _field(default=None)
    internal: Optional[
        Union[
            RoutingBgpOneOfInternalOptionsDef1,
            OneOfInternalOptionsDef2,
            RoutingBgpOneOfInternalOptionsDef3,
        ]
    ] = _field(default=None)
    # Set BGP address family
    ipv6_address_family: Optional[RoutingBgpIpv6AddressFamily] = _field(
        default=None, metadata={"alias": "ipv6AddressFamily"}
    )
    # Set BGP IPv6 neighbors
    ipv6_neighbor: Optional[List[Union[RoutingBgpIpv6Neighbor1, RoutingBgpIpv6Neighbor2]]] = _field(
        default=None, metadata={"alias": "ipv6Neighbor"}
    )
    keepalive: Optional[
        Union[
            FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfKeepaliveOptionsDef1,
            OneOfKeepaliveOptionsDef2,
            FeatureProfileSdRoutingTransportGlobalVrfRoutingBgpOneOfKeepaliveOptionsDef3,
        ]
    ] = _field(default=None)
    local: Optional[
        Union[
            RoutingBgpOneOfLocalOptionsDef1, OneOfLocalOptionsDef2, RoutingBgpOneOfLocalOptionsDef3
        ]
    ] = _field(default=None)
    missing_as_worst: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "missingAsWorst"})
    multipath_relax: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "multipathRelax"})
    # Set BGP IPv4 neighbors
    neighbor: Optional[List[Union[RoutingBgpNeighbor1, RoutingBgpNeighbor2]]] = _field(default=None)
    router_id: Optional[
        Union[OneOfRouterIdOptionsDef1, OneOfRouterIdOptionsDef2, OneOfRouterIdOptionsDef3]
    ] = _field(default=None, metadata={"alias": "routerId"})


@dataclass
class RoutingBgpPayload:
    """
    SD-Routing BGP for VRF feature schema
    """

    data: SdRoutingTransportGlobalVrfRoutingBgpData
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetSingleSdRoutingTransportGlobalVrfGlobalVrfRoutingBgpPayload:
    # User who last created this.
    created_by: Optional[str] = _field(default=None, metadata={"alias": "createdBy"})
    # Timestamp of creation
    created_on: Optional[int] = _field(default=None, metadata={"alias": "createdOn"})
    # User who last updated this.
    last_updated_by: Optional[str] = _field(default=None, metadata={"alias": "lastUpdatedBy"})
    # Timestamp of last update
    last_updated_on: Optional[int] = _field(default=None, metadata={"alias": "lastUpdatedOn"})
    parcel_id: Optional[str] = _field(default=None, metadata={"alias": "parcelId"})
    parcel_type: Optional[str] = _field(default=None, metadata={"alias": "parcelType"})
    # SD-Routing BGP for VRF feature schema
    payload: Optional[RoutingBgpPayload] = _field(default=None)


@dataclass
class EditTransportGlobalVrfAndRoutingBgpFeatureAssociationPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class EditTransportGlobalVrfAndRoutingBgpFeatureAssociationPutRequest:
    """
    Profile Parcel POST Request schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)
