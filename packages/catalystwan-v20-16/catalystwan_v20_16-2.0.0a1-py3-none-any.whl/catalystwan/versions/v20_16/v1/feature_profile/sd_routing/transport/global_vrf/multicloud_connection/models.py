# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

VariableOptionTypeDef = Literal["variable"]

GlobalOptionTypeDef = Literal["global"]

ExtensionsParcelTypeDef = Literal[
    "global-vrf",
    "global-vrf/routing/bgp",
    "global-vrf/wan/interface/ipsec",
    "management-vrf",
    "management-vrf/interface/ethernet",
    "vrf/routing/bgp",
    "vrf/wan/interface/ethernet",
    "vrf/wan/interface/gre",
    "vrf/wan/interface/ipsec",
]

DefaultOptionTypeDef = Literal["default"]

Value = Literal["ipv4-unicast", "vpnv4-unicast", "vpnv6-unicast"]

MulticloudConnectionValue = Literal["disable-peer", "warning-only"]

GlobalVrfMulticloudConnectionValue = Literal["ipv6-unicast", "vpnv6-unicast"]

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

Ipv4AddressFamilyRedistributeProtocolDef = Literal["connected", "nat", "ospf", "ospfv3", "static"]

Ipv6AddressFamilyRedistributeProtocolDef = Literal["connected", "ospf", "static"]

Ipv4GatewayDef = Literal["dhcp", "nextHop", "null0"]

DefaultIpv4GatewayDef = Literal["nextHop"]

Ipv6RouteNatDef = Literal["NAT64", "NAT66"]


