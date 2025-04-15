# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

VariableOptionTypeDef = Literal["variable"]

GlobalOptionTypeDef = Literal["global"]

DefaultOptionTypeDef = Literal["default"]

AdvertiseIpv4ProtocolDef = Literal[
    "aggregate", "bgp", "connected", "eigrp", "isis", "lisp", "network", "ospf", "ospfv3", "static"
]

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

RegionDef = Literal["access", "core", "core-and-access"]

Value = Literal["core-and-access"]

AdvertiseIpv6ProtocolDef = Literal["Aggregate", "BGP", "Connected", "Network", "OSPF", "Static"]

ProtocolSubTypeDef = Literal["External"]

Ipv6RouteNatDef = Literal["NAT64", "NAT66"]

ServiceTypeDef = Literal[
    "FW", "IDP", "IDS", "TE", "appqoe", "netsvc1", "netsvc2", "netsvc3", "netsvc4"
]

ServiceRouteDef = Literal["SIG", "SSE"]

VpnValue = Literal["SIG"]

NatDirectionDef = Literal["inside", "outside"]

NatPortForwardProtocolDef = Literal["TCP", "UDP"]

RouteLeakProtocolFromGlobalDef = Literal["bgp", "connected", "ospf", "static"]

RouteLeakRedistributeGlobalProtocolDef = Literal["bgp", "ospf"]

RouteLeakProtocolFromServiceDef = Literal["bgp", "connected", "ospf", "static"]

RouteLeakRedistributeServiceProtocolDef = Literal["bgp", "ospf"]

RouteImportFromProtocolDef = Literal["bgp", "connected", "ospf", "static"]

RouteImportFromRedistributeProtocolDef = Literal["bgp", "ospf"]

VpnAdvertiseIpv4ProtocolDef = Literal[
    "aggregate", "bgp", "connected", "eigrp", "isis", "lisp", "network", "ospf", "ospfv3", "static"
]

VpnRegionDef = Literal["access", "core", "core-and-access"]

VpnAdvertiseIpv6ProtocolDef = Literal["Aggregate", "BGP", "Connected", "Network", "OSPF", "Static"]

VpnProtocolSubTypeDef = Literal["External"]

LanVpnRegionDef = Literal["access", "core", "core-and-access"]

VpnServiceTypeDef = Literal[
    "FW", "IDP", "IDS", "TE", "appqoe", "netsvc1", "netsvc2", "netsvc3", "netsvc4"
]

VpnServiceRouteDef = Literal["SIG", "SSE"]

VpnNatDirectionDef = Literal["inside", "outside"]

VpnNatPortForwardProtocolDef = Literal["TCP", "UDP"]

LanVpnNatDirectionDef = Literal["inside", "outside"]

ServiceLanVpnNatDirectionDef = Literal["inside", "outside"]

VpnRouteLeakProtocolFromGlobalDef = Literal["bgp", "connected", "ospf", "static"]

VpnRouteLeakRedistributeGlobalProtocolDef = Literal["bgp", "ospf"]

VpnRouteLeakProtocolFromServiceDef = Literal["bgp", "connected", "ospf", "static"]

VpnRouteLeakRedistributeServiceProtocolDef = Literal["bgp", "ospf"]

VpnRouteImportFromProtocolDef = Literal["bgp", "connected", "ospf", "static"]

VpnRouteImportFromRedistributeProtocolDef = Literal["bgp", "ospf"]

LanVpnAdvertiseIpv4ProtocolDef = Literal[
    "aggregate", "bgp", "connected", "eigrp", "isis", "lisp", "network", "ospf", "ospfv3", "static"
]

ServiceLanVpnRegionDef = Literal["access", "core", "core-and-access"]

LanVpnAdvertiseIpv6ProtocolDef = Literal[
    "Aggregate", "BGP", "Connected", "Network", "OSPF", "Static"
]

LanVpnProtocolSubTypeDef = Literal["External"]

SdwanServiceLanVpnRegionDef = Literal["access", "core", "core-and-access"]

LanVpnServiceTypeDef = Literal[
    "FW", "IDP", "IDS", "TE", "appqoe", "netsvc1", "netsvc2", "netsvc3", "netsvc4"
]

LanVpnServiceRouteDef = Literal["SIG", "SSE"]

SdwanServiceLanVpnNatDirectionDef = Literal["inside", "outside"]

LanVpnNatPortForwardProtocolDef = Literal["TCP", "UDP"]

FeatureProfileSdwanServiceLanVpnNatDirectionDef = Literal["inside", "outside"]

V1FeatureProfileSdwanServiceLanVpnNatDirectionDef = Literal["inside", "outside"]

LanVpnRouteLeakProtocolFromGlobalDef = Literal["bgp", "connected", "ospf", "static"]

LanVpnRouteLeakRedistributeGlobalProtocolDef = Literal["bgp", "ospf"]

LanVpnRouteLeakProtocolFromServiceDef = Literal["bgp", "connected", "ospf", "static"]

LanVpnRouteLeakRedistributeServiceProtocolDef = Literal["bgp", "ospf"]

LanVpnRouteImportFromProtocolDef = Literal["bgp", "connected", "ospf", "static"]

LanVpnRouteImportFromRedistributeProtocolDef = Literal["bgp", "ospf"]


@dataclass
class OneOfVpnIdOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfVpnIdOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfVpnIdOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfVpnNameOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfVpnNameOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfVpnNameOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfOmpAdminIpv4OptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfOmpAdminIpv4OptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfOmpAdminIpv4OptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfOmpAdminIpv6OptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfOmpAdminIpv6OptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfOmpAdminIpv6OptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfPrimaryDnsAddressIpv4OptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfPrimaryDnsAddressIpv4OptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfPrimaryDnsAddressIpv4OptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfSecondaryDnsAddressIpv4OptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfSecondaryDnsAddressIpv4OptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfSecondaryDnsAddressIpv4OptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class DnsIpv4:
    primary_dns_address_ipv4: Optional[
        Union[
            OneOfPrimaryDnsAddressIpv4OptionsDef1,
            OneOfPrimaryDnsAddressIpv4OptionsDef2,
            OneOfPrimaryDnsAddressIpv4OptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "primaryDnsAddressIpv4"})
    secondary_dns_address_ipv4: Optional[
        Union[
            OneOfSecondaryDnsAddressIpv4OptionsDef1,
            OneOfSecondaryDnsAddressIpv4OptionsDef2,
            OneOfSecondaryDnsAddressIpv4OptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "secondaryDnsAddressIpv4"})


@dataclass
class OneOfPrimaryDnsAddressIpv6OptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfPrimaryDnsAddressIpv6OptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfPrimaryDnsAddressIpv6OptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfSecondaryDnsAddressIpv6OptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfSecondaryDnsAddressIpv6OptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfSecondaryDnsAddressIpv6OptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class DnsIpv6:
    primary_dns_address_ipv6: Optional[
        Union[
            OneOfPrimaryDnsAddressIpv6OptionsDef1,
            OneOfPrimaryDnsAddressIpv6OptionsDef2,
            OneOfPrimaryDnsAddressIpv6OptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "primaryDnsAddressIpv6"})
    secondary_dns_address_ipv6: Optional[
        Union[
            OneOfSecondaryDnsAddressIpv6OptionsDef1,
            OneOfSecondaryDnsAddressIpv6OptionsDef2,
            OneOfSecondaryDnsAddressIpv6OptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "secondaryDnsAddressIpv6"})


@dataclass
class OneOfHostNameOptionsWithoutDefault1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfHostNameOptionsWithoutDefault2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfListOfIpOptionsWithoutDefault1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfListOfIpOptionsWithoutDefault2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[Union[Any, Any]]


@dataclass
class NewHostMapping:
    host_name: Union[OneOfHostNameOptionsWithoutDefault1, OneOfHostNameOptionsWithoutDefault2] = (
        _field(metadata={"alias": "hostName"})
    )
    list_of_ip: Union[OneOfListOfIpOptionsWithoutDefault1, OneOfListOfIpOptionsWithoutDefault2] = (
        _field(metadata={"alias": "listOfIp"})
    )


@dataclass
class OneOfAdvertiseIpv4ProtocolOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAdvertiseIpv4ProtocolOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: AdvertiseIpv4ProtocolDef  # pytype: disable=annotation-type-mismatch


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
class OneOfRegionOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfRegionOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: RegionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfRegionOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Value  # pytype: disable=annotation-type-mismatch


@dataclass
class PrefixList:
    prefix: Ipv4AddressAndMaskDef
    aggregate_only: Optional[
        Union[
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef1,
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "aggregateOnly"})
    region: Optional[
        Union[OneOfRegionOptionsDef1, OneOfRegionOptionsDef2, OneOfRegionOptionsDef3]
    ] = _field(default=None)


@dataclass
class OmpAdvertiseIp4:
    omp_protocol: Union[
        OneOfAdvertiseIpv4ProtocolOptionsDef1, OneOfAdvertiseIpv4ProtocolOptionsDef2
    ] = _field(metadata={"alias": "ompProtocol"})
    # IPv4 Prefix List
    prefix_list: Optional[List[PrefixList]] = _field(default=None, metadata={"alias": "prefixList"})
    route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "routePolicy"})


@dataclass
class OneOfAdvertiseIpv6ProtocolOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAdvertiseIpv6ProtocolOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: AdvertiseIpv6ProtocolDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfAdvertiseIpv6ProtocolSubTypeOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAdvertiseIpv6ProtocolSubTypeOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ProtocolSubTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfAdvertiseIpv6ProtocolSubTypeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


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
class VpnPrefixList:
    prefix: Union[OneOfIpv6PrefixOptionsDef1, OneOfIpv6PrefixOptionsDef2]
    aggregate_only: Optional[
        Union[
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef1,
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "aggregateOnly"})
    region: Optional[
        Union[OneOfRegionOptionsDef1, OneOfRegionOptionsDef2, OneOfRegionOptionsDef3]
    ] = _field(default=None)


@dataclass
class OmpAdvertiseIpv6:
    omp_protocol: Union[
        OneOfAdvertiseIpv6ProtocolOptionsDef1, OneOfAdvertiseIpv6ProtocolOptionsDef2
    ] = _field(metadata={"alias": "ompProtocol"})
    # IPv6 Prefix List
    prefix_list: Optional[List[VpnPrefixList]] = _field(
        default=None, metadata={"alias": "prefixList"}
    )
    protocol_sub_type: Optional[
        Union[
            OneOfAdvertiseIpv6ProtocolSubTypeOptionsDef1,
            OneOfAdvertiseIpv6ProtocolSubTypeOptionsDef2,
            OneOfAdvertiseIpv6ProtocolSubTypeOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "protocolSubType"})
    route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "routePolicy"})


@dataclass
class Prefix:
    """
    Prefix
    """

    ip_address: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2] = _field(
        metadata={"alias": "ipAddress"}
    )
    subnet_mask: Union[OneOfIpV4SubnetMaskOptionsDef1, OneOfIpV4SubnetMaskOptionsDef2] = _field(
        metadata={"alias": "subnetMask"}
    )


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
class OneOfIpv4NextHopTrackerOptionsDef1:
    ref_id: RefId = _field(metadata={"alias": "refId"})


@dataclass
class OneOfIpv4NextHopTrackerOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class NextHopWithTracker:
    address: Union[
        OneOfIpv4NextHopAddressOptionsWithOutDefault1, OneOfIpv4NextHopAddressOptionsWithOutDefault2
    ]
    distance: Union[
        OneOfIpv4NextHopDistanceOptionsDef1,
        OneOfIpv4NextHopDistanceOptionsDef2,
        OneOfIpv4NextHopDistanceOptionsDef3,
    ]
    tracker: Union[OneOfIpv4NextHopTrackerOptionsDef1, OneOfIpv4NextHopTrackerOptionsDef2]


