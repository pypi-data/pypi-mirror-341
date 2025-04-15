# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

VariableOptionTypeDef = Literal["variable"]

GlobalOptionTypeDef = Literal["global"]

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

StaticNatDirectionDef = Literal["inside", "outside"]

NatPortForwardProtocolDef = Literal["TCP", "UDP"]

SourceTypeDef = Literal["acl", "route-map"]

NatTypeDef = Literal["interface", "pool"]

RouteLeakProtocolFromGlobalDef = Literal["bgp", "connected", "ospf", "static"]

RouteLeakRedistributeGlobalProtocolDef = Literal["bgp", "ospf"]

RouteLeakProtocolFromServiceDef = Literal["bgp", "connected", "ospf", "static"]

RouteLeakRedistributeServiceProtocolDef = Literal["bgp", "ospf"]

RouteImportFromProtocolDef = Literal["bgp", "connected", "ospf", "static"]

RouteImportFromRedistributeProtocolDef = Literal["bgp", "ospf"]


@dataclass
class OneOfVrfOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfVrfOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


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
class MplsVpnRouteTargetOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfVpnNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfVpnNameOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfVpnNameOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfIpAddressOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpAddressOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class Dns:
    ip_address: Union[OneOfIpAddressOptionsDef1, OneOfIpAddressOptionsDef2] = _field(
        metadata={"alias": "ipAddress"}
    )


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
class HostMapping:
    host_name: Union[OneOfHostNameOptionsWithoutDefault1, OneOfHostNameOptionsWithoutDefault2] = (
        _field(metadata={"alias": "hostName"})
    )
    list_of_ip: Union[OneOfListOfIpOptionsWithoutDefault1, OneOfListOfIpOptionsWithoutDefault2] = (
        _field(metadata={"alias": "listOfIp"})
    )


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
class OneOfIpV4AddressOptionsWithoutDefault1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpV4AddressOptionsWithoutDefault2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


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
class RefId:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfRefIdOptionsDef1:
    ref_id: RefId = _field(metadata={"alias": "refId"})


@dataclass
class OneOfRefIdOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class NextHop:
    address: Union[OneOfIpV4AddressOptionsWithoutDefault1, OneOfIpV4AddressOptionsWithoutDefault2]
    distance: Union[
        OneOfIpv4NextHopDistanceOptionsDef1,
        OneOfIpv4NextHopDistanceOptionsDef2,
        OneOfIpv4NextHopDistanceOptionsDef3,
    ]
    tracker_id: Union[OneOfRefIdOptionsDef1, OneOfRefIdOptionsDef2] = _field(
        metadata={"alias": "trackerId"}
    )


