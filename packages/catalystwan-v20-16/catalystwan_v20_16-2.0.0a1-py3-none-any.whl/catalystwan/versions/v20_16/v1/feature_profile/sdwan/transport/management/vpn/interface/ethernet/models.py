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

DuplexDef = Literal["auto", "full", "half"]

SpeedDef = Literal["10", "100", "1000", "10000", "2500", "25000"]

MediaTypeDef = Literal["auto-select", "rj45", "sfp"]

EthernetDuplexDef = Literal["auto", "full", "half"]

EthernetSpeedDef = Literal["10", "100", "1000", "10000", "2500", "25000"]

EthernetMediaTypeDef = Literal["auto-select", "rj45", "sfp"]

InterfaceEthernetDuplexDef = Literal["auto", "full", "half"]

InterfaceEthernetSpeedDef = Literal["10", "100", "1000", "10000", "2500", "25000"]

InterfaceEthernetMediaTypeDef = Literal["auto-select", "rj45", "sfp"]


@dataclass
class OneOfShutdownOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfShutdownOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfShutdownOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


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
class OneOfDescriptionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfDescriptionOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfDescriptionOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfDynamicDhcpDistanceOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfDynamicDhcpDistanceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfDynamicDhcpDistanceOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class Dynamic:
    dynamic_dhcp_distance: Union[
        OneOfDynamicDhcpDistanceOptionsDef1,
        OneOfDynamicDhcpDistanceOptionsDef2,
        OneOfDynamicDhcpDistanceOptionsDef3,
    ] = _field(metadata={"alias": "dynamicDhcpDistance"})


@dataclass
class IntfIpAddress1:
    dynamic: Dynamic


@dataclass
class OneOfIpV4AddressGlobalVariableDefaultOptionNoDefaultDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpV4AddressGlobalVariableDefaultOptionNoDefaultDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfIpV4AddressGlobalVariableDefaultOptionNoDefaultDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


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
class OneOfIpV4SubnetMaskOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class StaticIpV4AddressPrimary:
    """
    Static IpV4Address Primary
    """

    ip_address: Union[
        OneOfIpV4AddressGlobalVariableDefaultOptionNoDefaultDef1,
        OneOfIpV4AddressGlobalVariableDefaultOptionNoDefaultDef2,
        OneOfIpV4AddressGlobalVariableDefaultOptionNoDefaultDef3,
    ] = _field(metadata={"alias": "ipAddress"})
    subnet_mask: Union[
        OneOfIpV4SubnetMaskOptionsDef1,
        OneOfIpV4SubnetMaskOptionsDef2,
        OneOfIpV4SubnetMaskOptionsDef3,
    ] = _field(metadata={"alias": "subnetMask"})


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
class OneOfIpV4SubnetMaskOptionsWithoutDefault1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpV4SubnetMaskOptionsWithoutDefault2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Ipv4SubnetMaskDef  # pytype: disable=annotation-type-mismatch


@dataclass
class StaticIpV4AddressSecondary:
    ip_address: Union[
        OneOfIpV4AddressOptionsWithoutDefault1, OneOfIpV4AddressOptionsWithoutDefault2
    ] = _field(metadata={"alias": "ipAddress"})
    subnet_mask: Union[
        OneOfIpV4SubnetMaskOptionsWithoutDefault1, OneOfIpV4SubnetMaskOptionsWithoutDefault2
    ] = _field(metadata={"alias": "subnetMask"})


@dataclass
class Static:
    # Static IpV4Address Primary
    static_ip_v4_address_primary: StaticIpV4AddressPrimary = _field(
        metadata={"alias": "staticIpV4AddressPrimary"}
    )
    # Secondary IpV4 Addresses
    static_ip_v4_address_secondary: Optional[List[StaticIpV4AddressSecondary]] = _field(
        default=None, metadata={"alias": "staticIpV4AddressSecondary"}
    )