@dataclass
class NextHopContainer:
    # IPv4 Route Gateway Next Hop
    next_hop: Optional[List[NextHop]] = _field(default=None, metadata={"alias": "nextHop"})
    # IPv4 Route Gateway Next Hop with Tracker
    next_hop_with_tracker: Optional[List[NextHopWithTracker]] = _field(
        default=None, metadata={"alias": "nextHopWithTracker"}
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
class OneOfIpRoute2:
    null0: Union[
        OneOfIpv4V6RouteNull0OptionsWithoutVariable1, OneOfIpv4V6RouteNull0OptionsWithoutVariable2
    ]
    distance: Optional[
        Union[
            OneOfIpv4GatewayDistanceOptionsDef1,
            OneOfIpv4GatewayDistanceOptionsDef2,
            OneOfIpv4GatewayDistanceOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class OneOfIpv4RouteDhcpOptionsWithoutVariable1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfIpv4RouteDhcpOptionsWithoutVariable2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfIpRoute3:
    dhcp: Union[
        OneOfIpv4RouteDhcpOptionsWithoutVariable1, OneOfIpv4RouteDhcpOptionsWithoutVariable2
    ]


@dataclass
class OneOfIpv4RouteVpnOptionsWithoutVariable1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfIpv4RouteVpnOptionsWithoutVariable2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfIpRoute4:
    vpn: Union[OneOfIpv4RouteVpnOptionsWithoutVariable1, OneOfIpv4RouteVpnOptionsWithoutVariable2]


@dataclass
class InterfaceName1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class InterfaceName2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfIpv4NextHopAddressOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpv4NextHopAddressOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfIpv4NextHopAddressOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class VpnNextHop:
    address: Union[
        OneOfIpv4NextHopAddressOptionsDef1,
        OneOfIpv4NextHopAddressOptionsDef2,
        OneOfIpv4NextHopAddressOptionsDef3,
    ]
    distance: Union[
        OneOfIpv4NextHopDistanceOptionsDef1,
        OneOfIpv4NextHopDistanceOptionsDef2,
        OneOfIpv4NextHopDistanceOptionsDef3,
    ]


@dataclass
class IpStaticRouteInterface:
    interface_name: Union[InterfaceName1, InterfaceName2] = _field(
        metadata={"alias": "interfaceName"}
    )
    next_hop: Optional[List[VpnNextHop]] = _field(default=None, metadata={"alias": "nextHop"})


@dataclass
class InterfaceContainer:
    ip_static_route_interface: List[IpStaticRouteInterface] = _field(
        metadata={"alias": "ipStaticRouteInterface"}
    )


@dataclass
class OneOfIpRoute5:
    interface_container: InterfaceContainer = _field(metadata={"alias": "interfaceContainer"})


@dataclass
class Ipv4Route:
    one_of_ip_route: Union[
        OneOfIpRoute1, OneOfIpRoute2, OneOfIpRoute3, OneOfIpRoute4, OneOfIpRoute5
    ] = _field(metadata={"alias": "oneOfIpRoute"})
    # Prefix
    prefix: Prefix


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
class LanVpnNextHop:
    address: Union[
        OneOfIpv6NextHopAddressOptionsWithOutDefault1, OneOfIpv6NextHopAddressOptionsWithOutDefault2
    ]
    distance: Union[
        OneOfIpv6NextHopDistanceOptionsDef1,
        OneOfIpv6NextHopDistanceOptionsDef2,
        OneOfIpv6NextHopDistanceOptionsDef3,
    ]


@dataclass
class VpnNextHopContainer:
    # IPv6 Route Gateway Next Hop
    next_hop: Optional[List[LanVpnNextHop]] = _field(default=None, metadata={"alias": "nextHop"})


@dataclass
class VpnOneOfIpRoute1:
    next_hop_container: VpnNextHopContainer = _field(metadata={"alias": "nextHopContainer"})


@dataclass
class VpnOneOfIpRoute2:
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
class VpnOneOfIpRoute3:
    nat: Union[OneOfIpv6RouteNatOptionsWithoutDefault1, OneOfIpv6RouteNatOptionsWithoutDefault2]


@dataclass
class OneOfIpv6NextHopAddressOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpv6NextHopAddressOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfIpv6NextHopAddressOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class ServiceLanVpnNextHop:
    address: Union[
        OneOfIpv6NextHopAddressOptionsDef1,
        OneOfIpv6NextHopAddressOptionsDef2,
        OneOfIpv6NextHopAddressOptionsDef3,
    ]
    distance: Union[
        OneOfIpv6NextHopDistanceOptionsDef1,
        OneOfIpv6NextHopDistanceOptionsDef2,
        OneOfIpv6NextHopDistanceOptionsDef3,
    ]


@dataclass
class Ipv6StaticRouteInterface:
    interface_name: Union[InterfaceName1, InterfaceName2] = _field(
        metadata={"alias": "interfaceName"}
    )
    next_hop: Optional[List[ServiceLanVpnNextHop]] = _field(
        default=None, metadata={"alias": "nextHop"}
    )


@dataclass
class VpnInterfaceContainer:
    ipv6_static_route_interface: List[Ipv6StaticRouteInterface] = _field(
        metadata={"alias": "ipv6StaticRouteInterface"}
    )


@dataclass
class VpnOneOfIpRoute4:
    interface_container: VpnInterfaceContainer = _field(metadata={"alias": "interfaceContainer"})


@dataclass
class Ipv6Route:
    one_of_ip_route: Union[
        VpnOneOfIpRoute1, VpnOneOfIpRoute2, VpnOneOfIpRoute3, VpnOneOfIpRoute4
    ] = _field(metadata={"alias": "oneOfIpRoute"})
    prefix: Union[OneOfIpv6RoutePrefixOptionsDef1, OneOfIpv6RoutePrefixOptionsDef2]


@dataclass
class OneOfServiceTypeOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfServiceTypeOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ServiceTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfListOfIpV4OptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfListOfIpV4OptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class OneOfServiceTrackingOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfServiceTrackingOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfServiceTrackingOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class Service:
    ipv4_addresses: Union[OneOfListOfIpV4OptionsDef1, OneOfListOfIpV4OptionsDef2] = _field(
        metadata={"alias": "ipv4Addresses"}
    )
    service_type: Union[OneOfServiceTypeOptionsDef1, OneOfServiceTypeOptionsDef2] = _field(
        metadata={"alias": "serviceType"}
    )
    tracking: Union[
        OneOfServiceTrackingOptionsDef1,
        OneOfServiceTrackingOptionsDef2,
        OneOfServiceTrackingOptionsDef3,
    ]


@dataclass
class VpnPrefix:
    """
    Service Route Ip and Subnet Mask
    """

    ip_address: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2] = _field(
        metadata={"alias": "ipAddress"}
    )
    subnet_mask: Union[OneOfIpV4SubnetMaskOptionsDef1, OneOfIpV4SubnetMaskOptionsDef2] = _field(
        metadata={"alias": "subnetMask"}
    )


@dataclass
class OneOfServiceRouteServiceOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfServiceRouteServiceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ServiceRouteDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfServiceRouteServiceOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: VpnValue  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfDefaultVpnIdOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfSseInstanceOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfSseInstanceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ServiceRoute:
    # Service Route Ip and Subnet Mask
    prefix: VpnPrefix
    service: Union[
        OneOfServiceRouteServiceOptionsDef1,
        OneOfServiceRouteServiceOptionsDef2,
        OneOfServiceRouteServiceOptionsDef3,
    ]
    vpn: OneOfDefaultVpnIdOptionsDef
    sse_instance: Optional[Union[OneOfSseInstanceOptionsDef1, OneOfSseInstanceOptionsDef2]] = (
        _field(default=None, metadata={"alias": "sseInstance"})
    )


@dataclass
class LanVpnPrefix:
    """
    GRE Route Ip and Subnet Mask
    """

    ip_address: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2] = _field(
        metadata={"alias": "ipAddress"}
    )
    subnet_mask: Union[OneOfIpV4SubnetMaskOptionsDef1, OneOfIpV4SubnetMaskOptionsDef2] = _field(
        metadata={"alias": "subnetMask"}
    )


@dataclass
class OneOfGreRouteInterfaceOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfGreRouteInterfaceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class OneOfGreRouteInterfaceOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class GreRoute:
    interface: Union[
        OneOfGreRouteInterfaceOptionsDef1,
        OneOfGreRouteInterfaceOptionsDef2,
        OneOfGreRouteInterfaceOptionsDef3,
    ]
    # GRE Route Ip and Subnet Mask
    prefix: LanVpnPrefix
    vpn: OneOfDefaultVpnIdOptionsDef


@dataclass
class ServiceLanVpnPrefix:
    """
    IPSEC Route Ip and Subnet Mask
    """

    ip_address: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2] = _field(
        metadata={"alias": "ipAddress"}
    )
    subnet_mask: Union[OneOfIpV4SubnetMaskOptionsDef1, OneOfIpV4SubnetMaskOptionsDef2] = _field(
        metadata={"alias": "subnetMask"}
    )


@dataclass
class OneOfIpsecRouteInterfaceOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpsecRouteInterfaceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class OneOfIpsecRouteInterfaceOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class IpsecRoute:
    interface: Union[
        OneOfIpsecRouteInterfaceOptionsDef1,
        OneOfIpsecRouteInterfaceOptionsDef2,
        OneOfIpsecRouteInterfaceOptionsDef3,
    ]
    # IPSEC Route Ip and Subnet Mask
    prefix: ServiceLanVpnPrefix


@dataclass
class OneOfNatPoolNameOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfNatPoolNameOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNatPoolPrefixLengthOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfNatPoolPrefixLengthOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNatPoolRangeStartOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfNatPoolRangeStartOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfNatPoolRangeEndOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfNatPoolRangeEndOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfNatPoolOverloadOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfNatPoolOverloadOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfNatPoolOverloadOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfNatPoolDirectionOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfNatPoolDirectionOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: NatDirectionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class NatPool:
    direction: Union[OneOfNatPoolDirectionOptionsDef1, OneOfNatPoolDirectionOptionsDef2]
    nat_pool_name: Union[OneOfNatPoolNameOptionsDef1, OneOfNatPoolNameOptionsDef2] = _field(
        metadata={"alias": "natPoolName"}
    )
    overload: Union[
        OneOfNatPoolOverloadOptionsDef1,
        OneOfNatPoolOverloadOptionsDef2,
        OneOfNatPoolOverloadOptionsDef3,
    ]
    prefix_length: Union[
        OneOfNatPoolPrefixLengthOptionsDef1, OneOfNatPoolPrefixLengthOptionsDef2
    ] = _field(metadata={"alias": "prefixLength"})
    range_end: Union[OneOfNatPoolRangeEndOptionsDef1, OneOfNatPoolRangeEndOptionsDef2] = _field(
        metadata={"alias": "rangeEnd"}
    )
    range_start: Union[OneOfNatPoolRangeStartOptionsDef1, OneOfNatPoolRangeStartOptionsDef2] = (
        _field(metadata={"alias": "rangeStart"})
    )
    # Tracking object for NAT configuration
    tracking_object: Optional[Any] = _field(default=None, metadata={"alias": "trackingObject"})


@dataclass
class OneOfNatPoolNameInUseOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfNatPoolNameInUseOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNatPoolNameInUseOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfNatPortForwardSourcePortOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfNatPortForwardSourcePortOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNatPortForwardTranslatePortOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfNatPortForwardTranslatePortOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNatPortForwardSourceIpAddressOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfNatPortForwardSourceIpAddressOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfNatPortForwardTranslatedSourceIpAddressOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfNatPortForwardTranslatedSourceIpAddressOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfNatPortForwardProtocolOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfNatPortForwardProtocolOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: NatPortForwardProtocolDef  # pytype: disable=annotation-type-mismatch


@dataclass
class NatPortForward:
    nat_pool_name: Union[
        OneOfNatPoolNameInUseOptionsDef1,
        OneOfNatPoolNameInUseOptionsDef2,
        OneOfNatPoolNameInUseOptionsDef3,
    ] = _field(metadata={"alias": "natPoolName"})
    protocol: Union[OneOfNatPortForwardProtocolOptionsDef1, OneOfNatPortForwardProtocolOptionsDef2]
    source_ip: Union[
        OneOfNatPortForwardSourceIpAddressOptionsDef1, OneOfNatPortForwardSourceIpAddressOptionsDef2
    ] = _field(metadata={"alias": "sourceIp"})
    source_port: Union[
        OneOfNatPortForwardSourcePortOptionsDef1, OneOfNatPortForwardSourcePortOptionsDef2
    ] = _field(metadata={"alias": "sourcePort"})
    translate_port: Union[
        OneOfNatPortForwardTranslatePortOptionsDef1, OneOfNatPortForwardTranslatePortOptionsDef2
    ] = _field(metadata={"alias": "translatePort"})
    translated_source_ip: Union[
        OneOfNatPortForwardTranslatedSourceIpAddressOptionsDef1,
        OneOfNatPortForwardTranslatedSourceIpAddressOptionsDef2,
    ] = _field(metadata={"alias": "translatedSourceIp"})


@dataclass
class OneOfStaticNatSourceIpAddressOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfStaticNatSourceIpAddressOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfStaticNatTranslatedSourceIpAddressOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfStaticNatTranslatedSourceIpAddressOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfStaticNatDirectionOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfStaticNatDirectionOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: NatDirectionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class StaticNat:
    nat_pool_name: Optional[
        Union[
            OneOfNatPoolNameInUseOptionsDef1,
            OneOfNatPoolNameInUseOptionsDef2,
            OneOfNatPoolNameInUseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "natPoolName"})
    source_ip: Optional[
        Union[OneOfStaticNatSourceIpAddressOptionsDef1, OneOfStaticNatSourceIpAddressOptionsDef2]
    ] = _field(default=None, metadata={"alias": "sourceIp"})
    static_nat_direction: Optional[
        Union[OneOfStaticNatDirectionOptionsDef1, OneOfStaticNatDirectionOptionsDef2]
    ] = _field(default=None, metadata={"alias": "staticNatDirection"})
    # Tracking object for NAT configuration
    tracking_object: Optional[Any] = _field(default=None, metadata={"alias": "trackingObject"})
    translated_source_ip: Optional[
        Union[
            OneOfStaticNatTranslatedSourceIpAddressOptionsDef1,
            OneOfStaticNatTranslatedSourceIpAddressOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "translatedSourceIp"})


@dataclass
class OneOfStaticNatSubnetPrefixLengthOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfStaticNatSubnetPrefixLengthOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class StaticNatSubnet:
    prefix_length: Optional[
        Union[
            OneOfStaticNatSubnetPrefixLengthOptionsDef1, OneOfStaticNatSubnetPrefixLengthOptionsDef2
        ]
    ] = _field(default=None, metadata={"alias": "prefixLength"})
    source_ip_subnet: Optional[
        Union[OneOfStaticNatSourceIpAddressOptionsDef1, OneOfStaticNatSourceIpAddressOptionsDef2]
    ] = _field(default=None, metadata={"alias": "sourceIpSubnet"})
    static_nat_direction: Optional[
        Union[OneOfStaticNatDirectionOptionsDef1, OneOfStaticNatDirectionOptionsDef2]
    ] = _field(default=None, metadata={"alias": "staticNatDirection"})
    # Tracking object for NAT configuration
    tracking_object: Optional[Any] = _field(default=None, metadata={"alias": "trackingObject"})
    translated_source_ip_subnet: Optional[
        Union[
            OneOfStaticNatTranslatedSourceIpAddressOptionsDef1,
            OneOfStaticNatTranslatedSourceIpAddressOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "translatedSourceIpSubnet"})