@dataclass
class CreateTransportGlobalVrfAndMulticloudConnectionParcelAssociationPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class VariableOptionTypeObjectDef:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfExtensionsParcelTypeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ExtensionsParcelTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfExtensionsParcelTypeOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfExtensionsParcelIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfExtensionsParcelIdOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


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
class OneOfOnBooleanDefaultFalseNoVariableOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfOnBooleanDefaultFalseNoVariableOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


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
    value: Value  # pytype: disable=annotation-type-mismatch


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
class MulticloudConnectionPolicyType:
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
    policy_type: MulticloudConnectionPolicyType = _field(metadata={"alias": "policyType"})
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
class GlobalVrfMulticloudConnectionPolicyType:
    """
    Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is warning-only or disable-peer.
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: MulticloudConnectionValue  # pytype: disable=annotation-type-mismatch


@dataclass
class NeighborMaxPrefixConfigDef3:
    # Neighbor maximum prefix policy is enabled, when maximum prefix threshold is exceeded, policy action is warning-only or disable-peer.
    policy_type: GlobalVrfMulticloudConnectionPolicyType = _field(metadata={"alias": "policyType"})
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
class Neighbor:
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
    holdtime: Optional[Union[OneOfHoldtimeOptionsDef1, OneOfHoldtimeOptionsDef2]] = _field(
        default=None
    )
    if_name: Optional[
        Union[
            OneOfInterfaceNameOptionsDef1,
            OneOfInterfaceNameOptionsDef2,
            OneOfInterfaceNameOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ifName"})
    keepalive: Optional[Union[OneOfKeepaliveOptionsDef1, OneOfKeepaliveOptionsDef2]] = _field(
        default=None
    )
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
    send_label: Optional[
        Union[
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef1,
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "sendLabel"})
    send_label_explicit: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sendLabelExplicit"})
    shutdown: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)


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
class WanIpv6NeighborAfTypeDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: GlobalVrfMulticloudConnectionValue  # pytype: disable=annotation-type-mismatch


@dataclass
class MulticloudConnectionAddressFamily:
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
class Ipv6Neighbor:
    address: Union[OneOfIpv6AddrGlobalVariableOptionsDef1, OneOfIpv6AddrGlobalVariableOptionsDef2]
    remote_as: Union[OneOfAsNumOptionsDef1, OneOfAsNumOptionsDef2] = _field(
        metadata={"alias": "remoteAs"}
    )
    # Set IPv6 BGP address family
    address_family: Optional[List[MulticloudConnectionAddressFamily]] = _field(
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
    holdtime: Optional[Union[OneOfHoldtimeOptionsDef1, OneOfHoldtimeOptionsDef2]] = _field(
        default=None
    )
    if_name: Optional[
        Union[
            OneOfInterfaceNameOptionsDef1,
            OneOfInterfaceNameOptionsDef2,
            OneOfInterfaceNameOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ifName"})
    keepalive: Optional[Union[OneOfKeepaliveOptionsDef1, OneOfKeepaliveOptionsDef2]] = _field(
        default=None
    )
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
class Redistribute:
    protocol: Union[
        OneOfIpv4AddressFamilyRedistributeProtocolOptionsDef1,
        OneOfIpv4AddressFamilyRedistributeProtocolOptionsDef2,
    ]
    route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "routePolicy"})


@dataclass
class GlobalVrfMulticloudConnectionAddressFamily:
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
class MulticloudConnectionRedistribute:
    protocol: Union[
        OneOfIpv6AddressFamilyRedistributeProtocolOptionsDef1,
        OneOfIpv6AddressFamilyRedistributeProtocolOptionsDef2,
    ]
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
    redistribute: Optional[List[MulticloudConnectionRedistribute]] = _field(default=None)


@dataclass
class MulticloudConnectionOneOfIpV4AddressOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class Prefix:
    """
    Prefix
    """

    ip_address: Union[
        OneOfIpV4AddressOptionsDef1, MulticloudConnectionOneOfIpV4AddressOptionsDef2
    ] = _field(metadata={"alias": "ipAddress"})
    subnet_mask: Union[OneOfIpV4SubnetMaskOptionsDef1, OneOfIpV4SubnetMaskOptionsDef2] = _field(
        metadata={"alias": "subnetMask"}
    )


@dataclass
class Gateway:
    value: Optional[Any] = _field(default=None)


@dataclass
class OneOfIpv4NextHopAddressOptionsWithOutDefault1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpv4NextHopAddressOptionsWithOutDefault2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Union[Any, str]


@dataclass
class OneOfIpv4NextHopDistanceOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpv4NextHopDistanceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIpv4NextHopDistanceOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class NextHop:
    address: Union[
        OneOfIpv4NextHopAddressOptionsWithOutDefault1, OneOfIpv4NextHopAddressOptionsWithOutDefault2
    ]
    distance: Union[
        OneOfIpv4NextHopDistanceOptionsDef1,
        OneOfIpv4NextHopDistanceOptionsDef2,
        OneOfIpv4NextHopDistanceOptionsDef3,
    ]


@dataclass
class OneOfIpv4GatewayDistanceOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpv4GatewayDistanceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIpv4GatewayDistanceOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class Ipv4Route1:
    gateway: Gateway
    # IPv4 Route Gateway Next Hop
    next_hop: List[NextHop] = _field(metadata={"alias": "nextHop"})
    # Prefix
    prefix: Prefix
    distance: Optional[
        Union[
            OneOfIpv4GatewayDistanceOptionsDef1,
            OneOfIpv4GatewayDistanceOptionsDef2,
            OneOfIpv4GatewayDistanceOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class OneOfIpv4RouteGatewayOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Ipv4GatewayDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfIpv4RouteGatewayOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultIpv4GatewayDef  # pytype: disable=annotation-type-mismatch


@dataclass
class Ipv4Route2:
    gateway: Union[OneOfIpv4RouteGatewayOptionsDef1, OneOfIpv4RouteGatewayOptionsDef2]
    # Prefix
    prefix: Prefix
    distance: Optional[
        Union[
            OneOfIpv4GatewayDistanceOptionsDef1,
            OneOfIpv4GatewayDistanceOptionsDef2,
            OneOfIpv4GatewayDistanceOptionsDef3,
        ]
    ] = _field(default=None)
    # IPv4 Route Gateway Next Hop
    next_hop: Optional[List[NextHop]] = _field(default=None, metadata={"alias": "nextHop"})


@dataclass
class OneOfIpv6RoutePrefixOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpv6RoutePrefixOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfIpv6NextHopAddressOptionsWithOutDefault1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpv6NextHopAddressOptionsWithOutDefault2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfIpv6NextHopDistanceOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpv6NextHopDistanceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIpv6NextHopDistanceOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class MulticloudConnectionNextHop:
    address: Union[
        OneOfIpv6NextHopAddressOptionsWithOutDefault1, OneOfIpv6NextHopAddressOptionsWithOutDefault2
    ]
    distance: Union[
        OneOfIpv6NextHopDistanceOptionsDef1,
        OneOfIpv6NextHopDistanceOptionsDef2,
        OneOfIpv6NextHopDistanceOptionsDef3,
    ]


@dataclass
class NextHopContainer:
    # IPv6 Route Gateway Next Hop
    next_hop: Optional[List[MulticloudConnectionNextHop]] = _field(
        default=None, metadata={"alias": "nextHop"}
    )


@dataclass
class OneOfIpRoute1:
    next_hop_container: NextHopContainer = _field(metadata={"alias": "nextHopContainer"})


@dataclass
class OneOfIpv4V6RouteNull0OptionsWithoutVariable1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfIpv4V6RouteNull0OptionsWithoutVariable2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfIpRoute2:
    null0: Union[
        OneOfIpv4V6RouteNull0OptionsWithoutVariable1, OneOfIpv4V6RouteNull0OptionsWithoutVariable2
    ]


@dataclass
class OneOfIpv6RouteNatOptionsWithoutDefault1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpv6RouteNatOptionsWithoutDefault2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Ipv6RouteNatDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfIpRoute3:
    nat: Union[OneOfIpv6RouteNatOptionsWithoutDefault1, OneOfIpv6RouteNatOptionsWithoutDefault2]


@dataclass
class Ipv6Route:
    one_of_ip_route: Union[OneOfIpRoute1, OneOfIpRoute2, OneOfIpRoute3] = _field(
        metadata={"alias": "oneOfIpRoute"}
    )
    prefix: Union[OneOfIpv6RoutePrefixOptionsDef1, OneOfIpv6RoutePrefixOptionsDef2]


@dataclass
class MulticloudConnectionData:
    """
    Parameters for the new Connection
    """

    # Set IPv4 unicast BGP address family
    address_family: Optional[GlobalVrfMulticloudConnectionAddressFamily] = _field(
        default=None, metadata={"alias": "addressFamily"}
    )
    # IPv4 Static Route
    ipv4_route: Optional[List[Union[Ipv4Route1, Ipv4Route2]]] = _field(
        default=None, metadata={"alias": "ipv4Route"}
    )
    # Set BGP address family
    ipv6_address_family: Optional[Ipv6AddressFamily] = _field(
        default=None, metadata={"alias": "ipv6AddressFamily"}
    )
    # Set BGP IPv6 neighbors
    ipv6_neighbor: Optional[List[Ipv6Neighbor]] = _field(
        default=None, metadata={"alias": "ipv6Neighbor"}
    )
    # IPv6 Static Route
    ipv6_route: Optional[List[Ipv6Route]] = _field(default=None, metadata={"alias": "ipv6Route"})
    # Set BGP IPv4 neighbors
    neighbor: Optional[List[Neighbor]] = _field(default=None)


@dataclass
class Extensions:
    parcel_type: Union[
        OneOfExtensionsParcelTypeOptionsDef1, OneOfExtensionsParcelTypeOptionsDef2
    ] = _field(metadata={"alias": "parcelType"})
    #  Parameters for the new Connection
    data: Optional[MulticloudConnectionData] = _field(default=None)
    parcel_id: Optional[
        Union[OneOfExtensionsParcelIdOptionsDef1, OneOfExtensionsParcelIdOptionsDef2]
    ] = _field(default=None, metadata={"alias": "parcelId"})


@dataclass
class Data:
    connection_name: VariableOptionTypeObjectDef = _field(metadata={"alias": "connectionName"})
    # Extending Bgp Neighbors, Ip Routes, Interface Parcel Id reference and Route Policy for Transport Profile to build new Connections
    extensions: Optional[List[Extensions]] = _field(default=None)


@dataclass
class CreateTransportGlobalVrfAndMulticloudConnectionParcelAssociationPostRequest:
    """
    multi-cloud-connection profile parcel schema for POST request
    """

    data: Optional[Data] = _field(default=None)
    description: Optional[str] = _field(default=None)
    name: Optional[str] = _field(default=None)