@dataclass
class IntfIpAddress2:
    static: Static


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
class OneOfListOfIpV4OptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfIperfServerOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfIperfServerOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIperfServerOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfAutoBandwidthDetectOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAutoBandwidthDetectOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAutoBandwidthDetectOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class DhcpClient:
    """
    Enable DHCPv6
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class EthernetDynamic:
    # Enable DHCPv6
    dhcp_client: DhcpClient = _field(metadata={"alias": "dhcpClient"})


@dataclass
class IntfIpV6Address1:
    dynamic: EthernetDynamic


@dataclass
class OneOfIpv6PrefixGlobalVariableDefaultNoValueOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfIpv6PrefixGlobalVariableDefaultNoValueOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpv6PrefixGlobalVariableDefaultNoValueOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class PrimaryIpV6Address:
    """
    Static IpV6Address Primary
    """

    address: Union[
        OneOfIpv6PrefixGlobalVariableDefaultNoValueOptionsDef1,
        OneOfIpv6PrefixGlobalVariableDefaultNoValueOptionsDef2,
        OneOfIpv6PrefixGlobalVariableDefaultNoValueOptionsDef3,
    ]


@dataclass
class EthernetStatic:
    # Static IpV6Address Primary
    primary_ip_v6_address: Optional[PrimaryIpV6Address] = _field(
        default=None, metadata={"alias": "primaryIpV6Address"}
    )


@dataclass
class IntfIpV6Address2:
    static: EthernetStatic


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
    value: str


@dataclass
class OneOfMacAddressOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfMacAddressOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class Arp:
    ip_address: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2] = _field(
        metadata={"alias": "ipAddress"}
    )
    mac_address: Union[OneOfMacAddressOptionsDef1, OneOfMacAddressOptionsDef2] = _field(
        metadata={"alias": "macAddress"}
    )


@dataclass
class OneOfDuplexOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DuplexDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfDuplexOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfDuplexOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfAdvMacAddressOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfAdvMacAddressOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAdvMacAddressOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfMtuOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfMtuOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfMtuOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIntrfMtuOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIntrfMtuOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIntrfMtuOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfTcpMssAdjustOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfTcpMssAdjustOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTcpMssAdjustOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfSpeedOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SpeedDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfSpeedOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfSpeedOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfArpTimeoutOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfArpTimeoutOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfArpTimeoutOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfAutonegotiateOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAutonegotiateOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAutonegotiateOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfMediaTypeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: MediaTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfMediaTypeOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfMediaTypeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfLoadIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfLoadIntervalOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfLoadIntervalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIcmpRedirectDisableOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfIcmpRedirectDisableOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIcmpRedirectDisableOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfIpDirectedBroadcastOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfIpDirectedBroadcastOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpDirectedBroadcastOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class Advanced:
    """
    Advanced Attributes
    """

    arp_timeout: Union[
        OneOfArpTimeoutOptionsDef1, OneOfArpTimeoutOptionsDef2, OneOfArpTimeoutOptionsDef3
    ] = _field(metadata={"alias": "arpTimeout"})
    ip_directed_broadcast: Union[
        OneOfIpDirectedBroadcastOptionsDef1,
        OneOfIpDirectedBroadcastOptionsDef2,
        OneOfIpDirectedBroadcastOptionsDef3,
    ] = _field(metadata={"alias": "ipDirectedBroadcast"})
    ip_mtu: Union[OneOfMtuOptionsDef1, OneOfMtuOptionsDef2, OneOfMtuOptionsDef3] = _field(
        metadata={"alias": "ipMtu"}
    )
    load_interval: Union[
        OneOfLoadIntervalOptionsDef1, OneOfLoadIntervalOptionsDef2, OneOfLoadIntervalOptionsDef3
    ] = _field(metadata={"alias": "loadInterval"})
    autonegotiate: Optional[
        Union[
            OneOfAutonegotiateOptionsDef1,
            OneOfAutonegotiateOptionsDef2,
            OneOfAutonegotiateOptionsDef3,
        ]
    ] = _field(default=None)
    duplex: Optional[
        Union[OneOfDuplexOptionsDef1, OneOfDuplexOptionsDef2, OneOfDuplexOptionsDef3]
    ] = _field(default=None)
    icmp_redirect_disable: Optional[
        Union[
            OneOfIcmpRedirectDisableOptionsDef1,
            OneOfIcmpRedirectDisableOptionsDef2,
            OneOfIcmpRedirectDisableOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "icmpRedirectDisable"})
    intrf_mtu: Optional[
        Union[OneOfIntrfMtuOptionsDef1, OneOfIntrfMtuOptionsDef2, OneOfIntrfMtuOptionsDef3]
    ] = _field(default=None, metadata={"alias": "intrfMtu"})
    mac_address: Optional[
        Union[
            OneOfAdvMacAddressOptionsDef1,
            OneOfAdvMacAddressOptionsDef2,
            OneOfAdvMacAddressOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "macAddress"})
    media_type: Optional[
        Union[OneOfMediaTypeOptionsDef1, OneOfMediaTypeOptionsDef2, OneOfMediaTypeOptionsDef3]
    ] = _field(default=None, metadata={"alias": "mediaType"})
    speed: Optional[Union[OneOfSpeedOptionsDef1, OneOfSpeedOptionsDef2, OneOfSpeedOptionsDef3]] = (
        _field(default=None)
    )
    tcp_mss: Optional[
        Union[
            OneOfTcpMssAdjustOptionsDef1, OneOfTcpMssAdjustOptionsDef2, OneOfTcpMssAdjustOptionsDef3
        ]
    ] = _field(default=None, metadata={"alias": "tcpMss"})


@dataclass
class EthernetData:
    # Advanced Attributes
    advanced: Advanced
    interface_name: Union[OneOfInterfaceNameOptionsDef1, OneOfInterfaceNameOptionsDef2] = _field(
        metadata={"alias": "interfaceName"}
    )
    intf_ip_address: Union[IntfIpAddress1, IntfIpAddress2] = _field(
        metadata={"alias": "intfIpAddress"}
    )
    shutdown: Union[OneOfShutdownOptionsDef1, OneOfShutdownOptionsDef2, OneOfShutdownOptionsDef3]
    # Configure ARP entries
    arp: Optional[List[Arp]] = _field(default=None)
    auto_detect_bandwidth: Optional[
        Union[
            OneOfAutoBandwidthDetectOptionsDef1,
            OneOfAutoBandwidthDetectOptionsDef2,
            OneOfAutoBandwidthDetectOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "autoDetectBandwidth"})
    description: Optional[
        Union[OneOfDescriptionOptionsDef1, OneOfDescriptionOptionsDef2, OneOfDescriptionOptionsDef3]
    ] = _field(default=None)
    dhcp_helper: Optional[
        Union[OneOfListOfIpV4OptionsDef1, OneOfListOfIpV4OptionsDef2, OneOfListOfIpV4OptionsDef3]
    ] = _field(default=None, metadata={"alias": "dhcpHelper"})
    intf_ip_v6_address: Optional[Union[IntfIpV6Address1, IntfIpV6Address2]] = _field(
        default=None, metadata={"alias": "intfIpV6Address"}
    )
    iperf_server: Optional[
        Union[OneOfIperfServerOptionsDef1, OneOfIperfServerOptionsDef2, OneOfIperfServerOptionsDef3]
    ] = _field(default=None, metadata={"alias": "iperfServer"})


@dataclass
class Payload:
    """
    Management VPN Interface Ethernet profile parcel schema for POST request
    """

    data: EthernetData
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
    # Management VPN Interface Ethernet profile parcel schema for POST request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdwanTransportManagementVpnInterfaceEthernetPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateManagementVpnInterfaceEthernetParcelForTransportPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class InterfaceEthernetData:
    # Advanced Attributes
    advanced: Advanced
    interface_name: Union[OneOfInterfaceNameOptionsDef1, OneOfInterfaceNameOptionsDef2] = _field(
        metadata={"alias": "interfaceName"}
    )
    intf_ip_address: Union[IntfIpAddress1, IntfIpAddress2] = _field(
        metadata={"alias": "intfIpAddress"}
    )
    shutdown: Union[OneOfShutdownOptionsDef1, OneOfShutdownOptionsDef2, OneOfShutdownOptionsDef3]
    # Configure ARP entries
    arp: Optional[List[Arp]] = _field(default=None)
    auto_detect_bandwidth: Optional[
        Union[
            OneOfAutoBandwidthDetectOptionsDef1,
            OneOfAutoBandwidthDetectOptionsDef2,
            OneOfAutoBandwidthDetectOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "autoDetectBandwidth"})
    description: Optional[
        Union[OneOfDescriptionOptionsDef1, OneOfDescriptionOptionsDef2, OneOfDescriptionOptionsDef3]
    ] = _field(default=None)
    dhcp_helper: Optional[
        Union[OneOfListOfIpV4OptionsDef1, OneOfListOfIpV4OptionsDef2, OneOfListOfIpV4OptionsDef3]
    ] = _field(default=None, metadata={"alias": "dhcpHelper"})
    intf_ip_v6_address: Optional[Union[IntfIpV6Address1, IntfIpV6Address2]] = _field(
        default=None, metadata={"alias": "intfIpV6Address"}
    )
    iperf_server: Optional[
        Union[OneOfIperfServerOptionsDef1, OneOfIperfServerOptionsDef2, OneOfIperfServerOptionsDef3]
    ] = _field(default=None, metadata={"alias": "iperfServer"})


@dataclass
class CreateManagementVpnInterfaceEthernetParcelForTransportPostRequest:
    """
    Management VPN Interface Ethernet profile parcel schema for POST request
    """

    data: InterfaceEthernetData
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class EthernetOneOfDynamicDhcpDistanceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class EthernetOneOfDynamicDhcpDistanceOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceEthernetDynamic:
    dynamic_dhcp_distance: Union[
        OneOfDynamicDhcpDistanceOptionsDef1,
        EthernetOneOfDynamicDhcpDistanceOptionsDef2,
        EthernetOneOfDynamicDhcpDistanceOptionsDef3,
    ] = _field(metadata={"alias": "dynamicDhcpDistance"})


@dataclass
class EthernetIntfIpAddress1:
    dynamic: InterfaceEthernetDynamic


@dataclass
class EthernetStaticIpV4AddressPrimary:
    """
    Static IpV4Address Primary
    """

    ip_address: Union[
        OneOfIpV4AddressGlobalVariableDefaultOptionNoDefaultDef1,
        OneOfIpV4AddressGlobalVariableDefaultOptionNoDefaultDef2,
        OneOfIpV4AddressGlobalVariableDefaultOptionNoDefaultDef3,
    ] = _field(metadata={"alias": "ipAddress"})
    subnet_mask: Union[
        OneOfIpV4SubnetMaskOptionsDef1,
        OneOfIpV4SubnetMaskOptionsDef2,
        OneOfIpV4SubnetMaskOptionsDef3,
    ] = _field(metadata={"alias": "subnetMask"})


@dataclass
class InterfaceEthernetStatic:
    # Static IpV4Address Primary
    static_ip_v4_address_primary: EthernetStaticIpV4AddressPrimary = _field(
        metadata={"alias": "staticIpV4AddressPrimary"}
    )
    # Secondary IpV4 Addresses
    static_ip_v4_address_secondary: Optional[List[StaticIpV4AddressSecondary]] = _field(
        default=None, metadata={"alias": "staticIpV4AddressSecondary"}
    )


@dataclass
class EthernetIntfIpAddress2:
    static: InterfaceEthernetStatic


@dataclass
class EthernetOneOfListOfIpV4OptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class EthernetOneOfIperfServerOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class EthernetOneOfIpV4AddressOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class EthernetOneOfMacAddressOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class EthernetArp:
    ip_address: Union[OneOfIpV4AddressOptionsDef1, EthernetOneOfIpV4AddressOptionsDef2] = _field(
        metadata={"alias": "ipAddress"}
    )
    mac_address: Union[EthernetOneOfMacAddressOptionsDef1, OneOfMacAddressOptionsDef2] = _field(
        metadata={"alias": "macAddress"}
    )


@dataclass
class EthernetOneOfDuplexOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EthernetDuplexDef  # pytype: disable=annotation-type-mismatch


@dataclass
class EthernetOneOfAdvMacAddressOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class EthernetOneOfMtuOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class EthernetOneOfMtuOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class EthernetOneOfIntrfMtuOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class EthernetOneOfTcpMssAdjustOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class EthernetOneOfSpeedOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EthernetSpeedDef  # pytype: disable=annotation-type-mismatch


@dataclass
class EthernetOneOfArpTimeoutOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class EthernetOneOfArpTimeoutOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class EthernetOneOfMediaTypeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EthernetMediaTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class EthernetOneOfLoadIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class EthernetAdvanced:
    """
    Advanced Attributes
    """

    arp_timeout: Union[
        EthernetOneOfArpTimeoutOptionsDef1,
        OneOfArpTimeoutOptionsDef2,
        EthernetOneOfArpTimeoutOptionsDef3,
    ] = _field(metadata={"alias": "arpTimeout"})
    ip_directed_broadcast: Union[
        OneOfIpDirectedBroadcastOptionsDef1,
        OneOfIpDirectedBroadcastOptionsDef2,
        OneOfIpDirectedBroadcastOptionsDef3,
    ] = _field(metadata={"alias": "ipDirectedBroadcast"})
    ip_mtu: Union[EthernetOneOfMtuOptionsDef1, OneOfMtuOptionsDef2, EthernetOneOfMtuOptionsDef3] = (
        _field(metadata={"alias": "ipMtu"})
    )
    load_interval: Union[
        EthernetOneOfLoadIntervalOptionsDef1,
        OneOfLoadIntervalOptionsDef2,
        OneOfLoadIntervalOptionsDef3,
    ] = _field(metadata={"alias": "loadInterval"})
    autonegotiate: Optional[
        Union[
            OneOfAutonegotiateOptionsDef1,
            OneOfAutonegotiateOptionsDef2,
            OneOfAutonegotiateOptionsDef3,
        ]
    ] = _field(default=None)
    duplex: Optional[
        Union[EthernetOneOfDuplexOptionsDef1, OneOfDuplexOptionsDef2, OneOfDuplexOptionsDef3]
    ] = _field(default=None)
    icmp_redirect_disable: Optional[
        Union[
            OneOfIcmpRedirectDisableOptionsDef1,
            OneOfIcmpRedirectDisableOptionsDef2,
            OneOfIcmpRedirectDisableOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "icmpRedirectDisable"})
    intrf_mtu: Optional[
        Union[EthernetOneOfIntrfMtuOptionsDef1, OneOfIntrfMtuOptionsDef2, OneOfIntrfMtuOptionsDef3]
    ] = _field(default=None, metadata={"alias": "intrfMtu"})
    mac_address: Optional[
        Union[
            EthernetOneOfAdvMacAddressOptionsDef1,
            OneOfAdvMacAddressOptionsDef2,
            OneOfAdvMacAddressOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "macAddress"})
    media_type: Optional[
        Union[
            EthernetOneOfMediaTypeOptionsDef1, OneOfMediaTypeOptionsDef2, OneOfMediaTypeOptionsDef3
        ]
    ] = _field(default=None, metadata={"alias": "mediaType"})
    speed: Optional[
        Union[EthernetOneOfSpeedOptionsDef1, OneOfSpeedOptionsDef2, OneOfSpeedOptionsDef3]
    ] = _field(default=None)
    tcp_mss: Optional[
        Union[
            EthernetOneOfTcpMssAdjustOptionsDef1,
            OneOfTcpMssAdjustOptionsDef2,
            OneOfTcpMssAdjustOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tcpMss"})


@dataclass
class VpnInterfaceEthernetData:
    # Advanced Attributes
    advanced: EthernetAdvanced
    interface_name: Union[OneOfInterfaceNameOptionsDef1, OneOfInterfaceNameOptionsDef2] = _field(
        metadata={"alias": "interfaceName"}
    )
    intf_ip_address: Union[EthernetIntfIpAddress1, EthernetIntfIpAddress2] = _field(
        metadata={"alias": "intfIpAddress"}
    )
    shutdown: Union[OneOfShutdownOptionsDef1, OneOfShutdownOptionsDef2, OneOfShutdownOptionsDef3]
    # Configure ARP entries
    arp: Optional[List[EthernetArp]] = _field(default=None)
    auto_detect_bandwidth: Optional[
        Union[
            OneOfAutoBandwidthDetectOptionsDef1,
            OneOfAutoBandwidthDetectOptionsDef2,
            OneOfAutoBandwidthDetectOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "autoDetectBandwidth"})
    description: Optional[
        Union[OneOfDescriptionOptionsDef1, OneOfDescriptionOptionsDef2, OneOfDescriptionOptionsDef3]
    ] = _field(default=None)
    dhcp_helper: Optional[
        Union[
            OneOfListOfIpV4OptionsDef1,
            EthernetOneOfListOfIpV4OptionsDef2,
            OneOfListOfIpV4OptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "dhcpHelper"})
    intf_ip_v6_address: Optional[Union[IntfIpV6Address1, IntfIpV6Address2]] = _field(
        default=None, metadata={"alias": "intfIpV6Address"}
    )
    iperf_server: Optional[
        Union[
            EthernetOneOfIperfServerOptionsDef1,
            OneOfIperfServerOptionsDef2,
            OneOfIperfServerOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "iperfServer"})


@dataclass
class EthernetPayload:
    """
    Management VPN Interface Ethernet profile parcel schema for PUT request
    """

    data: VpnInterfaceEthernetData
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetSingleSdwanTransportManagementVpnInterfaceEthernetPayload:
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
    # Management VPN Interface Ethernet profile parcel schema for PUT request
    payload: Optional[EthernetPayload] = _field(default=None)


@dataclass
class EditManagementVpnInterfaceEthernetParcelForTransportPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class InterfaceEthernetOneOfDynamicDhcpDistanceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceEthernetOneOfDynamicDhcpDistanceOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VpnInterfaceEthernetDynamic:
    dynamic_dhcp_distance: Union[
        OneOfDynamicDhcpDistanceOptionsDef1,
        InterfaceEthernetOneOfDynamicDhcpDistanceOptionsDef2,
        InterfaceEthernetOneOfDynamicDhcpDistanceOptionsDef3,
    ] = _field(metadata={"alias": "dynamicDhcpDistance"})


@dataclass
class InterfaceEthernetIntfIpAddress1:
    dynamic: VpnInterfaceEthernetDynamic


@dataclass
class InterfaceEthernetStaticIpV4AddressPrimary:
    """
    Static IpV4Address Primary
    """

    ip_address: Union[
        OneOfIpV4AddressGlobalVariableDefaultOptionNoDefaultDef1,
        OneOfIpV4AddressGlobalVariableDefaultOptionNoDefaultDef2,
        OneOfIpV4AddressGlobalVariableDefaultOptionNoDefaultDef3,
    ] = _field(metadata={"alias": "ipAddress"})
    subnet_mask: Union[
        OneOfIpV4SubnetMaskOptionsDef1,
        OneOfIpV4SubnetMaskOptionsDef2,
        OneOfIpV4SubnetMaskOptionsDef3,
    ] = _field(metadata={"alias": "subnetMask"})


@dataclass
class VpnInterfaceEthernetStatic:
    # Static IpV4Address Primary
    static_ip_v4_address_primary: InterfaceEthernetStaticIpV4AddressPrimary = _field(
        metadata={"alias": "staticIpV4AddressPrimary"}
    )
    # Secondary IpV4 Addresses
    static_ip_v4_address_secondary: Optional[List[StaticIpV4AddressSecondary]] = _field(
        default=None, metadata={"alias": "staticIpV4AddressSecondary"}
    )


@dataclass
class InterfaceEthernetIntfIpAddress2:
    static: VpnInterfaceEthernetStatic


@dataclass
class InterfaceEthernetOneOfListOfIpV4OptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class InterfaceEthernetOneOfIperfServerOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class InterfaceEthernetOneOfIpV4AddressOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class InterfaceEthernetOneOfMacAddressOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class InterfaceEthernetArp:
    ip_address: Union[OneOfIpV4AddressOptionsDef1, InterfaceEthernetOneOfIpV4AddressOptionsDef2] = (
        _field(metadata={"alias": "ipAddress"})
    )
    mac_address: Union[InterfaceEthernetOneOfMacAddressOptionsDef1, OneOfMacAddressOptionsDef2] = (
        _field(metadata={"alias": "macAddress"})
    )


@dataclass
class InterfaceEthernetOneOfDuplexOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceEthernetDuplexDef  # pytype: disable=annotation-type-mismatch


@dataclass
class InterfaceEthernetOneOfAdvMacAddressOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class InterfaceEthernetOneOfMtuOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceEthernetOneOfMtuOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceEthernetOneOfIntrfMtuOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceEthernetOneOfTcpMssAdjustOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceEthernetOneOfSpeedOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceEthernetSpeedDef  # pytype: disable=annotation-type-mismatch


@dataclass
class InterfaceEthernetOneOfArpTimeoutOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceEthernetOneOfArpTimeoutOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceEthernetOneOfMediaTypeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceEthernetMediaTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class InterfaceEthernetOneOfLoadIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceEthernetAdvanced:
    """
    Advanced Attributes
    """

    arp_timeout: Union[
        InterfaceEthernetOneOfArpTimeoutOptionsDef1,
        OneOfArpTimeoutOptionsDef2,
        InterfaceEthernetOneOfArpTimeoutOptionsDef3,
    ] = _field(metadata={"alias": "arpTimeout"})
    ip_directed_broadcast: Union[
        OneOfIpDirectedBroadcastOptionsDef1,
        OneOfIpDirectedBroadcastOptionsDef2,
        OneOfIpDirectedBroadcastOptionsDef3,
    ] = _field(metadata={"alias": "ipDirectedBroadcast"})
    ip_mtu: Union[
        InterfaceEthernetOneOfMtuOptionsDef1,
        OneOfMtuOptionsDef2,
        InterfaceEthernetOneOfMtuOptionsDef3,
    ] = _field(metadata={"alias": "ipMtu"})
    load_interval: Union[
        InterfaceEthernetOneOfLoadIntervalOptionsDef1,
        OneOfLoadIntervalOptionsDef2,
        OneOfLoadIntervalOptionsDef3,
    ] = _field(metadata={"alias": "loadInterval"})
    autonegotiate: Optional[
        Union[
            OneOfAutonegotiateOptionsDef1,
            OneOfAutonegotiateOptionsDef2,
            OneOfAutonegotiateOptionsDef3,
        ]
    ] = _field(default=None)
    duplex: Optional[
        Union[
            InterfaceEthernetOneOfDuplexOptionsDef1, OneOfDuplexOptionsDef2, OneOfDuplexOptionsDef3
        ]
    ] = _field(default=None)
    icmp_redirect_disable: Optional[
        Union[
            OneOfIcmpRedirectDisableOptionsDef1,
            OneOfIcmpRedirectDisableOptionsDef2,
            OneOfIcmpRedirectDisableOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "icmpRedirectDisable"})
    intrf_mtu: Optional[
        Union[
            InterfaceEthernetOneOfIntrfMtuOptionsDef1,
            OneOfIntrfMtuOptionsDef2,
            OneOfIntrfMtuOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "intrfMtu"})
    mac_address: Optional[
        Union[
            InterfaceEthernetOneOfAdvMacAddressOptionsDef1,
            OneOfAdvMacAddressOptionsDef2,
            OneOfAdvMacAddressOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "macAddress"})
    media_type: Optional[
        Union[
            InterfaceEthernetOneOfMediaTypeOptionsDef1,
            OneOfMediaTypeOptionsDef2,
            OneOfMediaTypeOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "mediaType"})
    speed: Optional[
        Union[InterfaceEthernetOneOfSpeedOptionsDef1, OneOfSpeedOptionsDef2, OneOfSpeedOptionsDef3]
    ] = _field(default=None)
    tcp_mss: Optional[
        Union[
            InterfaceEthernetOneOfTcpMssAdjustOptionsDef1,
            OneOfTcpMssAdjustOptionsDef2,
            OneOfTcpMssAdjustOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tcpMss"})


@dataclass
class ManagementVpnInterfaceEthernetData:
    # Advanced Attributes
    advanced: InterfaceEthernetAdvanced
    interface_name: Union[OneOfInterfaceNameOptionsDef1, OneOfInterfaceNameOptionsDef2] = _field(
        metadata={"alias": "interfaceName"}
    )
    intf_ip_address: Union[InterfaceEthernetIntfIpAddress1, InterfaceEthernetIntfIpAddress2] = (
        _field(metadata={"alias": "intfIpAddress"})
    )
    shutdown: Union[OneOfShutdownOptionsDef1, OneOfShutdownOptionsDef2, OneOfShutdownOptionsDef3]
    # Configure ARP entries
    arp: Optional[List[InterfaceEthernetArp]] = _field(default=None)
    auto_detect_bandwidth: Optional[
        Union[
            OneOfAutoBandwidthDetectOptionsDef1,
            OneOfAutoBandwidthDetectOptionsDef2,
            OneOfAutoBandwidthDetectOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "autoDetectBandwidth"})
    description: Optional[
        Union[OneOfDescriptionOptionsDef1, OneOfDescriptionOptionsDef2, OneOfDescriptionOptionsDef3]
    ] = _field(default=None)
    dhcp_helper: Optional[
        Union[
            OneOfListOfIpV4OptionsDef1,
            InterfaceEthernetOneOfListOfIpV4OptionsDef2,
            OneOfListOfIpV4OptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "dhcpHelper"})
    intf_ip_v6_address: Optional[Union[IntfIpV6Address1, IntfIpV6Address2]] = _field(
        default=None, metadata={"alias": "intfIpV6Address"}
    )
    iperf_server: Optional[
        Union[
            InterfaceEthernetOneOfIperfServerOptionsDef1,
            OneOfIperfServerOptionsDef2,
            OneOfIperfServerOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "iperfServer"})


@dataclass
class EditManagementVpnInterfaceEthernetParcelForTransportPutRequest:
    """
    Management VPN Interface Ethernet profile parcel schema for PUT request
    """

    data: ManagementVpnInterfaceEthernetData
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