@dataclass
class OneOfNat64V4PoolNameOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfNat64V4PoolNameOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfNat64V4PoolRangeStartOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfNat64V4PoolRangeStartOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfNat64V4PoolRangeEndOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfNat64V4PoolRangeEndOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfNat64V4PoolOverloadOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfNat64V4PoolOverloadOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfNat64V4PoolOverloadOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class Nat64V4Pool:
    nat64_v4_pool_name: Union[OneOfNat64V4PoolNameOptionsDef1, OneOfNat64V4PoolNameOptionsDef2] = (
        _field(metadata={"alias": "nat64V4PoolName"})
    )
    nat64_v4_pool_overload: Union[
        OneOfNat64V4PoolOverloadOptionsDef1,
        OneOfNat64V4PoolOverloadOptionsDef2,
        OneOfNat64V4PoolOverloadOptionsDef3,
    ] = _field(metadata={"alias": "nat64V4PoolOverload"})
    nat64_v4_pool_range_end: Union[
        OneOfNat64V4PoolRangeEndOptionsDef1, OneOfNat64V4PoolRangeEndOptionsDef2
    ] = _field(metadata={"alias": "nat64V4PoolRangeEnd"})
    nat64_v4_pool_range_start: Union[
        OneOfNat64V4PoolRangeStartOptionsDef1, OneOfNat64V4PoolRangeStartOptionsDef2
    ] = _field(metadata={"alias": "nat64V4PoolRangeStart"})


@dataclass
class OneOfRouteLeakFromGlobalProtocolOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfRouteLeakFromGlobalProtocolOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: RouteLeakProtocolFromGlobalDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfRouteLeakFromGlobalRedistributeProtocolOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfRouteLeakFromGlobalRedistributeProtocolOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: RouteLeakRedistributeGlobalProtocolDef  # pytype: disable=annotation-type-mismatch


@dataclass
class RedistributeToProtocol:
    protocol: Union[
        OneOfRouteLeakFromGlobalRedistributeProtocolOptionsDef1,
        OneOfRouteLeakFromGlobalRedistributeProtocolOptionsDef2,
    ]
    policy: Optional[Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]] = (
        _field(default=None)
    )


@dataclass
class RouteLeakFromGlobal:
    route_protocol: Union[
        OneOfRouteLeakFromGlobalProtocolOptionsDef1, OneOfRouteLeakFromGlobalProtocolOptionsDef2
    ] = _field(metadata={"alias": "routeProtocol"})
    # Redistribute Routes to specific Protocol on Service VPN
    redistribute_to_protocol: Optional[List[RedistributeToProtocol]] = _field(
        default=None, metadata={"alias": "redistributeToProtocol"}
    )
    route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "routePolicy"})


@dataclass
class OneOfRouteLeakFromServiceProtocolOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfRouteLeakFromServiceProtocolOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: RouteLeakProtocolFromServiceDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfRouteLeakFromServiceRedistributeProtocolOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfRouteLeakFromServiceRedistributeProtocolOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: RouteLeakRedistributeServiceProtocolDef  # pytype: disable=annotation-type-mismatch


@dataclass
class VpnRedistributeToProtocol:
    protocol: Union[
        OneOfRouteLeakFromServiceRedistributeProtocolOptionsDef1,
        OneOfRouteLeakFromServiceRedistributeProtocolOptionsDef2,
    ]
    policy: Optional[Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]] = (
        _field(default=None)
    )


@dataclass
class RouteLeakFromService:
    route_protocol: Union[
        OneOfRouteLeakFromServiceProtocolOptionsDef1, OneOfRouteLeakFromServiceProtocolOptionsDef2
    ] = _field(metadata={"alias": "routeProtocol"})
    # Redistribute Routes to specific Protocol on Global VPN
    redistribute_to_protocol: Optional[List[VpnRedistributeToProtocol]] = _field(
        default=None, metadata={"alias": "redistributeToProtocol"}
    )
    route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "routePolicy"})


@dataclass
class OneOfRouteImportFromSourceVpnOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfRouteImportFromSourceVpnOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfRouteImportFromProtocolOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfRouteImportFromProtocolOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: RouteImportFromProtocolDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfRouteImportFromRedistributeProtocolOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: RouteImportFromRedistributeProtocolDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfRouteImportFromRedistributeProtocolOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class LanVpnRedistributeToProtocol:
    protocol: Union[
        OneOfRouteImportFromRedistributeProtocolOptionsDef1,
        OneOfRouteImportFromRedistributeProtocolOptionsDef2,
    ]
    policy: Optional[Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]] = (
        _field(default=None)
    )


@dataclass
class RouteLeakBetweenServices:
    route_protocol: Union[
        OneOfRouteImportFromProtocolOptionsDef1, OneOfRouteImportFromProtocolOptionsDef2
    ] = _field(metadata={"alias": "routeProtocol"})
    source_vpn: Union[
        OneOfRouteImportFromSourceVpnOptionsDef1, OneOfRouteImportFromSourceVpnOptionsDef2
    ] = _field(metadata={"alias": "sourceVpn"})
    # Redistribute Route to specific Protocol on Current Service VPN
    redistribute_to_protocol: Optional[List[LanVpnRedistributeToProtocol]] = _field(
        default=None, metadata={"alias": "redistributeToProtocol"}
    )
    route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "routePolicy"})


@dataclass
class MplsVpnRouteTargetOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class MplsVpnRouteTargetOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class MplsVpnRouteTargetsDef:
    rt: Union[MplsVpnRouteTargetOptionsDef1, MplsVpnRouteTargetOptionsDef2]


@dataclass
class MplsVpnIpv4RouteTarget:
    export_rt_list: Optional[List[MplsVpnRouteTargetsDef]] = _field(
        default=None, metadata={"alias": "exportRtList"}
    )
    import_rt_list: Optional[List[MplsVpnRouteTargetsDef]] = _field(
        default=None, metadata={"alias": "importRtList"}
    )


@dataclass
class MplsVpnIpv6RouteTarget:
    export_rt_list: Optional[List[MplsVpnRouteTargetsDef]] = _field(
        default=None, metadata={"alias": "exportRtList"}
    )
    import_rt_list: Optional[List[MplsVpnRouteTargetsDef]] = _field(
        default=None, metadata={"alias": "importRtList"}
    )


@dataclass
class OneOfEnableSdraDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfEnableSdraDef2:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[bool] = _field(default=None)


@dataclass
class VpnData:
    name: Union[OneOfVpnNameOptionsDef1, OneOfVpnNameOptionsDef2, OneOfVpnNameOptionsDef3]
    vpn_id: Union[OneOfVpnIdOptionsDef1, OneOfVpnIdOptionsDef2, OneOfVpnIdOptionsDef3] = _field(
        metadata={"alias": "vpnId"}
    )
    dns_ipv4: Optional[DnsIpv4] = _field(default=None, metadata={"alias": "dnsIpv4"})
    dns_ipv6: Optional[DnsIpv6] = _field(default=None, metadata={"alias": "dnsIpv6"})
    enable_sdra: Optional[Union[OneOfEnableSdraDef1, OneOfEnableSdraDef2]] = _field(
        default=None, metadata={"alias": "enableSdra"}
    )
    # IPv4 Static GRE Route
    gre_route: Optional[List[GreRoute]] = _field(default=None, metadata={"alias": "greRoute"})
    # IPv4 Static IPSEC Route
    ipsec_route: Optional[List[IpsecRoute]] = _field(default=None, metadata={"alias": "ipsecRoute"})
    # IPv4 Static Route
    ipv4_route: Optional[List[Ipv4Route]] = _field(default=None, metadata={"alias": "ipv4Route"})
    # IPv6 Static Route
    ipv6_route: Optional[List[Ipv6Route]] = _field(default=None, metadata={"alias": "ipv6Route"})
    mpls_vpn_ipv4_route_target: Optional[MplsVpnIpv4RouteTarget] = _field(
        default=None, metadata={"alias": "mplsVpnIpv4RouteTarget"}
    )
    mpls_vpn_ipv6_route_target: Optional[MplsVpnIpv6RouteTarget] = _field(
        default=None, metadata={"alias": "mplsVpnIpv6RouteTarget"}
    )
    # NAT64 V4 Pool
    nat64_v4_pool: Optional[List[Nat64V4Pool]] = _field(
        default=None, metadata={"alias": "nat64V4Pool"}
    )
    # NAT Pool
    nat_pool: Optional[List[NatPool]] = _field(default=None, metadata={"alias": "natPool"})
    # NAT Port Forward
    nat_port_forward: Optional[List[NatPortForward]] = _field(
        default=None, metadata={"alias": "natPortForward"}
    )
    new_host_mapping: Optional[List[NewHostMapping]] = _field(
        default=None, metadata={"alias": "newHostMapping"}
    )
    omp_admin_distance: Optional[
        Union[
            OneOfOmpAdminIpv4OptionsDef1, OneOfOmpAdminIpv4OptionsDef2, OneOfOmpAdminIpv4OptionsDef3
        ]
    ] = _field(default=None, metadata={"alias": "ompAdminDistance"})
    omp_admin_distance_ipv6: Optional[
        Union[
            OneOfOmpAdminIpv6OptionsDef1, OneOfOmpAdminIpv6OptionsDef2, OneOfOmpAdminIpv6OptionsDef3
        ]
    ] = _field(default=None, metadata={"alias": "ompAdminDistanceIpv6"})
    # OMP Advertise IPv4
    omp_advertise_ip4: Optional[List[OmpAdvertiseIp4]] = _field(
        default=None, metadata={"alias": "ompAdvertiseIp4"}
    )
    # OMP Advertise IPv6
    omp_advertise_ipv6: Optional[List[OmpAdvertiseIpv6]] = _field(
        default=None, metadata={"alias": "ompAdvertiseIpv6"}
    )
    # Enable route leak from another Service VPN to current Service VPN
    route_leak_between_services: Optional[List[RouteLeakBetweenServices]] = _field(
        default=None, metadata={"alias": "routeLeakBetweenServices"}
    )
    # Enable route leaking from Global to Service VPN
    route_leak_from_global: Optional[List[RouteLeakFromGlobal]] = _field(
        default=None, metadata={"alias": "routeLeakFromGlobal"}
    )
    # Enable route leaking from Service to Global VPN
    route_leak_from_service: Optional[List[RouteLeakFromService]] = _field(
        default=None, metadata={"alias": "routeLeakFromService"}
    )
    # Service
    service: Optional[List[Service]] = _field(default=None)
    # Service
    service_route: Optional[List[ServiceRoute]] = _field(
        default=None, metadata={"alias": "serviceRoute"}
    )
    # Static NAT Rules
    static_nat: Optional[List[StaticNat]] = _field(default=None, metadata={"alias": "staticNat"})
    # Static NAT Subnet Rules
    static_nat_subnet: Optional[List[StaticNatSubnet]] = _field(
        default=None, metadata={"alias": "staticNatSubnet"}
    )


@dataclass
class Payload:
    """
    LAN VPN feature schema for POST request
    """

    data: VpnData
    name: str
    # Set the Feature description
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
    # LAN VPN feature schema for POST request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdwanServiceLanVpnPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateLanVpnProfileParcelForServicePostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class LanVpnData:
    name: Union[OneOfVpnNameOptionsDef1, OneOfVpnNameOptionsDef2, OneOfVpnNameOptionsDef3]
    vpn_id: Union[OneOfVpnIdOptionsDef1, OneOfVpnIdOptionsDef2, OneOfVpnIdOptionsDef3] = _field(
        metadata={"alias": "vpnId"}
    )
    dns_ipv4: Optional[DnsIpv4] = _field(default=None, metadata={"alias": "dnsIpv4"})
    dns_ipv6: Optional[DnsIpv6] = _field(default=None, metadata={"alias": "dnsIpv6"})
    enable_sdra: Optional[Union[OneOfEnableSdraDef1, OneOfEnableSdraDef2]] = _field(
        default=None, metadata={"alias": "enableSdra"}
    )
    # IPv4 Static GRE Route
    gre_route: Optional[List[GreRoute]] = _field(default=None, metadata={"alias": "greRoute"})
    # IPv4 Static IPSEC Route
    ipsec_route: Optional[List[IpsecRoute]] = _field(default=None, metadata={"alias": "ipsecRoute"})
    # IPv4 Static Route
    ipv4_route: Optional[List[Ipv4Route]] = _field(default=None, metadata={"alias": "ipv4Route"})
    # IPv6 Static Route
    ipv6_route: Optional[List[Ipv6Route]] = _field(default=None, metadata={"alias": "ipv6Route"})
    mpls_vpn_ipv4_route_target: Optional[MplsVpnIpv4RouteTarget] = _field(
        default=None, metadata={"alias": "mplsVpnIpv4RouteTarget"}
    )
    mpls_vpn_ipv6_route_target: Optional[MplsVpnIpv6RouteTarget] = _field(
        default=None, metadata={"alias": "mplsVpnIpv6RouteTarget"}
    )
    # NAT64 V4 Pool
    nat64_v4_pool: Optional[List[Nat64V4Pool]] = _field(
        default=None, metadata={"alias": "nat64V4Pool"}
    )
    # NAT Pool
    nat_pool: Optional[List[NatPool]] = _field(default=None, metadata={"alias": "natPool"})
    # NAT Port Forward
    nat_port_forward: Optional[List[NatPortForward]] = _field(
        default=None, metadata={"alias": "natPortForward"}
    )
    new_host_mapping: Optional[List[NewHostMapping]] = _field(
        default=None, metadata={"alias": "newHostMapping"}
    )
    omp_admin_distance: Optional[
        Union[
            OneOfOmpAdminIpv4OptionsDef1, OneOfOmpAdminIpv4OptionsDef2, OneOfOmpAdminIpv4OptionsDef3
        ]
    ] = _field(default=None, metadata={"alias": "ompAdminDistance"})
    omp_admin_distance_ipv6: Optional[
        Union[
            OneOfOmpAdminIpv6OptionsDef1, OneOfOmpAdminIpv6OptionsDef2, OneOfOmpAdminIpv6OptionsDef3
        ]
    ] = _field(default=None, metadata={"alias": "ompAdminDistanceIpv6"})
    # OMP Advertise IPv4
    omp_advertise_ip4: Optional[List[OmpAdvertiseIp4]] = _field(
        default=None, metadata={"alias": "ompAdvertiseIp4"}
    )
    # OMP Advertise IPv6
    omp_advertise_ipv6: Optional[List[OmpAdvertiseIpv6]] = _field(
        default=None, metadata={"alias": "ompAdvertiseIpv6"}
    )
    # Enable route leak from another Service VPN to current Service VPN
    route_leak_between_services: Optional[List[RouteLeakBetweenServices]] = _field(
        default=None, metadata={"alias": "routeLeakBetweenServices"}
    )
    # Enable route leaking from Global to Service VPN
    route_leak_from_global: Optional[List[RouteLeakFromGlobal]] = _field(
        default=None, metadata={"alias": "routeLeakFromGlobal"}
    )
    # Enable route leaking from Service to Global VPN
    route_leak_from_service: Optional[List[RouteLeakFromService]] = _field(
        default=None, metadata={"alias": "routeLeakFromService"}
    )
    # Service
    service: Optional[List[Service]] = _field(default=None)
    # Service
    service_route: Optional[List[ServiceRoute]] = _field(
        default=None, metadata={"alias": "serviceRoute"}
    )
    # Static NAT Rules
    static_nat: Optional[List[StaticNat]] = _field(default=None, metadata={"alias": "staticNat"})
    # Static NAT Subnet Rules
    static_nat_subnet: Optional[List[StaticNatSubnet]] = _field(
        default=None, metadata={"alias": "staticNatSubnet"}
    )