@dataclass
class NextHopContainer:
    # IPv4 Route Gateway Next Hop
    next_hop: List[NextHop] = _field(metadata={"alias": "nextHop"})


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
    distance: Optional[
        Union[
            OneOfIpv4NextHopDistanceOptionsDef1,
            OneOfIpv4NextHopDistanceOptionsDef2,
            OneOfIpv4NextHopDistanceOptionsDef3,
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
    distance: Optional[
        Union[
            OneOfIpv4NextHopDistanceOptionsDef1,
            OneOfIpv4NextHopDistanceOptionsDef2,
            OneOfIpv4NextHopDistanceOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class OneOfVrfInterfaceNameOptionsNoDefaultDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfVrfInterfaceNameOptionsNoDefaultDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class VrfNextHop:
    address: Union[OneOfIpV4AddressOptionsWithoutDefault1, OneOfIpV4AddressOptionsWithoutDefault2]
    distance: Union[
        OneOfIpv4NextHopDistanceOptionsDef1,
        OneOfIpv4NextHopDistanceOptionsDef2,
        OneOfIpv4NextHopDistanceOptionsDef3,
    ]


@dataclass
class IpStaticRouteInterface:
    interface_name: Union[
        OneOfVrfInterfaceNameOptionsNoDefaultDef1, OneOfVrfInterfaceNameOptionsNoDefaultDef2
    ] = _field(metadata={"alias": "interfaceName"})
    distance: Optional[
        Union[
            OneOfIpv4NextHopDistanceOptionsDef1,
            OneOfIpv4NextHopDistanceOptionsDef2,
            OneOfIpv4NextHopDistanceOptionsDef3,
        ]
    ] = _field(default=None)
    next_hop: Optional[List[VrfNextHop]] = _field(default=None, metadata={"alias": "nextHop"})


@dataclass
class InterfaceContainer:
    ip_static_route_interface: List[IpStaticRouteInterface] = _field(
        metadata={"alias": "ipStaticRouteInterface"}
    )


@dataclass
class OneOfIpRoute4:
    interface_container: InterfaceContainer = _field(metadata={"alias": "interfaceContainer"})


@dataclass
class Ipv4Route:
    one_of_ip_route: Union[OneOfIpRoute1, OneOfIpRoute2, OneOfIpRoute3, OneOfIpRoute4] = _field(
        metadata={"alias": "oneOfIpRoute"}
    )
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
class ServiceVrfNextHop:
    address: Union[
        OneOfIpv6NextHopAddressOptionsWithOutDefault1, OneOfIpv6NextHopAddressOptionsWithOutDefault2
    ]
    distance: Union[
        OneOfIpv6NextHopDistanceOptionsDef1,
        OneOfIpv6NextHopDistanceOptionsDef2,
        OneOfIpv6NextHopDistanceOptionsDef3,
    ]


@dataclass
class VrfNextHopContainer:
    # IPv6 Route Gateway Next Hop
    next_hop: Optional[List[ServiceVrfNextHop]] = _field(
        default=None, metadata={"alias": "nextHop"}
    )


@dataclass
class VrfOneOfIpRoute1:
    next_hop_container: VrfNextHopContainer = _field(metadata={"alias": "nextHopContainer"})


@dataclass
class VrfOneOfIpRoute2:
    null0: Union[
        OneOfIpv4V6RouteNull0OptionsWithoutVariable1, OneOfIpv4V6RouteNull0OptionsWithoutVariable2
    ]


@dataclass
class SdRoutingServiceVrfNextHop:
    address: Union[
        OneOfIpv6NextHopAddressOptionsWithOutDefault1, OneOfIpv6NextHopAddressOptionsWithOutDefault2
    ]
    distance: Union[
        OneOfIpv6NextHopDistanceOptionsDef1,
        OneOfIpv6NextHopDistanceOptionsDef2,
        OneOfIpv6NextHopDistanceOptionsDef3,
    ]


@dataclass
class Ipv6StaticRouteInterface:
    interface_name: Union[
        OneOfVrfInterfaceNameOptionsNoDefaultDef1, OneOfVrfInterfaceNameOptionsNoDefaultDef2
    ] = _field(metadata={"alias": "interfaceName"})
    distance: Optional[
        Union[
            OneOfIpv6NextHopDistanceOptionsDef1,
            OneOfIpv6NextHopDistanceOptionsDef2,
            OneOfIpv6NextHopDistanceOptionsDef3,
        ]
    ] = _field(default=None)
    next_hop: Optional[List[SdRoutingServiceVrfNextHop]] = _field(
        default=None, metadata={"alias": "nextHop"}
    )


@dataclass
class VrfInterfaceContainer:
    ipv6_static_route_interface: List[Ipv6StaticRouteInterface] = _field(
        metadata={"alias": "ipv6StaticRouteInterface"}
    )


@dataclass
class VrfOneOfIpRoute3:
    interface_container: VrfInterfaceContainer = _field(metadata={"alias": "interfaceContainer"})


@dataclass
class Ipv6Route:
    one_of_ip_route: Union[VrfOneOfIpRoute1, VrfOneOfIpRoute2, VrfOneOfIpRoute3] = _field(
        metadata={"alias": "oneOfIpRoute"}
    )
    prefix: Union[OneOfIpv6RoutePrefixOptionsDef1, OneOfIpv6RoutePrefixOptionsDef2]


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
class OneOfDirectionOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: StaticNatDirectionDef


@dataclass
class NatInterfaces:
    direction: OneOfDirectionOptionsDef
    interface: Union[
        OneOfVrfInterfaceNameOptionsNoDefaultDef1, OneOfVrfInterfaceNameOptionsNoDefaultDef2
    ]


@dataclass
class StaticNat:
    direction: OneOfDirectionOptionsDef
    source_ip: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2] = _field(
        metadata={"alias": "sourceIp"}
    )
    translate_ip: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2] = _field(
        metadata={"alias": "translateIp"}
    )
    route_map_id: Optional[Union[OneOfRefIdOptionsDef1, OneOfRefIdOptionsDef2]] = _field(
        default=None, metadata={"alias": "routeMapId"}
    )
    tracker_id: Optional[Union[OneOfRefIdOptionsDef1, OneOfRefIdOptionsDef2]] = _field(
        default=None, metadata={"alias": "trackerId"}
    )


@dataclass
class OneOfPrefixLengthOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfPrefixLengthOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class StaticNatSubnet:
    direction: OneOfDirectionOptionsDef
    prefix_length: Union[OneOfPrefixLengthOptionsDef1, OneOfPrefixLengthOptionsDef2] = _field(
        metadata={"alias": "prefixLength"}
    )
    source_ip_subnet: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2] = _field(
        metadata={"alias": "sourceIpSubnet"}
    )
    translate_ip_subnet: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2] = _field(
        metadata={"alias": "translateIpSubnet"}
    )
    tracker_id: Optional[Union[OneOfRefIdOptionsDef1, OneOfRefIdOptionsDef2]] = _field(
        default=None, metadata={"alias": "trackerId"}
    )


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
class OneOfPortOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfPortOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class NatPortForward:
    protocol: Union[OneOfNatPortForwardProtocolOptionsDef1, OneOfNatPortForwardProtocolOptionsDef2]
    source_ip: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2] = _field(
        metadata={"alias": "sourceIp"}
    )
    source_port: Union[OneOfPortOptionsDef1, OneOfPortOptionsDef2] = _field(
        metadata={"alias": "sourcePort"}
    )
    translate_port: Union[OneOfPortOptionsDef1, OneOfPortOptionsDef2] = _field(
        metadata={"alias": "translatePort"}
    )
    translated_source_ip: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2] = _field(
        metadata={"alias": "translatedSourceIp"}
    )


