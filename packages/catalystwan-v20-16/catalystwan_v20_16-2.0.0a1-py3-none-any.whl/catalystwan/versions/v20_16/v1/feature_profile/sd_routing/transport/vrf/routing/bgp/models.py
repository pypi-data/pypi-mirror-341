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

Ipv4AddressFamilyRedistributeProtocolDef = Literal["connected", "eigrp", "ospf", "ospfv3", "static"]

OspfMatchRouteListDef = Literal["External-type1", "External-type2", "Internal"]

Ipv6AddressFamilyRedistributeProtocolDef = Literal["connected", "ospf", "static"]


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
class LanIpv4NeighborAfTypeDef:
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
    family_type: LanIpv4NeighborAfTypeDef = _field(metadata={"alias": "familyType"})
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
class LanIpv6NeighborAfTypeDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: RoutingBgpValue


@dataclass
class BgpAddressFamily:
    family_type: LanIpv6NeighborAfTypeDef = _field(metadata={"alias": "familyType"})
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
    family_type: LanIpv6NeighborAfTypeDef = _field(metadata={"alias": "familyType"})
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
class VrfRoutingBgpAddressFamily:
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
    address_family: Optional[VrfRoutingBgpAddressFamily] = _field(
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
    SD-Routing BGP for VRF feature schema
    """

    data: BgpData
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


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
    # SD-Routing BGP for VRF feature schema
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdRoutingTransportVrfRoutingBgpPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateSdroutingTransportVrfBgpFeaturePostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class TransportVrfRoutingBgpAddressFamily:
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
    address_family: Optional[TransportVrfRoutingBgpAddressFamily] = _field(
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
class CreateSdroutingTransportVrfBgpFeaturePostRequest:
    """
    SD-Routing BGP for VRF feature schema
    """

    data: RoutingBgpData
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetSingleSdRoutingTransportVrfRoutingBgpPayload:
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
    payload: Optional[Payload] = _field(default=None)


@dataclass
class EditSdroutingTransportVrfBgpFeaturePutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SdRoutingTransportVrfRoutingBgpAddressFamily:
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
class VrfRoutingBgpData:
    as_num: Union[OneOfAsNumOptionsDef1, OneOfAsNumOptionsDef2] = _field(
        metadata={"alias": "asNum"}
    )
    # Set IPv4 unicast BGP address family
    address_family: Optional[SdRoutingTransportVrfRoutingBgpAddressFamily] = _field(
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
class EditSdroutingTransportVrfBgpFeaturePutRequest:
    """
    SD-Routing BGP for VRF feature schema
    """

    data: VrfRoutingBgpData
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetTransportVrfAssociatedRoutingBgpFeatures1GetResponse:
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
    payload: Optional[Payload] = _field(default=None)


@dataclass
class CreateTransportVrfAndRoutingBgpFeatureAssociationPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class CreateTransportVrfAndRoutingBgpFeatureAssociationPostRequest:
    """
    Profile Parcel POST Request schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetSingleSdRoutingTransportVrfVrfRoutingBgpPayload:
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
    payload: Optional[Payload] = _field(default=None)


@dataclass
class EditTransportVrfAndRoutingBgpFeatureAssociationPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class EditTransportVrfAndRoutingBgpFeatureAssociationPutRequest:
    """
    Profile Parcel POST Request schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)