@dataclass
class CreateLanVpnProfileParcelForServicePostRequest:
    """
    LAN VPN feature schema for POST request
    """

    data: LanVpnData
    name: str
    # Set the Feature description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class VpnOneOfVpnIdOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VpnOneOfOmpAdminIpv4OptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VpnOneOfOmpAdminIpv6OptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VpnOneOfPrimaryDnsAddressIpv4OptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VpnOneOfSecondaryDnsAddressIpv4OptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VpnDnsIpv4:
    primary_dns_address_ipv4: Optional[
        Union[
            OneOfPrimaryDnsAddressIpv4OptionsDef1,
            VpnOneOfPrimaryDnsAddressIpv4OptionsDef2,
            OneOfPrimaryDnsAddressIpv4OptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "primaryDnsAddressIpv4"})
    secondary_dns_address_ipv4: Optional[
        Union[
            OneOfSecondaryDnsAddressIpv4OptionsDef1,
            VpnOneOfSecondaryDnsAddressIpv4OptionsDef2,
            OneOfSecondaryDnsAddressIpv4OptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "secondaryDnsAddressIpv4"})


@dataclass
class VpnDnsIpv6:
    primary_dns_address_ipv6: Optional[
        Union[
            OneOfPrimaryDnsAddressIpv6OptionsDef1,
            OneOfPrimaryDnsAddressIpv6OptionsDef2,
            OneOfPrimaryDnsAddressIpv6OptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "primaryDnsAddressIpv6"})
    secondary_dns_address_ipv6: Optional[
        Union[
            OneOfSecondaryDnsAddressIpv6OptionsDef1,
            OneOfSecondaryDnsAddressIpv6OptionsDef2,
            OneOfSecondaryDnsAddressIpv6OptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "secondaryDnsAddressIpv6"})


@dataclass
class VpnOneOfAdvertiseIpv4ProtocolOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: VpnAdvertiseIpv4ProtocolDef  # pytype: disable=annotation-type-mismatch


@dataclass
class VpnOneOfRegionOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: VpnRegionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class VpnOneOfRegionOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Optional[Value] = _field(default=None)


@dataclass
class LanVpnPrefixList:
    prefix: Ipv4AddressAndMaskDef
    aggregate_only: Optional[
        Union[
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef1,
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "aggregateOnly"})
    region: Optional[
        Union[OneOfRegionOptionsDef1, VpnOneOfRegionOptionsDef2, VpnOneOfRegionOptionsDef3]
    ] = _field(default=None)


@dataclass
class VpnOmpAdvertiseIp4:
    omp_protocol: Union[
        OneOfAdvertiseIpv4ProtocolOptionsDef1, VpnOneOfAdvertiseIpv4ProtocolOptionsDef2
    ] = _field(metadata={"alias": "ompProtocol"})
    # IPv4 Prefix List
    prefix_list: Optional[List[LanVpnPrefixList]] = _field(
        default=None, metadata={"alias": "prefixList"}
    )
    route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "routePolicy"})


@dataclass
class VpnOneOfAdvertiseIpv6ProtocolOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: VpnAdvertiseIpv6ProtocolDef  # pytype: disable=annotation-type-mismatch


@dataclass
class VpnOneOfAdvertiseIpv6ProtocolSubTypeOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: VpnProtocolSubTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class LanVpnOneOfRegionOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: LanVpnRegionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class LanVpnOneOfRegionOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Optional[Value] = _field(default=None)


@dataclass
class ServiceLanVpnPrefixList:
    prefix: Union[OneOfIpv6PrefixOptionsDef1, OneOfIpv6PrefixOptionsDef2]
    aggregate_only: Optional[
        Union[
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef1,
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "aggregateOnly"})
    region: Optional[
        Union[OneOfRegionOptionsDef1, LanVpnOneOfRegionOptionsDef2, LanVpnOneOfRegionOptionsDef3]
    ] = _field(default=None)


@dataclass
class VpnOmpAdvertiseIpv6:
    omp_protocol: Union[
        OneOfAdvertiseIpv6ProtocolOptionsDef1, VpnOneOfAdvertiseIpv6ProtocolOptionsDef2
    ] = _field(metadata={"alias": "ompProtocol"})
    # IPv6 Prefix List
    prefix_list: Optional[List[ServiceLanVpnPrefixList]] = _field(
        default=None, metadata={"alias": "prefixList"}
    )
    protocol_sub_type: Optional[
        Union[
            OneOfAdvertiseIpv6ProtocolSubTypeOptionsDef1,
            VpnOneOfAdvertiseIpv6ProtocolSubTypeOptionsDef2,
            OneOfAdvertiseIpv6ProtocolSubTypeOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "protocolSubType"})
    route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "routePolicy"})


@dataclass
class VpnOneOfIpv4NextHopDistanceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SdwanServiceLanVpnNextHop:
    address: Union[
        OneOfIpv4NextHopAddressOptionsWithOutDefault1, OneOfIpv4NextHopAddressOptionsWithOutDefault2
    ]
    distance: Union[
        OneOfIpv4NextHopDistanceOptionsDef1,
        VpnOneOfIpv4NextHopDistanceOptionsDef2,
        OneOfIpv4NextHopDistanceOptionsDef3,
    ]


@dataclass
class LanVpnOneOfIpv4NextHopDistanceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VpnNextHopWithTracker:
    address: Union[
        OneOfIpv4NextHopAddressOptionsWithOutDefault1, OneOfIpv4NextHopAddressOptionsWithOutDefault2
    ]
    distance: Union[
        OneOfIpv4NextHopDistanceOptionsDef1,
        LanVpnOneOfIpv4NextHopDistanceOptionsDef2,
        OneOfIpv4NextHopDistanceOptionsDef3,
    ]
    tracker: Union[OneOfIpv4NextHopTrackerOptionsDef1, OneOfIpv4NextHopTrackerOptionsDef2]


@dataclass
class LanVpnNextHopContainer:
    # IPv4 Route Gateway Next Hop
    next_hop: Optional[List[SdwanServiceLanVpnNextHop]] = _field(
        default=None, metadata={"alias": "nextHop"}
    )
    # IPv4 Route Gateway Next Hop with Tracker
    next_hop_with_tracker: Optional[List[VpnNextHopWithTracker]] = _field(
        default=None, metadata={"alias": "nextHopWithTracker"}
    )


@dataclass
class LanVpnOneOfIpRoute1:
    next_hop_container: LanVpnNextHopContainer = _field(metadata={"alias": "nextHopContainer"})


@dataclass
class VpnOneOfIpv4GatewayDistanceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class LanVpnOneOfIpRoute2:
    null0: Union[
        OneOfIpv4V6RouteNull0OptionsWithoutVariable1, OneOfIpv4V6RouteNull0OptionsWithoutVariable2
    ]
    distance: Optional[
        Union[
            OneOfIpv4GatewayDistanceOptionsDef1,
            VpnOneOfIpv4GatewayDistanceOptionsDef2,
            OneOfIpv4GatewayDistanceOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class VpnOneOfIpv4NextHopAddressOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ServiceLanVpnOneOfIpv4NextHopDistanceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class FeatureProfileSdwanServiceLanVpnNextHop:
    address: Union[
        OneOfIpv4NextHopAddressOptionsDef1,
        VpnOneOfIpv4NextHopAddressOptionsDef2,
        OneOfIpv4NextHopAddressOptionsDef3,
    ]
    distance: Union[
        OneOfIpv4NextHopDistanceOptionsDef1,
        ServiceLanVpnOneOfIpv4NextHopDistanceOptionsDef2,
        OneOfIpv4NextHopDistanceOptionsDef3,
    ]


@dataclass
class VpnIpStaticRouteInterface:
    interface_name: Union[InterfaceName1, InterfaceName2] = _field(
        metadata={"alias": "interfaceName"}
    )
    next_hop: Optional[List[FeatureProfileSdwanServiceLanVpnNextHop]] = _field(
        default=None, metadata={"alias": "nextHop"}
    )


@dataclass
class LanVpnInterfaceContainer:
    ip_static_route_interface: List[VpnIpStaticRouteInterface] = _field(
        metadata={"alias": "ipStaticRouteInterface"}
    )


@dataclass
class VpnOneOfIpRoute5:
    interface_container: LanVpnInterfaceContainer = _field(metadata={"alias": "interfaceContainer"})


@dataclass
class VpnIpv4Route:
    one_of_ip_route: Union[
        LanVpnOneOfIpRoute1, LanVpnOneOfIpRoute2, OneOfIpRoute3, OneOfIpRoute4, VpnOneOfIpRoute5
    ] = _field(metadata={"alias": "oneOfIpRoute"})
    # Prefix
    prefix: Prefix


@dataclass
class VpnOneOfIpv6NextHopDistanceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class V1FeatureProfileSdwanServiceLanVpnNextHop:
    address: Union[
        OneOfIpv6NextHopAddressOptionsWithOutDefault1, OneOfIpv6NextHopAddressOptionsWithOutDefault2
    ]
    distance: Union[
        OneOfIpv6NextHopDistanceOptionsDef1,
        VpnOneOfIpv6NextHopDistanceOptionsDef2,
        OneOfIpv6NextHopDistanceOptionsDef3,
    ]


@dataclass
class ServiceLanVpnNextHopContainer:
    # IPv6 Route Gateway Next Hop
    next_hop: Optional[List[V1FeatureProfileSdwanServiceLanVpnNextHop]] = _field(
        default=None, metadata={"alias": "nextHop"}
    )


@dataclass
class ServiceLanVpnOneOfIpRoute1:
    next_hop_container: ServiceLanVpnNextHopContainer = _field(
        metadata={"alias": "nextHopContainer"}
    )


@dataclass
class ServiceLanVpnOneOfIpRoute2:
    null0: Union[
        OneOfIpv4V6RouteNull0OptionsWithoutVariable1, OneOfIpv4V6RouteNull0OptionsWithoutVariable2
    ]


@dataclass
class LanVpnOneOfIpRoute3:
    nat: Union[OneOfIpv6RouteNatOptionsWithoutDefault1, OneOfIpv6RouteNatOptionsWithoutDefault2]


@dataclass
class LanVpnOneOfIpv6NextHopDistanceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class NextHop1:
    address: Union[
        OneOfIpv6NextHopAddressOptionsDef1,
        OneOfIpv6NextHopAddressOptionsDef2,
        OneOfIpv6NextHopAddressOptionsDef3,
    ]
    distance: Union[
        OneOfIpv6NextHopDistanceOptionsDef1,
        LanVpnOneOfIpv6NextHopDistanceOptionsDef2,
        OneOfIpv6NextHopDistanceOptionsDef3,
    ]


@dataclass
class VpnIpv6StaticRouteInterface:
    interface_name: Union[InterfaceName1, InterfaceName2] = _field(
        metadata={"alias": "interfaceName"}
    )
    next_hop: Optional[List[NextHop1]] = _field(default=None, metadata={"alias": "nextHop"})


@dataclass
class ServiceLanVpnInterfaceContainer:
    ipv6_static_route_interface: List[VpnIpv6StaticRouteInterface] = _field(
        metadata={"alias": "ipv6StaticRouteInterface"}
    )


@dataclass
class LanVpnOneOfIpRoute4:
    interface_container: ServiceLanVpnInterfaceContainer = _field(
        metadata={"alias": "interfaceContainer"}
    )


@dataclass
class VpnIpv6Route:
    one_of_ip_route: Union[
        ServiceLanVpnOneOfIpRoute1,
        ServiceLanVpnOneOfIpRoute2,
        LanVpnOneOfIpRoute3,
        LanVpnOneOfIpRoute4,
    ] = _field(metadata={"alias": "oneOfIpRoute"})
    prefix: Union[OneOfIpv6RoutePrefixOptionsDef1, OneOfIpv6RoutePrefixOptionsDef2]


@dataclass
class VpnOneOfServiceTypeOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: VpnServiceTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class VpnOneOfListOfIpV4OptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class VpnService:
    ipv4_addresses: Union[OneOfListOfIpV4OptionsDef1, VpnOneOfListOfIpV4OptionsDef2] = _field(
        metadata={"alias": "ipv4Addresses"}
    )
    service_type: Union[OneOfServiceTypeOptionsDef1, VpnOneOfServiceTypeOptionsDef2] = _field(
        metadata={"alias": "serviceType"}
    )
    tracking: Union[
        OneOfServiceTrackingOptionsDef1,
        OneOfServiceTrackingOptionsDef2,
        OneOfServiceTrackingOptionsDef3,
    ]


@dataclass
class SdwanServiceLanVpnPrefix:
    """
    Service Route Ip and Subnet Mask
    """

    ip_address: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2] = _field(
        metadata={"alias": "ipAddress"}
    )
    subnet_mask: Union[OneOfIpV4SubnetMaskOptionsDef1, OneOfIpV4SubnetMaskOptionsDef2] = _field(
        metadata={"alias": "subnetMask"}
    )


@dataclass
class VpnOneOfServiceRouteServiceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: VpnServiceRouteDef  # pytype: disable=annotation-type-mismatch


@dataclass
class VpnOneOfSseInstanceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VpnServiceRoute:
    # Service Route Ip and Subnet Mask
    prefix: SdwanServiceLanVpnPrefix
    service: Union[
        OneOfServiceRouteServiceOptionsDef1,
        VpnOneOfServiceRouteServiceOptionsDef2,
        OneOfServiceRouteServiceOptionsDef3,
    ]
    vpn: OneOfDefaultVpnIdOptionsDef
    sse_instance: Optional[Union[OneOfSseInstanceOptionsDef1, VpnOneOfSseInstanceOptionsDef2]] = (
        _field(default=None, metadata={"alias": "sseInstance"})
    )


@dataclass
class FeatureProfileSdwanServiceLanVpnPrefix:
    """
    GRE Route Ip and Subnet Mask
    """

    ip_address: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2] = _field(
        metadata={"alias": "ipAddress"}
    )
    subnet_mask: Union[OneOfIpV4SubnetMaskOptionsDef1, OneOfIpV4SubnetMaskOptionsDef2] = _field(
        metadata={"alias": "subnetMask"}
    )