@dataclass
class NatType:
    value: Optional[Any] = _field(default=None)


@dataclass
class OneOfSourceTypeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SourceTypeDef


@dataclass
class ParcelReferenceDef:
    ref_id: RefId = _field(metadata={"alias": "refId"})


@dataclass
class OneOfPoolNameOptionsNoDefaultDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfPoolNameOptionsNoDefaultDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfPrefixLengthWithoutDefaultOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfPrefixLengthWithoutDefaultOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
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
class NatPool:
    """
    NAT Pool
    """

    pool_name: Union[OneOfPoolNameOptionsNoDefaultDef1, OneOfPoolNameOptionsNoDefaultDef2] = _field(
        metadata={"alias": "poolName"}
    )
    prefix_length: Union[
        OneOfPrefixLengthWithoutDefaultOptionsDef1, OneOfPrefixLengthWithoutDefaultOptionsDef2
    ] = _field(metadata={"alias": "prefixLength"})
    range_end: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2] = _field(
        metadata={"alias": "rangeEnd"}
    )
    range_start: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2] = _field(
        metadata={"alias": "rangeStart"}
    )
    match_in_vrf: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "matchInVrf"})
    overload: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)
    tracker_id: Optional[Union[OneOfRefIdOptionsDef1, OneOfRefIdOptionsDef2]] = _field(
        default=None, metadata={"alias": "trackerId"}
    )


@dataclass
class DynamicNat1:
    direction: OneOfDirectionOptionsDef
    egress_interface: Union[
        OneOfVrfInterfaceNameOptionsNoDefaultDef1, OneOfVrfInterfaceNameOptionsNoDefaultDef2
    ] = _field(metadata={"alias": "egressInterface"})
    nat_type: NatType = _field(metadata={"alias": "natType"})
    source_type: OneOfSourceTypeOptionsDef = _field(metadata={"alias": "sourceType"})
    ipv4_acl_id: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "ipv4AclId"}
    )
    # NAT Pool
    nat_pool: Optional[NatPool] = _field(default=None, metadata={"alias": "natPool"})
    route_map_id: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "routeMapId"}
    )


@dataclass
class OneOfNatTypeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: NatTypeDef


@dataclass
class DynamicNat2:
    direction: OneOfDirectionOptionsDef
    nat_type: OneOfNatTypeOptionsDef = _field(metadata={"alias": "natType"})
    source_type: OneOfSourceTypeOptionsDef = _field(metadata={"alias": "sourceType"})
    egress_interface: Optional[
        Union[OneOfVrfInterfaceNameOptionsNoDefaultDef1, OneOfVrfInterfaceNameOptionsNoDefaultDef2]
    ] = _field(default=None, metadata={"alias": "egressInterface"})
    ipv4_acl_id: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "ipv4AclId"}
    )
    # NAT Pool
    nat_pool: Optional[NatPool] = _field(default=None, metadata={"alias": "natPool"})
    route_map_id: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "routeMapId"}
    )


@dataclass
class NatAttributesIpv4:
    """
    NAT Attributes Ipv4
    """

    nat_enable: Union[
        OneOfOnBooleanDefaultFalseNoVariableOptionsDef1,
        OneOfOnBooleanDefaultFalseNoVariableOptionsDef2,
    ] = _field(metadata={"alias": "natEnable"})
    # NAT Attributes Ipv4
    dynamic_nat: Optional[List[Union[DynamicNat1, DynamicNat2]]] = _field(
        default=None, metadata={"alias": "dynamicNat"}
    )
    # nat interfaces
    nat_interfaces: Optional[List[NatInterfaces]] = _field(
        default=None, metadata={"alias": "natInterfaces"}
    )
    # NAT Port Forward
    nat_port_forward: Optional[List[NatPortForward]] = _field(
        default=None, metadata={"alias": "natPortForward"}
    )
    # static NAT
    static_nat: Optional[List[StaticNat]] = _field(default=None, metadata={"alias": "staticNat"})
    # static NAT Subnet
    static_nat_subnet: Optional[List[StaticNatSubnet]] = _field(
        default=None, metadata={"alias": "staticNatSubnet"}
    )


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
class OneOfRoutePolicyNameOptionsDef1:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfRoutePolicyNameOptionsDef2:
    ref_id: RefId = _field(metadata={"alias": "refId"})


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
    # Redistribute Routes to specific Protocol on Service VRF
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
class VrfRedistributeToProtocol:
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
    # Redistribute Routes to specific Protocol on Global VRF
    redistribute_to_protocol: Optional[List[VrfRedistributeToProtocol]] = _field(
        default=None, metadata={"alias": "redistributeToProtocol"}
    )
    route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "routePolicy"})


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
class ServiceVrfRedistributeToProtocol:
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
    source_vpn: Union[OneOfVrfOptionsDef1, OneOfVrfOptionsDef2] = _field(
        metadata={"alias": "sourceVpn"}
    )
    # Redistribute Route to specific Protocol on Current Service VRF
    redistribute_to_protocol: Optional[List[ServiceVrfRedistributeToProtocol]] = _field(
        default=None, metadata={"alias": "redistributeToProtocol"}
    )
    route_policy: Optional[
        Union[OneOfRoutePolicyNameOptionsDef1, OneOfRoutePolicyNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "routePolicy"})


@dataclass
class VrfData:
    vrf_name: Union[OneOfVrfOptionsDef1, OneOfVrfOptionsDef2] = _field(
        metadata={"alias": "vrfName"}
    )
    description: Optional[
        Union[OneOfVpnNameOptionsDef1, OneOfVpnNameOptionsDef2, OneOfVpnNameOptionsDef3]
    ] = _field(default=None)
    dns: Optional[List[Dns]] = _field(default=None)
    host_mapping: Optional[List[HostMapping]] = _field(
        default=None, metadata={"alias": "hostMapping"}
    )
    # IPv4 Static Route
    ipv4_route: Optional[List[Ipv4Route]] = _field(default=None, metadata={"alias": "ipv4Route"})
    # IPv6 Static Route
    ipv6_route: Optional[List[Ipv6Route]] = _field(default=None, metadata={"alias": "ipv6Route"})
    # NAT Attributes Ipv4
    nat_attributes_ipv4: Optional[NatAttributesIpv4] = _field(
        default=None, metadata={"alias": "natAttributesIpv4"}
    )
    rd: Optional[
        Union[
            MplsVpnRouteTargetOptionsDef1,
            MplsVpnRouteTargetOptionsDef2,
            MplsVpnRouteTargetOptionsDef3,
        ]
    ] = _field(default=None)
    # Enable route leak from another Service VRF to current Service VRF
    route_leak_between_services: Optional[List[RouteLeakBetweenServices]] = _field(
        default=None, metadata={"alias": "routeLeakBetweenServices"}
    )
    # Enable route leaking from Global to Service VRF
    route_leak_from_global: Optional[List[RouteLeakFromGlobal]] = _field(
        default=None, metadata={"alias": "routeLeakFromGlobal"}
    )
    # Enable route leaking from Service to Global VRF
    route_leak_from_service: Optional[List[RouteLeakFromService]] = _field(
        default=None, metadata={"alias": "routeLeakFromService"}
    )