@dataclass
class VpnOneOfGreRouteInterfaceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class VpnGreRoute:
    interface: Union[
        OneOfGreRouteInterfaceOptionsDef1,
        VpnOneOfGreRouteInterfaceOptionsDef2,
        OneOfGreRouteInterfaceOptionsDef3,
    ]
    # GRE Route Ip and Subnet Mask
    prefix: FeatureProfileSdwanServiceLanVpnPrefix
    vpn: OneOfDefaultVpnIdOptionsDef


@dataclass
class V1FeatureProfileSdwanServiceLanVpnPrefix:
    """
    IPSEC Route Ip and Subnet Mask
    """

    ip_address: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2] = _field(
        metadata={"alias": "ipAddress"}
    )
    subnet_mask: Union[OneOfIpV4SubnetMaskOptionsDef1, OneOfIpV4SubnetMaskOptionsDef2] = _field(
        metadata={"alias": "subnetMask"}
    )


@dataclass
class VpnOneOfIpsecRouteInterfaceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class VpnIpsecRoute:
    interface: Union[
        OneOfIpsecRouteInterfaceOptionsDef1,
        VpnOneOfIpsecRouteInterfaceOptionsDef2,
        OneOfIpsecRouteInterfaceOptionsDef3,
    ]
    # IPSEC Route Ip and Subnet Mask
    prefix: V1FeatureProfileSdwanServiceLanVpnPrefix


@dataclass
class VpnOneOfNatPoolNameOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VpnOneOfNatPoolPrefixLengthOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VpnOneOfNatPoolRangeStartOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VpnOneOfNatPoolRangeEndOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VpnOneOfNatPoolDirectionOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: VpnNatDirectionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class VpnNatPool:
    direction: Union[OneOfNatPoolDirectionOptionsDef1, VpnOneOfNatPoolDirectionOptionsDef2]
    nat_pool_name: Union[OneOfNatPoolNameOptionsDef1, VpnOneOfNatPoolNameOptionsDef2] = _field(
        metadata={"alias": "natPoolName"}
    )
    overload: Union[
        OneOfNatPoolOverloadOptionsDef1,
        OneOfNatPoolOverloadOptionsDef2,
        OneOfNatPoolOverloadOptionsDef3,
    ]
    prefix_length: Union[
        OneOfNatPoolPrefixLengthOptionsDef1, VpnOneOfNatPoolPrefixLengthOptionsDef2
    ] = _field(metadata={"alias": "prefixLength"})
    range_end: Union[OneOfNatPoolRangeEndOptionsDef1, VpnOneOfNatPoolRangeEndOptionsDef2] = _field(
        metadata={"alias": "rangeEnd"}
    )
    range_start: Union[OneOfNatPoolRangeStartOptionsDef1, VpnOneOfNatPoolRangeStartOptionsDef2] = (
        _field(metadata={"alias": "rangeStart"})
    )
    # Tracking object for NAT configuration
    tracking_object: Optional[Any] = _field(default=None, metadata={"alias": "trackingObject"})


@dataclass
class VpnOneOfNatPoolNameInUseOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VpnOneOfNatPortForwardSourcePortOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VpnOneOfNatPortForwardTranslatePortOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VpnOneOfNatPortForwardSourceIpAddressOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VpnOneOfNatPortForwardTranslatedSourceIpAddressOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VpnOneOfNatPortForwardProtocolOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: VpnNatPortForwardProtocolDef  # pytype: disable=annotation-type-mismatch


@dataclass
class VpnNatPortForward:
    nat_pool_name: Union[
        OneOfNatPoolNameInUseOptionsDef1,
        VpnOneOfNatPoolNameInUseOptionsDef2,
        OneOfNatPoolNameInUseOptionsDef3,
    ] = _field(metadata={"alias": "natPoolName"})
    protocol: Union[
        OneOfNatPortForwardProtocolOptionsDef1, VpnOneOfNatPortForwardProtocolOptionsDef2
    ]
    source_ip: Union[
        OneOfNatPortForwardSourceIpAddressOptionsDef1,
        VpnOneOfNatPortForwardSourceIpAddressOptionsDef2,
    ] = _field(metadata={"alias": "sourceIp"})
    source_port: Union[
        OneOfNatPortForwardSourcePortOptionsDef1, VpnOneOfNatPortForwardSourcePortOptionsDef2
    ] = _field(metadata={"alias": "sourcePort"})
    translate_port: Union[
        OneOfNatPortForwardTranslatePortOptionsDef1, VpnOneOfNatPortForwardTranslatePortOptionsDef2
    ] = _field(metadata={"alias": "translatePort"})
    translated_source_ip: Union[
        OneOfNatPortForwardTranslatedSourceIpAddressOptionsDef1,
        VpnOneOfNatPortForwardTranslatedSourceIpAddressOptionsDef2,
    ] = _field(metadata={"alias": "translatedSourceIp"})


@dataclass
class LanVpnOneOfNatPoolNameInUseOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VpnOneOfStaticNatSourceIpAddressOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VpnOneOfStaticNatTranslatedSourceIpAddressOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VpnOneOfStaticNatDirectionOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: LanVpnNatDirectionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class VpnStaticNat:
    nat_pool_name: Optional[
        Union[
            OneOfNatPoolNameInUseOptionsDef1,
            LanVpnOneOfNatPoolNameInUseOptionsDef2,
            OneOfNatPoolNameInUseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "natPoolName"})
    source_ip: Optional[
        Union[OneOfStaticNatSourceIpAddressOptionsDef1, VpnOneOfStaticNatSourceIpAddressOptionsDef2]
    ] = _field(default=None, metadata={"alias": "sourceIp"})
    static_nat_direction: Optional[
        Union[OneOfStaticNatDirectionOptionsDef1, VpnOneOfStaticNatDirectionOptionsDef2]
    ] = _field(default=None, metadata={"alias": "staticNatDirection"})
    # Tracking object for NAT configuration
    tracking_object: Optional[Any] = _field(default=None, metadata={"alias": "trackingObject"})
    translated_source_ip: Optional[
        Union[
            OneOfStaticNatTranslatedSourceIpAddressOptionsDef1,
            VpnOneOfStaticNatTranslatedSourceIpAddressOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "translatedSourceIp"})


@dataclass
class LanVpnOneOfStaticNatSourceIpAddressOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class LanVpnOneOfStaticNatTranslatedSourceIpAddressOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VpnOneOfStaticNatSubnetPrefixLengthOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class LanVpnOneOfStaticNatDirectionOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ServiceLanVpnNatDirectionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class VpnStaticNatSubnet:
    prefix_length: Optional[
        Union[
            OneOfStaticNatSubnetPrefixLengthOptionsDef1,
            VpnOneOfStaticNatSubnetPrefixLengthOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "prefixLength"})
    source_ip_subnet: Optional[
        Union[
            OneOfStaticNatSourceIpAddressOptionsDef1, LanVpnOneOfStaticNatSourceIpAddressOptionsDef2
        ]
    ] = _field(default=None, metadata={"alias": "sourceIpSubnet"})
    static_nat_direction: Optional[
        Union[OneOfStaticNatDirectionOptionsDef1, LanVpnOneOfStaticNatDirectionOptionsDef2]
    ] = _field(default=None, metadata={"alias": "staticNatDirection"})
    # Tracking object for NAT configuration
    tracking_object: Optional[Any] = _field(default=None, metadata={"alias": "trackingObject"})
    translated_source_ip_subnet: Optional[
        Union[
            OneOfStaticNatTranslatedSourceIpAddressOptionsDef1,
            LanVpnOneOfStaticNatTranslatedSourceIpAddressOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "translatedSourceIpSubnet"})


@dataclass
class VpnOneOfNat64V4PoolNameOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VpnOneOfNat64V4PoolRangeStartOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VpnOneOfNat64V4PoolRangeEndOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VpnNat64V4Pool:
    nat64_v4_pool_name: Union[
        OneOfNat64V4PoolNameOptionsDef1, VpnOneOfNat64V4PoolNameOptionsDef2
    ] = _field(metadata={"alias": "nat64V4PoolName"})
    nat64_v4_pool_overload: Union[
        OneOfNat64V4PoolOverloadOptionsDef1,
        OneOfNat64V4PoolOverloadOptionsDef2,
        OneOfNat64V4PoolOverloadOptionsDef3,
    ] = _field(metadata={"alias": "nat64V4PoolOverload"})
    nat64_v4_pool_range_end: Union[
        OneOfNat64V4PoolRangeEndOptionsDef1, VpnOneOfNat64V4PoolRangeEndOptionsDef2
    ] = _field(metadata={"alias": "nat64V4PoolRangeEnd"})
    nat64_v4_pool_range_start: Union[
        OneOfNat64V4PoolRangeStartOptionsDef1, VpnOneOfNat64V4PoolRangeStartOptionsDef2
    ] = _field(metadata={"alias": "nat64V4PoolRangeStart"})


@dataclass
class VpnOneOfRouteLeakFromGlobalProtocolOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: VpnRouteLeakProtocolFromGlobalDef  # pytype: disable=annotation-type-mismatch


@dataclass
class VpnOneOfRouteLeakFromGlobalRedistributeProtocolOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: VpnRouteLeakRedistributeGlobalProtocolDef  # pytype: disable=annotation-type-mismatch


@dataclass
class ServiceLanVpnRedistributeToProtocol:
    protocol: Union[
        OneOfRouteLeakFromGlobalRedistributeProtocolOptionsDef1,
        VpnOneOfRouteLeakFromGlobalRedistributeProtocolOptionsDef2,
    ]
    policy: Optional[Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]] = (
        _field(default=None)
    )


@dataclass
class VpnRouteLeakFromGlobal:
    route_protocol: Union[
        OneOfRouteLeakFromGlobalProtocolOptionsDef1, VpnOneOfRouteLeakFromGlobalProtocolOptionsDef2
    ] = _field(metadata={"alias": "routeProtocol"})
    # Redistribute Routes to specific Protocol on Service VPN
    redistribute_to_protocol: Optional[List[ServiceLanVpnRedistributeToProtocol]] = _field(
        default=None, metadata={"alias": "redistributeToProtocol"}
    )
    route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "routePolicy"})


@dataclass
class VpnOneOfRouteLeakFromServiceProtocolOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: VpnRouteLeakProtocolFromServiceDef  # pytype: disable=annotation-type-mismatch


@dataclass
class VpnOneOfRouteLeakFromServiceRedistributeProtocolOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: VpnRouteLeakRedistributeServiceProtocolDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SdwanServiceLanVpnRedistributeToProtocol:
    protocol: Union[
        OneOfRouteLeakFromServiceRedistributeProtocolOptionsDef1,
        VpnOneOfRouteLeakFromServiceRedistributeProtocolOptionsDef2,
    ]
    policy: Optional[Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]] = (
        _field(default=None)
    )


@dataclass
class VpnRouteLeakFromService:
    route_protocol: Union[
        OneOfRouteLeakFromServiceProtocolOptionsDef1,
        VpnOneOfRouteLeakFromServiceProtocolOptionsDef2,
    ] = _field(metadata={"alias": "routeProtocol"})
    # Redistribute Routes to specific Protocol on Global VPN
    redistribute_to_protocol: Optional[List[SdwanServiceLanVpnRedistributeToProtocol]] = _field(
        default=None, metadata={"alias": "redistributeToProtocol"}
    )
    route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "routePolicy"})


@dataclass
class VpnOneOfRouteImportFromSourceVpnOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VpnOneOfRouteImportFromProtocolOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: VpnRouteImportFromProtocolDef  # pytype: disable=annotation-type-mismatch


@dataclass
class VpnOneOfRouteImportFromRedistributeProtocolOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: VpnRouteImportFromRedistributeProtocolDef  # pytype: disable=annotation-type-mismatch


@dataclass
class FeatureProfileSdwanServiceLanVpnRedistributeToProtocol:
    protocol: Union[
        VpnOneOfRouteImportFromRedistributeProtocolOptionsDef1,
        OneOfRouteImportFromRedistributeProtocolOptionsDef2,
    ]
    policy: Optional[Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]] = (
        _field(default=None)
    )


@dataclass
class VpnRouteLeakBetweenServices:
    route_protocol: Union[
        OneOfRouteImportFromProtocolOptionsDef1, VpnOneOfRouteImportFromProtocolOptionsDef2
    ] = _field(metadata={"alias": "routeProtocol"})
    source_vpn: Union[
        OneOfRouteImportFromSourceVpnOptionsDef1, VpnOneOfRouteImportFromSourceVpnOptionsDef2
    ] = _field(metadata={"alias": "sourceVpn"})
    # Redistribute Route to specific Protocol on Current Service VPN
    redistribute_to_protocol: Optional[
        List[FeatureProfileSdwanServiceLanVpnRedistributeToProtocol]
    ] = _field(default=None, metadata={"alias": "redistributeToProtocol"})
    route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "routePolicy"})