@dataclass
class Payload:
    """
    SD-Routing VRF feature schema
    """

    data: VrfData
    name: str
    # Set the feature description
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
    # SD-Routing VRF feature schema
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdRoutingServiceVrfPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateSdroutingServiceVrfFeaturePostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class ServiceVrfData:
    vrf_name: Union[OneOfVrfOptionsDef1, OneOfVrfOptionsDef2] = _field(
        metadata={"alias": "vrfName"}
    )
    description: Optional[
        Union[OneOfVpnNameOptionsDef1, OneOfVpnNameOptionsDef2, OneOfVpnNameOptionsDef3]
    ] = _field(default=None)
    dns: Optional[List[Dns]] = _field(default=None)
    host_mapping: Optional[List[HostMapping]] = _field(
        default=None, metadata={"alias": "hostMapping"}
    )
    # IPv4 Static Route
    ipv4_route: Optional[List[Ipv4Route]] = _field(default=None, metadata={"alias": "ipv4Route"})
    # IPv6 Static Route
    ipv6_route: Optional[List[Ipv6Route]] = _field(default=None, metadata={"alias": "ipv6Route"})
    # NAT Attributes Ipv4
    nat_attributes_ipv4: Optional[NatAttributesIpv4] = _field(
        default=None, metadata={"alias": "natAttributesIpv4"}
    )
    rd: Optional[
        Union[
            MplsVpnRouteTargetOptionsDef1,
            MplsVpnRouteTargetOptionsDef2,
            MplsVpnRouteTargetOptionsDef3,
        ]
    ] = _field(default=None)
    # Enable route leak from another Service VRF to current Service VRF
    route_leak_between_services: Optional[List[RouteLeakBetweenServices]] = _field(
        default=None, metadata={"alias": "routeLeakBetweenServices"}
    )
    # Enable route leaking from Global to Service VRF
    route_leak_from_global: Optional[List[RouteLeakFromGlobal]] = _field(
        default=None, metadata={"alias": "routeLeakFromGlobal"}
    )
    # Enable route leaking from Service to Global VRF
    route_leak_from_service: Optional[List[RouteLeakFromService]] = _field(
        default=None, metadata={"alias": "routeLeakFromService"}
    )


@dataclass
class CreateSdroutingServiceVrfFeaturePostRequest:
    """
    SD-Routing VRF feature schema
    """

    data: ServiceVrfData
    name: str
    # Set the feature description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetSingleSdRoutingServiceVrfPayload:
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
    # SD-Routing VRF feature schema
    payload: Optional[Payload] = _field(default=None)


@dataclass
class EditSdroutingServiceVrfFeaturePutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SdRoutingServiceVrfData:
    vrf_name: Union[OneOfVrfOptionsDef1, OneOfVrfOptionsDef2] = _field(
        metadata={"alias": "vrfName"}
    )
    description: Optional[
        Union[OneOfVpnNameOptionsDef1, OneOfVpnNameOptionsDef2, OneOfVpnNameOptionsDef3]
    ] = _field(default=None)
    dns: Optional[List[Dns]] = _field(default=None)
    host_mapping: Optional[List[HostMapping]] = _field(
        default=None, metadata={"alias": "hostMapping"}
    )
    # IPv4 Static Route
    ipv4_route: Optional[List[Ipv4Route]] = _field(default=None, metadata={"alias": "ipv4Route"})
    # IPv6 Static Route
    ipv6_route: Optional[List[Ipv6Route]] = _field(default=None, metadata={"alias": "ipv6Route"})
    # NAT Attributes Ipv4
    nat_attributes_ipv4: Optional[NatAttributesIpv4] = _field(
        default=None, metadata={"alias": "natAttributesIpv4"}
    )
    rd: Optional[
        Union[
            MplsVpnRouteTargetOptionsDef1,
            MplsVpnRouteTargetOptionsDef2,
            MplsVpnRouteTargetOptionsDef3,
        ]
    ] = _field(default=None)
    # Enable route leak from another Service VRF to current Service VRF
    route_leak_between_services: Optional[List[RouteLeakBetweenServices]] = _field(
        default=None, metadata={"alias": "routeLeakBetweenServices"}
    )
    # Enable route leaking from Global to Service VRF
    route_leak_from_global: Optional[List[RouteLeakFromGlobal]] = _field(
        default=None, metadata={"alias": "routeLeakFromGlobal"}
    )
    # Enable route leaking from Service to Global VRF
    route_leak_from_service: Optional[List[RouteLeakFromService]] = _field(
        default=None, metadata={"alias": "routeLeakFromService"}
    )


@dataclass
class EditSdroutingServiceVrfFeaturePutRequest:
    """
    SD-Routing VRF feature schema
    """

    data: SdRoutingServiceVrfData
    name: str
    # Set the feature description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