@dataclass
class VpnMplsVpnRouteTargetOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VpnMplsVpnRouteTargetsDef:
    rt: Union[VpnMplsVpnRouteTargetOptionsDef1, MplsVpnRouteTargetOptionsDef2]


@dataclass
class LanVpnMplsVpnRouteTargetOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class LanVpnMplsVpnRouteTargetsDef:
    rt: Union[LanVpnMplsVpnRouteTargetOptionsDef1, MplsVpnRouteTargetOptionsDef2]


@dataclass
class VpnMplsVpnIpv4RouteTarget:
    export_rt_list: Optional[List[LanVpnMplsVpnRouteTargetsDef]] = _field(
        default=None, metadata={"alias": "exportRtList"}
    )
    import_rt_list: Optional[List[VpnMplsVpnRouteTargetsDef]] = _field(
        default=None, metadata={"alias": "importRtList"}
    )


@dataclass
class ServiceLanVpnMplsVpnRouteTargetOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ServiceLanVpnMplsVpnRouteTargetsDef:
    rt: Union[ServiceLanVpnMplsVpnRouteTargetOptionsDef1, MplsVpnRouteTargetOptionsDef2]


@dataclass
class SdwanServiceLanVpnMplsVpnRouteTargetOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SdwanServiceLanVpnMplsVpnRouteTargetsDef:
    rt: Union[SdwanServiceLanVpnMplsVpnRouteTargetOptionsDef1, MplsVpnRouteTargetOptionsDef2]


@dataclass
class VpnMplsVpnIpv6RouteTarget:
    export_rt_list: Optional[List[SdwanServiceLanVpnMplsVpnRouteTargetsDef]] = _field(
        default=None, metadata={"alias": "exportRtList"}
    )
    import_rt_list: Optional[List[ServiceLanVpnMplsVpnRouteTargetsDef]] = _field(
        default=None, metadata={"alias": "importRtList"}
    )


@dataclass
class ServiceLanVpnData:
    name: Union[OneOfVpnNameOptionsDef1, OneOfVpnNameOptionsDef2, OneOfVpnNameOptionsDef3]
    vpn_id: Union[OneOfVpnIdOptionsDef1, VpnOneOfVpnIdOptionsDef2, OneOfVpnIdOptionsDef3] = _field(
        metadata={"alias": "vpnId"}
    )
    dns_ipv4: Optional[VpnDnsIpv4] = _field(default=None, metadata={"alias": "dnsIpv4"})
    dns_ipv6: Optional[VpnDnsIpv6] = _field(default=None, metadata={"alias": "dnsIpv6"})
    enable_sdra: Optional[Union[OneOfEnableSdraDef1, OneOfEnableSdraDef2]] = _field(
        default=None, metadata={"alias": "enableSdra"}
    )
    # IPv4 Static GRE Route
    gre_route: Optional[List[VpnGreRoute]] = _field(default=None, metadata={"alias": "greRoute"})
    # IPv4 Static IPSEC Route
    ipsec_route: Optional[List[VpnIpsecRoute]] = _field(
        default=None, metadata={"alias": "ipsecRoute"}
    )
    # IPv4 Static Route
    ipv4_route: Optional[List[VpnIpv4Route]] = _field(default=None, metadata={"alias": "ipv4Route"})
    # IPv6 Static Route
    ipv6_route: Optional[List[VpnIpv6Route]] = _field(default=None, metadata={"alias": "ipv6Route"})
    mpls_vpn_ipv4_route_target: Optional[VpnMplsVpnIpv4RouteTarget] = _field(
        default=None, metadata={"alias": "mplsVpnIpv4RouteTarget"}
    )
    mpls_vpn_ipv6_route_target: Optional[VpnMplsVpnIpv6RouteTarget] = _field(
        default=None, metadata={"alias": "mplsVpnIpv6RouteTarget"}
    )
    # NAT64 V4 Pool
    nat64_v4_pool: Optional[List[VpnNat64V4Pool]] = _field(
        default=None, metadata={"alias": "nat64V4Pool"}
    )
    # NAT Pool
    nat_pool: Optional[List[VpnNatPool]] = _field(default=None, metadata={"alias": "natPool"})
    # NAT Port Forward
    nat_port_forward: Optional[List[VpnNatPortForward]] = _field(
        default=None, metadata={"alias": "natPortForward"}
    )
    new_host_mapping: Optional[List[NewHostMapping]] = _field(
        default=None, metadata={"alias": "newHostMapping"}
    )
    omp_admin_distance: Optional[
        Union[
            OneOfOmpAdminIpv4OptionsDef1,
            VpnOneOfOmpAdminIpv4OptionsDef2,
            OneOfOmpAdminIpv4OptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ompAdminDistance"})
    omp_admin_distance_ipv6: Optional[
        Union[
            OneOfOmpAdminIpv6OptionsDef1,
            VpnOneOfOmpAdminIpv6OptionsDef2,
            OneOfOmpAdminIpv6OptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ompAdminDistanceIpv6"})
    # OMP Advertise IPv4
    omp_advertise_ip4: Optional[List[VpnOmpAdvertiseIp4]] = _field(
        default=None, metadata={"alias": "ompAdvertiseIp4"}
    )
    # OMP Advertise IPv6
    omp_advertise_ipv6: Optional[List[VpnOmpAdvertiseIpv6]] = _field(
        default=None, metadata={"alias": "ompAdvertiseIpv6"}
    )
    # Enable route leak from another Service VPN to current Service VPN
    route_leak_between_services: Optional[List[VpnRouteLeakBetweenServices]] = _field(
        default=None, metadata={"alias": "routeLeakBetweenServices"}
    )
    # Enable route leaking from Global to Service VPN
    route_leak_from_global: Optional[List[VpnRouteLeakFromGlobal]] = _field(
        default=None, metadata={"alias": "routeLeakFromGlobal"}
    )
    # Enable route leaking from Service to Global VPN
    route_leak_from_service: Optional[List[VpnRouteLeakFromService]] = _field(
        default=None, metadata={"alias": "routeLeakFromService"}
    )
    # Service
    service: Optional[List[VpnService]] = _field(default=None)
    # Service
    service_route: Optional[List[VpnServiceRoute]] = _field(
        default=None, metadata={"alias": "serviceRoute"}
    )
    # Static NAT Rules
    static_nat: Optional[List[VpnStaticNat]] = _field(default=None, metadata={"alias": "staticNat"})
    # Static NAT Subnet Rules
    static_nat_subnet: Optional[List[VpnStaticNatSubnet]] = _field(
        default=None, metadata={"alias": "staticNatSubnet"}
    )


@dataclass
class VpnPayload:
    """
    LAN VPN feature schema for PUT request
    """

    data: ServiceLanVpnData
    name: str
    # Set the Feature description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetSingleSdwanServiceLanVpnPayload:
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
    # LAN VPN feature schema for PUT request
    payload: Optional[VpnPayload] = _field(default=None)


@dataclass
class EditLanVpnProfileParcelForServicePutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class LanVpnOneOfVpnIdOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class LanVpnOneOfOmpAdminIpv4OptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class LanVpnOneOfOmpAdminIpv6OptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class LanVpnOneOfPrimaryDnsAddressIpv4OptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class LanVpnOneOfSecondaryDnsAddressIpv4OptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class LanVpnDnsIpv4:
    primary_dns_address_ipv4: Optional[
        Union[
            OneOfPrimaryDnsAddressIpv4OptionsDef1,
            LanVpnOneOfPrimaryDnsAddressIpv4OptionsDef2,
            OneOfPrimaryDnsAddressIpv4OptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "primaryDnsAddressIpv4"})
    secondary_dns_address_ipv4: Optional[
        Union[
            OneOfSecondaryDnsAddressIpv4OptionsDef1,
            LanVpnOneOfSecondaryDnsAddressIpv4OptionsDef2,
            OneOfSecondaryDnsAddressIpv4OptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "secondaryDnsAddressIpv4"})


@dataclass
class LanVpnDnsIpv6:
    primary_dns_address_ipv6: Optional[
        Union[
            OneOfPrimaryDnsAddressIpv6OptionsDef1,
            OneOfPrimaryDnsAddressIpv6OptionsDef2,
            OneOfPrimaryDnsAddressIpv6OptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "primaryDnsAddressIpv6"})
    secondary_dns_address_ipv6: Optional[
        Union[
            OneOfSecondaryDnsAddressIpv6OptionsDef1,
            OneOfSecondaryDnsAddressIpv6OptionsDef2,
            OneOfSecondaryDnsAddressIpv6OptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "secondaryDnsAddressIpv6"})


@dataclass
class LanVpnOneOfAdvertiseIpv4ProtocolOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: LanVpnAdvertiseIpv4ProtocolDef  # pytype: disable=annotation-type-mismatch


@dataclass
class ServiceLanVpnOneOfRegionOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ServiceLanVpnRegionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class ServiceLanVpnOneOfRegionOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Optional[Value] = _field(default=None)


@dataclass
class SdwanServiceLanVpnPrefixList:
    prefix: Ipv4AddressAndMaskDef
    aggregate_only: Optional[
        Union[
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef1,
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "aggregateOnly"})
    region: Optional[
        Union[
            OneOfRegionOptionsDef1,
            ServiceLanVpnOneOfRegionOptionsDef2,
            ServiceLanVpnOneOfRegionOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class LanVpnOmpAdvertiseIp4:
    omp_protocol: Union[
        OneOfAdvertiseIpv4ProtocolOptionsDef1, LanVpnOneOfAdvertiseIpv4ProtocolOptionsDef2
    ] = _field(metadata={"alias": "ompProtocol"})
    # IPv4 Prefix List
    prefix_list: Optional[List[SdwanServiceLanVpnPrefixList]] = _field(
        default=None, metadata={"alias": "prefixList"}
    )
    route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "routePolicy"})


@dataclass
class LanVpnOneOfAdvertiseIpv6ProtocolOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: LanVpnAdvertiseIpv6ProtocolDef  # pytype: disable=annotation-type-mismatch


@dataclass
class LanVpnOneOfAdvertiseIpv6ProtocolSubTypeOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: LanVpnProtocolSubTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SdwanServiceLanVpnOneOfRegionOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SdwanServiceLanVpnRegionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SdwanServiceLanVpnOneOfRegionOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Optional[Value] = _field(default=None)


@dataclass
class FeatureProfileSdwanServiceLanVpnPrefixList:
    prefix: Union[OneOfIpv6PrefixOptionsDef1, OneOfIpv6PrefixOptionsDef2]
    aggregate_only: Optional[
        Union[
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef1,
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "aggregateOnly"})
    region: Optional[
        Union[
            OneOfRegionOptionsDef1,
            SdwanServiceLanVpnOneOfRegionOptionsDef2,
            SdwanServiceLanVpnOneOfRegionOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class LanVpnOmpAdvertiseIpv6:
    omp_protocol: Union[
        OneOfAdvertiseIpv6ProtocolOptionsDef1, LanVpnOneOfAdvertiseIpv6ProtocolOptionsDef2
    ] = _field(metadata={"alias": "ompProtocol"})
    # IPv6 Prefix List
    prefix_list: Optional[List[FeatureProfileSdwanServiceLanVpnPrefixList]] = _field(
        default=None, metadata={"alias": "prefixList"}
    )
    protocol_sub_type: Optional[
        Union[
            OneOfAdvertiseIpv6ProtocolSubTypeOptionsDef1,
            LanVpnOneOfAdvertiseIpv6ProtocolSubTypeOptionsDef2,
            OneOfAdvertiseIpv6ProtocolSubTypeOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "protocolSubType"})
    route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "routePolicy"})


@dataclass
class SdwanServiceLanVpnOneOfIpv4NextHopDistanceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class NextHop2:
    address: Union[
        OneOfIpv4NextHopAddressOptionsWithOutDefault1, OneOfIpv4NextHopAddressOptionsWithOutDefault2
    ]
    distance: Union[
        OneOfIpv4NextHopDistanceOptionsDef1,
        SdwanServiceLanVpnOneOfIpv4NextHopDistanceOptionsDef2,
        OneOfIpv4NextHopDistanceOptionsDef3,
    ]


@dataclass
class FeatureProfileSdwanServiceLanVpnOneOfIpv4NextHopDistanceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class LanVpnNextHopWithTracker:
    address: Union[
        OneOfIpv4NextHopAddressOptionsWithOutDefault1, OneOfIpv4NextHopAddressOptionsWithOutDefault2
    ]
    distance: Union[
        OneOfIpv4NextHopDistanceOptionsDef1,
        FeatureProfileSdwanServiceLanVpnOneOfIpv4NextHopDistanceOptionsDef2,
        OneOfIpv4NextHopDistanceOptionsDef3,
    ]
    tracker: Union[OneOfIpv4NextHopTrackerOptionsDef1, OneOfIpv4NextHopTrackerOptionsDef2]


@dataclass
class SdwanServiceLanVpnNextHopContainer:
    # IPv4 Route Gateway Next Hop
    next_hop: Optional[List[NextHop2]] = _field(default=None, metadata={"alias": "nextHop"})
    # IPv4 Route Gateway Next Hop with Tracker
    next_hop_with_tracker: Optional[List[LanVpnNextHopWithTracker]] = _field(
        default=None, metadata={"alias": "nextHopWithTracker"}
    )


@dataclass
class SdwanServiceLanVpnOneOfIpRoute1:
    next_hop_container: SdwanServiceLanVpnNextHopContainer = _field(
        metadata={"alias": "nextHopContainer"}
    )


@dataclass
class LanVpnOneOfIpv4GatewayDistanceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SdwanServiceLanVpnOneOfIpRoute2:
    null0: Union[
        OneOfIpv4V6RouteNull0OptionsWithoutVariable1, OneOfIpv4V6RouteNull0OptionsWithoutVariable2
    ]
    distance: Optional[
        Union[
            OneOfIpv4GatewayDistanceOptionsDef1,
            LanVpnOneOfIpv4GatewayDistanceOptionsDef2,
            OneOfIpv4GatewayDistanceOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class LanVpnOneOfIpv4NextHopAddressOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class V1FeatureProfileSdwanServiceLanVpnOneOfIpv4NextHopDistanceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class NextHop3:
    address: Union[
        OneOfIpv4NextHopAddressOptionsDef1,
        LanVpnOneOfIpv4NextHopAddressOptionsDef2,
        OneOfIpv4NextHopAddressOptionsDef3,
    ]
    distance: Union[
        OneOfIpv4NextHopDistanceOptionsDef1,
        V1FeatureProfileSdwanServiceLanVpnOneOfIpv4NextHopDistanceOptionsDef2,
        OneOfIpv4NextHopDistanceOptionsDef3,
    ]


@dataclass
class LanVpnIpStaticRouteInterface:
    interface_name: Union[InterfaceName1, InterfaceName2] = _field(
        metadata={"alias": "interfaceName"}
    )
    next_hop: Optional[List[NextHop3]] = _field(default=None, metadata={"alias": "nextHop"})


@dataclass
class SdwanServiceLanVpnInterfaceContainer:
    ip_static_route_interface: List[LanVpnIpStaticRouteInterface] = _field(
        metadata={"alias": "ipStaticRouteInterface"}
    )


@dataclass
class LanVpnOneOfIpRoute5:
    interface_container: SdwanServiceLanVpnInterfaceContainer = _field(
        metadata={"alias": "interfaceContainer"}
    )


@dataclass
class LanVpnIpv4Route:
    one_of_ip_route: Union[
        SdwanServiceLanVpnOneOfIpRoute1,
        SdwanServiceLanVpnOneOfIpRoute2,
        OneOfIpRoute3,
        OneOfIpRoute4,
        LanVpnOneOfIpRoute5,
    ] = _field(metadata={"alias": "oneOfIpRoute"})
    # Prefix
    prefix: Prefix


@dataclass
class ServiceLanVpnOneOfIpv6NextHopDistanceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class NextHop4:
    address: Union[
        OneOfIpv6NextHopAddressOptionsWithOutDefault1, OneOfIpv6NextHopAddressOptionsWithOutDefault2
    ]
    distance: Union[
        OneOfIpv6NextHopDistanceOptionsDef1,
        ServiceLanVpnOneOfIpv6NextHopDistanceOptionsDef2,
        OneOfIpv6NextHopDistanceOptionsDef3,
    ]


@dataclass
class FeatureProfileSdwanServiceLanVpnNextHopContainer:
    # IPv6 Route Gateway Next Hop
    next_hop: Optional[List[NextHop4]] = _field(default=None, metadata={"alias": "nextHop"})


@dataclass
class FeatureProfileSdwanServiceLanVpnOneOfIpRoute1:
    next_hop_container: FeatureProfileSdwanServiceLanVpnNextHopContainer = _field(
        metadata={"alias": "nextHopContainer"}
    )


@dataclass
class FeatureProfileSdwanServiceLanVpnOneOfIpRoute2:
    null0: Union[
        OneOfIpv4V6RouteNull0OptionsWithoutVariable1, OneOfIpv4V6RouteNull0OptionsWithoutVariable2
    ]


@dataclass
class ServiceLanVpnOneOfIpRoute3:
    nat: Union[OneOfIpv6RouteNatOptionsWithoutDefault1, OneOfIpv6RouteNatOptionsWithoutDefault2]


@dataclass
class SdwanServiceLanVpnOneOfIpv6NextHopDistanceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class NextHop5:
    address: Union[
        OneOfIpv6NextHopAddressOptionsDef1,
        OneOfIpv6NextHopAddressOptionsDef2,
        OneOfIpv6NextHopAddressOptionsDef3,
    ]
    distance: Union[
        OneOfIpv6NextHopDistanceOptionsDef1,
        SdwanServiceLanVpnOneOfIpv6NextHopDistanceOptionsDef2,
        OneOfIpv6NextHopDistanceOptionsDef3,
    ]


@dataclass
class LanVpnIpv6StaticRouteInterface:
    interface_name: Union[InterfaceName1, InterfaceName2] = _field(
        metadata={"alias": "interfaceName"}
    )
    next_hop: Optional[List[NextHop5]] = _field(default=None, metadata={"alias": "nextHop"})


@dataclass
class FeatureProfileSdwanServiceLanVpnInterfaceContainer:
    ipv6_static_route_interface: List[LanVpnIpv6StaticRouteInterface] = _field(
        metadata={"alias": "ipv6StaticRouteInterface"}
    )


@dataclass
class ServiceLanVpnOneOfIpRoute4:
    interface_container: FeatureProfileSdwanServiceLanVpnInterfaceContainer = _field(
        metadata={"alias": "interfaceContainer"}
    )


@dataclass
class LanVpnIpv6Route:
    one_of_ip_route: Union[
        FeatureProfileSdwanServiceLanVpnOneOfIpRoute1,
        FeatureProfileSdwanServiceLanVpnOneOfIpRoute2,
        ServiceLanVpnOneOfIpRoute3,
        ServiceLanVpnOneOfIpRoute4,
    ] = _field(metadata={"alias": "oneOfIpRoute"})
    prefix: Union[OneOfIpv6RoutePrefixOptionsDef1, OneOfIpv6RoutePrefixOptionsDef2]


@dataclass
class LanVpnOneOfServiceTypeOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: LanVpnServiceTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class LanVpnOneOfListOfIpV4OptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class LanVpnService:
    ipv4_addresses: Union[OneOfListOfIpV4OptionsDef1, LanVpnOneOfListOfIpV4OptionsDef2] = _field(
        metadata={"alias": "ipv4Addresses"}
    )
    service_type: Union[OneOfServiceTypeOptionsDef1, LanVpnOneOfServiceTypeOptionsDef2] = _field(
        metadata={"alias": "serviceType"}
    )
    tracking: Union[
        OneOfServiceTrackingOptionsDef1,
        OneOfServiceTrackingOptionsDef2,
        OneOfServiceTrackingOptionsDef3,
    ]


@dataclass
class Prefix1:
    """
    Service Route Ip and Subnet Mask
    """

    ip_address: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2] = _field(
        metadata={"alias": "ipAddress"}
    )
    subnet_mask: Union[OneOfIpV4SubnetMaskOptionsDef1, OneOfIpV4SubnetMaskOptionsDef2] = _field(
        metadata={"alias": "subnetMask"}
    )


@dataclass
class LanVpnOneOfServiceRouteServiceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: LanVpnServiceRouteDef  # pytype: disable=annotation-type-mismatch


@dataclass
class LanVpnOneOfSseInstanceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class LanVpnServiceRoute:
    # Service Route Ip and Subnet Mask
    prefix: Prefix1
    service: Union[
        OneOfServiceRouteServiceOptionsDef1,
        LanVpnOneOfServiceRouteServiceOptionsDef2,
        OneOfServiceRouteServiceOptionsDef3,
    ]
    vpn: OneOfDefaultVpnIdOptionsDef
    sse_instance: Optional[
        Union[OneOfSseInstanceOptionsDef1, LanVpnOneOfSseInstanceOptionsDef2]
    ] = _field(default=None, metadata={"alias": "sseInstance"})


@dataclass
class Prefix2:
    """
    GRE Route Ip and Subnet Mask
    """

    ip_address: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2] = _field(
        metadata={"alias": "ipAddress"}
    )
    subnet_mask: Union[OneOfIpV4SubnetMaskOptionsDef1, OneOfIpV4SubnetMaskOptionsDef2] = _field(
        metadata={"alias": "subnetMask"}
    )


@dataclass
class LanVpnOneOfGreRouteInterfaceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class LanVpnGreRoute:
    interface: Union[
        OneOfGreRouteInterfaceOptionsDef1,
        LanVpnOneOfGreRouteInterfaceOptionsDef2,
        OneOfGreRouteInterfaceOptionsDef3,
    ]
    # GRE Route Ip and Subnet Mask
    prefix: Prefix2
    vpn: OneOfDefaultVpnIdOptionsDef


@dataclass
class Prefix3:
    """
    IPSEC Route Ip and Subnet Mask
    """

    ip_address: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2] = _field(
        metadata={"alias": "ipAddress"}
    )
    subnet_mask: Union[OneOfIpV4SubnetMaskOptionsDef1, OneOfIpV4SubnetMaskOptionsDef2] = _field(
        metadata={"alias": "subnetMask"}
    )


@dataclass
class LanVpnOneOfIpsecRouteInterfaceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class LanVpnIpsecRoute:
    interface: Union[
        OneOfIpsecRouteInterfaceOptionsDef1,
        LanVpnOneOfIpsecRouteInterfaceOptionsDef2,
        OneOfIpsecRouteInterfaceOptionsDef3,
    ]
    # IPSEC Route Ip and Subnet Mask
    prefix: Prefix3


@dataclass
class LanVpnOneOfNatPoolNameOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class LanVpnOneOfNatPoolPrefixLengthOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class LanVpnOneOfNatPoolRangeStartOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class LanVpnOneOfNatPoolRangeEndOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class LanVpnOneOfNatPoolDirectionOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SdwanServiceLanVpnNatDirectionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class LanVpnNatPool:
    direction: Union[OneOfNatPoolDirectionOptionsDef1, LanVpnOneOfNatPoolDirectionOptionsDef2]
    nat_pool_name: Union[OneOfNatPoolNameOptionsDef1, LanVpnOneOfNatPoolNameOptionsDef2] = _field(
        metadata={"alias": "natPoolName"}
    )
    overload: Union[
        OneOfNatPoolOverloadOptionsDef1,
        OneOfNatPoolOverloadOptionsDef2,
        OneOfNatPoolOverloadOptionsDef3,
    ]
    prefix_length: Union[
        OneOfNatPoolPrefixLengthOptionsDef1, LanVpnOneOfNatPoolPrefixLengthOptionsDef2
    ] = _field(metadata={"alias": "prefixLength"})
    range_end: Union[OneOfNatPoolRangeEndOptionsDef1, LanVpnOneOfNatPoolRangeEndOptionsDef2] = (
        _field(metadata={"alias": "rangeEnd"})
    )
    range_start: Union[
        OneOfNatPoolRangeStartOptionsDef1, LanVpnOneOfNatPoolRangeStartOptionsDef2
    ] = _field(metadata={"alias": "rangeStart"})
    # Tracking object for NAT configuration
    tracking_object: Optional[Any] = _field(default=None, metadata={"alias": "trackingObject"})


@dataclass
class ServiceLanVpnOneOfNatPoolNameInUseOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class LanVpnOneOfNatPortForwardSourcePortOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class LanVpnOneOfNatPortForwardTranslatePortOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class LanVpnOneOfNatPortForwardSourceIpAddressOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class LanVpnOneOfNatPortForwardTranslatedSourceIpAddressOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class LanVpnOneOfNatPortForwardProtocolOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: LanVpnNatPortForwardProtocolDef  # pytype: disable=annotation-type-mismatch


@dataclass
class LanVpnNatPortForward:
    nat_pool_name: Union[
        OneOfNatPoolNameInUseOptionsDef1,
        ServiceLanVpnOneOfNatPoolNameInUseOptionsDef2,
        OneOfNatPoolNameInUseOptionsDef3,
    ] = _field(metadata={"alias": "natPoolName"})
    protocol: Union[
        OneOfNatPortForwardProtocolOptionsDef1, LanVpnOneOfNatPortForwardProtocolOptionsDef2
    ]
    source_ip: Union[
        OneOfNatPortForwardSourceIpAddressOptionsDef1,
        LanVpnOneOfNatPortForwardSourceIpAddressOptionsDef2,
    ] = _field(metadata={"alias": "sourceIp"})
    source_port: Union[
        OneOfNatPortForwardSourcePortOptionsDef1, LanVpnOneOfNatPortForwardSourcePortOptionsDef2
    ] = _field(metadata={"alias": "sourcePort"})
    translate_port: Union[
        OneOfNatPortForwardTranslatePortOptionsDef1,
        LanVpnOneOfNatPortForwardTranslatePortOptionsDef2,
    ] = _field(metadata={"alias": "translatePort"})
    translated_source_ip: Union[
        OneOfNatPortForwardTranslatedSourceIpAddressOptionsDef1,
        LanVpnOneOfNatPortForwardTranslatedSourceIpAddressOptionsDef2,
    ] = _field(metadata={"alias": "translatedSourceIp"})


@dataclass
class SdwanServiceLanVpnOneOfNatPoolNameInUseOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class ServiceLanVpnOneOfStaticNatSourceIpAddressOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ServiceLanVpnOneOfStaticNatTranslatedSourceIpAddressOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ServiceLanVpnOneOfStaticNatDirectionOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: (
        FeatureProfileSdwanServiceLanVpnNatDirectionDef  # pytype: disable=annotation-type-mismatch
    )


@dataclass
class LanVpnStaticNat:
    nat_pool_name: Optional[
        Union[
            OneOfNatPoolNameInUseOptionsDef1,
            SdwanServiceLanVpnOneOfNatPoolNameInUseOptionsDef2,
            OneOfNatPoolNameInUseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "natPoolName"})
    source_ip: Optional[
        Union[
            OneOfStaticNatSourceIpAddressOptionsDef1,
            ServiceLanVpnOneOfStaticNatSourceIpAddressOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "sourceIp"})
    static_nat_direction: Optional[
        Union[OneOfStaticNatDirectionOptionsDef1, ServiceLanVpnOneOfStaticNatDirectionOptionsDef2]
    ] = _field(default=None, metadata={"alias": "staticNatDirection"})
    # Tracking object for NAT configuration
    tracking_object: Optional[Any] = _field(default=None, metadata={"alias": "trackingObject"})
    translated_source_ip: Optional[
        Union[
            OneOfStaticNatTranslatedSourceIpAddressOptionsDef1,
            ServiceLanVpnOneOfStaticNatTranslatedSourceIpAddressOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "translatedSourceIp"})


@dataclass
class SdwanServiceLanVpnOneOfStaticNatSourceIpAddressOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SdwanServiceLanVpnOneOfStaticNatTranslatedSourceIpAddressOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class LanVpnOneOfStaticNatSubnetPrefixLengthOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SdwanServiceLanVpnOneOfStaticNatDirectionOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: V1FeatureProfileSdwanServiceLanVpnNatDirectionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class LanVpnStaticNatSubnet:
    prefix_length: Optional[
        Union[
            OneOfStaticNatSubnetPrefixLengthOptionsDef1,
            LanVpnOneOfStaticNatSubnetPrefixLengthOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "prefixLength"})
    source_ip_subnet: Optional[
        Union[
            OneOfStaticNatSourceIpAddressOptionsDef1,
            SdwanServiceLanVpnOneOfStaticNatSourceIpAddressOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "sourceIpSubnet"})
    static_nat_direction: Optional[
        Union[
            OneOfStaticNatDirectionOptionsDef1, SdwanServiceLanVpnOneOfStaticNatDirectionOptionsDef2
        ]
    ] = _field(default=None, metadata={"alias": "staticNatDirection"})
    # Tracking object for NAT configuration
    tracking_object: Optional[Any] = _field(default=None, metadata={"alias": "trackingObject"})
    translated_source_ip_subnet: Optional[
        Union[
            OneOfStaticNatTranslatedSourceIpAddressOptionsDef1,
            SdwanServiceLanVpnOneOfStaticNatTranslatedSourceIpAddressOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "translatedSourceIpSubnet"})


@dataclass
class LanVpnOneOfNat64V4PoolNameOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class LanVpnOneOfNat64V4PoolRangeStartOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class LanVpnOneOfNat64V4PoolRangeEndOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class LanVpnNat64V4Pool:
    nat64_v4_pool_name: Union[
        OneOfNat64V4PoolNameOptionsDef1, LanVpnOneOfNat64V4PoolNameOptionsDef2
    ] = _field(metadata={"alias": "nat64V4PoolName"})
    nat64_v4_pool_overload: Union[
        OneOfNat64V4PoolOverloadOptionsDef1,
        OneOfNat64V4PoolOverloadOptionsDef2,
        OneOfNat64V4PoolOverloadOptionsDef3,
    ] = _field(metadata={"alias": "nat64V4PoolOverload"})
    nat64_v4_pool_range_end: Union[
        OneOfNat64V4PoolRangeEndOptionsDef1, LanVpnOneOfNat64V4PoolRangeEndOptionsDef2
    ] = _field(metadata={"alias": "nat64V4PoolRangeEnd"})
    nat64_v4_pool_range_start: Union[
        OneOfNat64V4PoolRangeStartOptionsDef1, LanVpnOneOfNat64V4PoolRangeStartOptionsDef2
    ] = _field(metadata={"alias": "nat64V4PoolRangeStart"})


@dataclass
class LanVpnOneOfRouteLeakFromGlobalProtocolOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: LanVpnRouteLeakProtocolFromGlobalDef  # pytype: disable=annotation-type-mismatch


@dataclass
class LanVpnOneOfRouteLeakFromGlobalRedistributeProtocolOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: LanVpnRouteLeakRedistributeGlobalProtocolDef  # pytype: disable=annotation-type-mismatch


@dataclass
class V1FeatureProfileSdwanServiceLanVpnRedistributeToProtocol:
    protocol: Union[
        OneOfRouteLeakFromGlobalRedistributeProtocolOptionsDef1,
        LanVpnOneOfRouteLeakFromGlobalRedistributeProtocolOptionsDef2,
    ]
    policy: Optional[Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]] = (
        _field(default=None)
    )


@dataclass
class LanVpnRouteLeakFromGlobal:
    route_protocol: Union[
        OneOfRouteLeakFromGlobalProtocolOptionsDef1,
        LanVpnOneOfRouteLeakFromGlobalProtocolOptionsDef2,
    ] = _field(metadata={"alias": "routeProtocol"})
    # Redistribute Routes to specific Protocol on Service VPN
    redistribute_to_protocol: Optional[
        List[V1FeatureProfileSdwanServiceLanVpnRedistributeToProtocol]
    ] = _field(default=None, metadata={"alias": "redistributeToProtocol"})
    route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "routePolicy"})


@dataclass
class LanVpnOneOfRouteLeakFromServiceProtocolOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: LanVpnRouteLeakProtocolFromServiceDef  # pytype: disable=annotation-type-mismatch


@dataclass
class LanVpnOneOfRouteLeakFromServiceRedistributeProtocolOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: LanVpnRouteLeakRedistributeServiceProtocolDef  # pytype: disable=annotation-type-mismatch


@dataclass
class RedistributeToProtocol1:
    protocol: Union[
        OneOfRouteLeakFromServiceRedistributeProtocolOptionsDef1,
        LanVpnOneOfRouteLeakFromServiceRedistributeProtocolOptionsDef2,
    ]
    policy: Optional[Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]] = (
        _field(default=None)
    )


@dataclass
class LanVpnRouteLeakFromService:
    route_protocol: Union[
        OneOfRouteLeakFromServiceProtocolOptionsDef1,
        LanVpnOneOfRouteLeakFromServiceProtocolOptionsDef2,
    ] = _field(metadata={"alias": "routeProtocol"})
    # Redistribute Routes to specific Protocol on Global VPN
    redistribute_to_protocol: Optional[List[RedistributeToProtocol1]] = _field(
        default=None, metadata={"alias": "redistributeToProtocol"}
    )
    route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "routePolicy"})


@dataclass
class LanVpnOneOfRouteImportFromSourceVpnOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class LanVpnOneOfRouteImportFromProtocolOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: LanVpnRouteImportFromProtocolDef  # pytype: disable=annotation-type-mismatch


@dataclass
class LanVpnOneOfRouteImportFromRedistributeProtocolOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: LanVpnRouteImportFromRedistributeProtocolDef  # pytype: disable=annotation-type-mismatch


@dataclass
class RedistributeToProtocol2:
    protocol: Union[
        LanVpnOneOfRouteImportFromRedistributeProtocolOptionsDef1,
        OneOfRouteImportFromRedistributeProtocolOptionsDef2,
    ]
    policy: Optional[Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]] = (
        _field(default=None)
    )


@dataclass
class LanVpnRouteLeakBetweenServices:
    route_protocol: Union[
        OneOfRouteImportFromProtocolOptionsDef1, LanVpnOneOfRouteImportFromProtocolOptionsDef2
    ] = _field(metadata={"alias": "routeProtocol"})
    source_vpn: Union[
        OneOfRouteImportFromSourceVpnOptionsDef1, LanVpnOneOfRouteImportFromSourceVpnOptionsDef2
    ] = _field(metadata={"alias": "sourceVpn"})
    # Redistribute Route to specific Protocol on Current Service VPN
    redistribute_to_protocol: Optional[List[RedistributeToProtocol2]] = _field(
        default=None, metadata={"alias": "redistributeToProtocol"}
    )
    route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "routePolicy"})


@dataclass
class FeatureProfileSdwanServiceLanVpnMplsVpnRouteTargetOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class FeatureProfileSdwanServiceLanVpnMplsVpnRouteTargetsDef:
    rt: Union[
        FeatureProfileSdwanServiceLanVpnMplsVpnRouteTargetOptionsDef1, MplsVpnRouteTargetOptionsDef2
    ]


@dataclass
class V1FeatureProfileSdwanServiceLanVpnMplsVpnRouteTargetOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class V1FeatureProfileSdwanServiceLanVpnMplsVpnRouteTargetsDef:
    rt: Union[
        V1FeatureProfileSdwanServiceLanVpnMplsVpnRouteTargetOptionsDef1,
        MplsVpnRouteTargetOptionsDef2,
    ]


@dataclass
class LanVpnMplsVpnIpv4RouteTarget:
    export_rt_list: Optional[List[V1FeatureProfileSdwanServiceLanVpnMplsVpnRouteTargetsDef]] = (
        _field(default=None, metadata={"alias": "exportRtList"})
    )
    import_rt_list: Optional[List[FeatureProfileSdwanServiceLanVpnMplsVpnRouteTargetsDef]] = _field(
        default=None, metadata={"alias": "importRtList"}
    )


@dataclass
class MplsVpnRouteTargetOptionsDef11:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class MplsVpnRouteTargetsDef1:
    rt: Union[MplsVpnRouteTargetOptionsDef11, MplsVpnRouteTargetOptionsDef2]


@dataclass
class MplsVpnRouteTargetOptionsDef12:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class MplsVpnRouteTargetsDef2:
    rt: Union[MplsVpnRouteTargetOptionsDef12, MplsVpnRouteTargetOptionsDef2]


@dataclass
class LanVpnMplsVpnIpv6RouteTarget:
    export_rt_list: Optional[List[MplsVpnRouteTargetsDef2]] = _field(
        default=None, metadata={"alias": "exportRtList"}
    )
    import_rt_list: Optional[List[MplsVpnRouteTargetsDef1]] = _field(
        default=None, metadata={"alias": "importRtList"}
    )


@dataclass
class SdwanServiceLanVpnData:
    name: Union[OneOfVpnNameOptionsDef1, OneOfVpnNameOptionsDef2, OneOfVpnNameOptionsDef3]
    vpn_id: Union[OneOfVpnIdOptionsDef1, LanVpnOneOfVpnIdOptionsDef2, OneOfVpnIdOptionsDef3] = (
        _field(metadata={"alias": "vpnId"})
    )
    dns_ipv4: Optional[LanVpnDnsIpv4] = _field(default=None, metadata={"alias": "dnsIpv4"})
    dns_ipv6: Optional[LanVpnDnsIpv6] = _field(default=None, metadata={"alias": "dnsIpv6"})
    enable_sdra: Optional[Union[OneOfEnableSdraDef1, OneOfEnableSdraDef2]] = _field(
        default=None, metadata={"alias": "enableSdra"}
    )
    # IPv4 Static GRE Route
    gre_route: Optional[List[LanVpnGreRoute]] = _field(default=None, metadata={"alias": "greRoute"})
    # IPv4 Static IPSEC Route
    ipsec_route: Optional[List[LanVpnIpsecRoute]] = _field(
        default=None, metadata={"alias": "ipsecRoute"}
    )
    # IPv4 Static Route
    ipv4_route: Optional[List[LanVpnIpv4Route]] = _field(
        default=None, metadata={"alias": "ipv4Route"}
    )
    # IPv6 Static Route
    ipv6_route: Optional[List[LanVpnIpv6Route]] = _field(
        default=None, metadata={"alias": "ipv6Route"}
    )
    mpls_vpn_ipv4_route_target: Optional[LanVpnMplsVpnIpv4RouteTarget] = _field(
        default=None, metadata={"alias": "mplsVpnIpv4RouteTarget"}
    )
    mpls_vpn_ipv6_route_target: Optional[LanVpnMplsVpnIpv6RouteTarget] = _field(
        default=None, metadata={"alias": "mplsVpnIpv6RouteTarget"}
    )
    # NAT64 V4 Pool
    nat64_v4_pool: Optional[List[LanVpnNat64V4Pool]] = _field(
        default=None, metadata={"alias": "nat64V4Pool"}
    )
    # NAT Pool
    nat_pool: Optional[List[LanVpnNatPool]] = _field(default=None, metadata={"alias": "natPool"})
    # NAT Port Forward
    nat_port_forward: Optional[List[LanVpnNatPortForward]] = _field(
        default=None, metadata={"alias": "natPortForward"}
    )
    new_host_mapping: Optional[List[NewHostMapping]] = _field(
        default=None, metadata={"alias": "newHostMapping"}
    )
    omp_admin_distance: Optional[
        Union[
            OneOfOmpAdminIpv4OptionsDef1,
            LanVpnOneOfOmpAdminIpv4OptionsDef2,
            OneOfOmpAdminIpv4OptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ompAdminDistance"})
    omp_admin_distance_ipv6: Optional[
        Union[
            OneOfOmpAdminIpv6OptionsDef1,
            LanVpnOneOfOmpAdminIpv6OptionsDef2,
            OneOfOmpAdminIpv6OptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ompAdminDistanceIpv6"})
    # OMP Advertise IPv4
    omp_advertise_ip4: Optional[List[LanVpnOmpAdvertiseIp4]] = _field(
        default=None, metadata={"alias": "ompAdvertiseIp4"}
    )
    # OMP Advertise IPv6
    omp_advertise_ipv6: Optional[List[LanVpnOmpAdvertiseIpv6]] = _field(
        default=None, metadata={"alias": "ompAdvertiseIpv6"}
    )
    # Enable route leak from another Service VPN to current Service VPN
    route_leak_between_services: Optional[List[LanVpnRouteLeakBetweenServices]] = _field(
        default=None, metadata={"alias": "routeLeakBetweenServices"}
    )
    # Enable route leaking from Global to Service VPN
    route_leak_from_global: Optional[List[LanVpnRouteLeakFromGlobal]] = _field(
        default=None, metadata={"alias": "routeLeakFromGlobal"}
    )
    # Enable route leaking from Service to Global VPN
    route_leak_from_service: Optional[List[LanVpnRouteLeakFromService]] = _field(
        default=None, metadata={"alias": "routeLeakFromService"}
    )
    # Service
    service: Optional[List[LanVpnService]] = _field(default=None)
    # Service
    service_route: Optional[List[LanVpnServiceRoute]] = _field(
        default=None, metadata={"alias": "serviceRoute"}
    )
    # Static NAT Rules
    static_nat: Optional[List[LanVpnStaticNat]] = _field(
        default=None, metadata={"alias": "staticNat"}
    )
    # Static NAT Subnet Rules
    static_nat_subnet: Optional[List[LanVpnStaticNatSubnet]] = _field(
        default=None, metadata={"alias": "staticNatSubnet"}
    )


@dataclass
class EditLanVpnProfileParcelForServicePutRequest:
    """
    LAN VPN feature schema for PUT request
    """

    data: SdwanServiceLanVpnData
    name: str
    # Set the Feature description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
