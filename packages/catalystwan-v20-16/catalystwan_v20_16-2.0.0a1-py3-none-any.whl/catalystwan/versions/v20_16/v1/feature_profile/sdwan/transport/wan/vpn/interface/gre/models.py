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

TunnelModeDef = Literal["ipv4", "ipv6"]

DefaultTunnelModeDef = Literal["ipv4"]

IkeModeDef = Literal["aggressive", "main"]

DefaultIkeModeDef = Literal["main"]

IkeCiphersuiteDef = Literal[
    "aes128-cbc-sha1", "aes128-cbc-sha2", "aes256-cbc-sha1", "aes256-cbc-sha2"
]

DefaultIkeCiphersuiteDef = Literal["aes256-cbc-sha1"]

IkeGroupDef = Literal["14", "15", "16", "19", "2", "20", "21", "24"]

DefaultIkeGroupDef = Literal["16"]

IpsecCiphersuiteDef = Literal[
    "aes256-cbc-sha1",
    "aes256-cbc-sha256",
    "aes256-cbc-sha384",
    "aes256-cbc-sha512",
    "aes256-gcm",
    "null-sha1",
    "null-sha256",
    "null-sha384",
    "null-sha512",
]

DefaultIpsecCiphersuiteDef = Literal["aes256-gcm"]

PerfectForwardSecrecyDef = Literal[
    "group-1",
    "group-14",
    "group-15",
    "group-16",
    "group-19",
    "group-2",
    "group-20",
    "group-21",
    "group-24",
    "group-5",
    "none",
]

DefaultPerfectForwardSecrecyDef = Literal["group-16"]

ApplicationDef = Literal["none", "sig"]


@dataclass
class OneOfIfNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfIfNameOptionsDef2:
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
class OneOfIpV4AddressOptionsWithDefault1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpV4AddressOptionsWithDefault2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfIpV4AddressOptionsWithDefault3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfIpV4SubnetMaskOptionsWithDefault1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpV4SubnetMaskOptionsWithDefault2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Ipv4SubnetMaskDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfIpV4SubnetMaskOptionsWithDefault3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class Ipv4AddressAndMaskWithDefault:
    address: Optional[
        Union[
            OneOfIpV4AddressOptionsWithDefault1,
            OneOfIpV4AddressOptionsWithDefault2,
            OneOfIpV4AddressOptionsWithDefault3,
        ]
    ] = _field(default=None)
    mask: Optional[
        Union[
            OneOfIpV4SubnetMaskOptionsWithDefault1,
            OneOfIpV4SubnetMaskOptionsWithDefault2,
            OneOfIpV4SubnetMaskOptionsWithDefault3,
        ]
    ] = _field(default=None)


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
class OneOfIpv6PrefixOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


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
    value: Optional[bool] = _field(default=None)


@dataclass
class OneOfMultiplexingOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfMultiplexingOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfMultiplexingOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfTunnelProtectionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfTunnelProtectionOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfTunnelModeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: TunnelModeDef


@dataclass
class OneOfTunnelModeOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultTunnelModeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfTunnelSourceOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfTunnelSourceOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTunnelRouteViaOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfTunnelRouteViaOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTunnelRouteViaOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class SourceIp:
    tunnel_source: Union[OneOfTunnelSourceOptionsDef1, OneOfTunnelSourceOptionsDef2] = _field(
        metadata={"alias": "tunnelSource"}
    )
    tunnel_route_via: Optional[
        Union[
            OneOfTunnelRouteViaOptionsDef1,
            OneOfTunnelRouteViaOptionsDef2,
            OneOfTunnelRouteViaOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tunnelRouteVia"})


@dataclass
class TunnelSourceType1:
    source_ip: SourceIp = _field(metadata={"alias": "sourceIp"})


@dataclass
class OneOfTunnelSourceInterfaceOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfTunnelSourceInterfaceOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class SourceNotLoopback:
    tunnel_source_interface: Union[
        OneOfTunnelSourceInterfaceOptionsDef1, OneOfTunnelSourceInterfaceOptionsDef2
    ] = _field(metadata={"alias": "tunnelSourceInterface"})
    tunnel_route_via: Optional[
        Union[
            OneOfTunnelRouteViaOptionsDef1,
            OneOfTunnelRouteViaOptionsDef2,
            OneOfTunnelRouteViaOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tunnelRouteVia"})


@dataclass
class TunnelSourceType2:
    source_not_loopback: SourceNotLoopback = _field(metadata={"alias": "sourceNotLoopback"})


@dataclass
class SourceLoopback:
    tunnel_source_interface: Union[
        OneOfTunnelSourceInterfaceOptionsDef1, OneOfTunnelSourceInterfaceOptionsDef2
    ] = _field(metadata={"alias": "tunnelSourceInterface"})
    tunnel_route_via: Optional[
        Union[
            OneOfTunnelRouteViaOptionsDef1,
            OneOfTunnelRouteViaOptionsDef2,
            OneOfTunnelRouteViaOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tunnelRouteVia"})


@dataclass
class TunnelSourceType3:
    source_loopback: SourceLoopback = _field(metadata={"alias": "sourceLoopback"})


@dataclass
class OneOfIpv6AddressOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfIpv6AddressOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class SourceIpv6:
    tunnel_source_v6: Union[OneOfIpv6AddressOptionsDef1, OneOfIpv6AddressOptionsDef2] = _field(
        metadata={"alias": "tunnelSourceV6"}
    )
    tunnel_route_via: Optional[
        Union[
            OneOfTunnelRouteViaOptionsDef1,
            OneOfTunnelRouteViaOptionsDef2,
            OneOfTunnelRouteViaOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tunnelRouteVia"})


@dataclass
class TunnelSourceType4:
    source_ipv6: SourceIpv6 = _field(metadata={"alias": "sourceIpv6"})


@dataclass
class OneOfTunnelDestinationOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfTunnelDestinationOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


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
class OneOfMtuV6OptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfMtuV6OptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfMtuV6OptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


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
class OneOfTcpMssAdjustV6OptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfTcpMssAdjustV6OptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTcpMssAdjustV6OptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfClearDontFragmentOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfClearDontFragmentOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfClearDontFragmentOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Optional[bool] = _field(default=None)


@dataclass
class OneOfDpdIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfDpdIntervalOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfDpdIntervalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfDpdRetriesOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfDpdRetriesOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfDpdRetriesOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIkeVersionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIkeVersionOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIkeModeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: IkeModeDef


@dataclass
class OneOfIkeModeOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIkeModeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultIkeModeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfIkeRekeyIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIkeRekeyIntervalOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIkeRekeyIntervalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIkeCiphersuiteOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: IkeCiphersuiteDef


@dataclass
class OneOfIkeCiphersuiteOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIkeCiphersuiteOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultIkeCiphersuiteDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfIkeGroupOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: IkeGroupDef


@dataclass
class OneOfIkeGroupOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIkeGroupOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultIkeGroupDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfPreSharedSecretOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfPreSharedSecretOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfPreSharedSecretOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfIkeLocalIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfIkeLocalIdOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIkeLocalIdOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfIkeRemoteIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfIkeRemoteIdOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIkeRemoteIdOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfIpsecRekeyIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIpsecRekeyIntervalOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpsecRekeyIntervalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIpsecReplayWindowOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIpsecReplayWindowOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpsecReplayWindowOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIpsecCiphersuiteOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: IpsecCiphersuiteDef


@dataclass
class OneOfIpsecCiphersuiteOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpsecCiphersuiteOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultIpsecCiphersuiteDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfPerfectForwardSecrecyOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: PerfectForwardSecrecyDef


@dataclass
class OneOfPerfectForwardSecrecyOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfPerfectForwardSecrecyOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultPerfectForwardSecrecyDef  # pytype: disable=annotation-type-mismatch


@dataclass
class Basic1:
    if_name: Union[OneOfIfNameOptionsDef1, OneOfIfNameOptionsDef2] = _field(
        metadata={"alias": "ifName"}
    )
    tunnel_destination: Union[
        OneOfTunnelDestinationOptionsDef1, OneOfTunnelDestinationOptionsDef2
    ] = _field(metadata={"alias": "tunnelDestination"})
    address: Optional[Ipv4AddressAndMaskWithDefault] = _field(default=None)
    clear_dont_fragment: Optional[
        Union[
            OneOfClearDontFragmentOptionsDef1,
            OneOfClearDontFragmentOptionsDef2,
            OneOfClearDontFragmentOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "clearDontFragment"})
    description: Optional[
        Union[OneOfDescriptionOptionsDef1, OneOfDescriptionOptionsDef2, OneOfDescriptionOptionsDef3]
    ] = _field(default=None)
    dpd_interval: Optional[
        Union[OneOfDpdIntervalOptionsDef1, OneOfDpdIntervalOptionsDef2, OneOfDpdIntervalOptionsDef3]
    ] = _field(default=None, metadata={"alias": "dpdInterval"})
    dpd_retries: Optional[
        Union[OneOfDpdRetriesOptionsDef1, OneOfDpdRetriesOptionsDef2, OneOfDpdRetriesOptionsDef3]
    ] = _field(default=None, metadata={"alias": "dpdRetries"})
    ike_ciphersuite: Optional[
        Union[
            OneOfIkeCiphersuiteOptionsDef1,
            OneOfIkeCiphersuiteOptionsDef2,
            OneOfIkeCiphersuiteOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ikeCiphersuite"})
    ike_group: Optional[
        Union[OneOfIkeGroupOptionsDef1, OneOfIkeGroupOptionsDef2, OneOfIkeGroupOptionsDef3]
    ] = _field(default=None, metadata={"alias": "ikeGroup"})
    ike_local_id: Optional[
        Union[OneOfIkeLocalIdOptionsDef1, OneOfIkeLocalIdOptionsDef2, OneOfIkeLocalIdOptionsDef3]
    ] = _field(default=None, metadata={"alias": "ikeLocalId"})
    ike_mode: Optional[
        Union[OneOfIkeModeOptionsDef1, OneOfIkeModeOptionsDef2, OneOfIkeModeOptionsDef3]
    ] = _field(default=None, metadata={"alias": "ikeMode"})
    ike_rekey_interval: Optional[
        Union[
            OneOfIkeRekeyIntervalOptionsDef1,
            OneOfIkeRekeyIntervalOptionsDef2,
            OneOfIkeRekeyIntervalOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ikeRekeyInterval"})
    ike_remote_id: Optional[
        Union[OneOfIkeRemoteIdOptionsDef1, OneOfIkeRemoteIdOptionsDef2, OneOfIkeRemoteIdOptionsDef3]
    ] = _field(default=None, metadata={"alias": "ikeRemoteId"})
    ike_version: Optional[Union[OneOfIkeVersionOptionsDef1, OneOfIkeVersionOptionsDef2]] = _field(
        default=None, metadata={"alias": "ikeVersion"}
    )
    ipsec_ciphersuite: Optional[
        Union[
            OneOfIpsecCiphersuiteOptionsDef1,
            OneOfIpsecCiphersuiteOptionsDef2,
            OneOfIpsecCiphersuiteOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ipsecCiphersuite"})
    ipsec_rekey_interval: Optional[
        Union[
            OneOfIpsecRekeyIntervalOptionsDef1,
            OneOfIpsecRekeyIntervalOptionsDef2,
            OneOfIpsecRekeyIntervalOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ipsecRekeyInterval"})
    ipsec_replay_window: Optional[
        Union[
            OneOfIpsecReplayWindowOptionsDef1,
            OneOfIpsecReplayWindowOptionsDef2,
            OneOfIpsecReplayWindowOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ipsecReplayWindow"})
    ipv6_address: Optional[
        Union[OneOfIpv6PrefixOptionsDef1, OneOfIpv6PrefixOptionsDef2, OneOfIpv6PrefixOptionsDef3]
    ] = _field(default=None, metadata={"alias": "ipv6Address"})
    mtu: Optional[Union[OneOfMtuOptionsDef1, OneOfMtuOptionsDef2, OneOfMtuOptionsDef3]] = _field(
        default=None
    )
    mtu_v6: Optional[Union[OneOfMtuV6OptionsDef1, OneOfMtuV6OptionsDef2, OneOfMtuV6OptionsDef3]] = (
        _field(default=None, metadata={"alias": "mtuV6"})
    )
    multiplexing: Optional[
        Union[
            OneOfMultiplexingOptionsDef1, OneOfMultiplexingOptionsDef2, OneOfMultiplexingOptionsDef3
        ]
    ] = _field(default=None)
    perfect_forward_secrecy: Optional[
        Union[
            OneOfPerfectForwardSecrecyOptionsDef1,
            OneOfPerfectForwardSecrecyOptionsDef2,
            OneOfPerfectForwardSecrecyOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "perfectForwardSecrecy"})
    pre_shared_secret: Optional[
        Union[
            OneOfPreSharedSecretOptionsDef1,
            OneOfPreSharedSecretOptionsDef2,
            OneOfPreSharedSecretOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "preSharedSecret"})
    shutdown: Optional[
        Union[OneOfShutdownOptionsDef1, OneOfShutdownOptionsDef2, OneOfShutdownOptionsDef3]
    ] = _field(default=None)
    tcp_mss_adjust: Optional[
        Union[
            OneOfTcpMssAdjustOptionsDef1, OneOfTcpMssAdjustOptionsDef2, OneOfTcpMssAdjustOptionsDef3
        ]
    ] = _field(default=None, metadata={"alias": "tcpMssAdjust"})
    tcp_mss_adjust_v6: Optional[
        Union[
            OneOfTcpMssAdjustV6OptionsDef1,
            OneOfTcpMssAdjustV6OptionsDef2,
            OneOfTcpMssAdjustV6OptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tcpMssAdjustV6"})
    tunnel_destination_v6: Optional[
        Union[OneOfIpv6AddressOptionsDef1, OneOfIpv6AddressOptionsDef2]
    ] = _field(default=None, metadata={"alias": "tunnelDestinationV6"})
    tunnel_mode: Optional[Union[OneOfTunnelModeOptionsDef1, OneOfTunnelModeOptionsDef2]] = _field(
        default=None, metadata={"alias": "tunnelMode"}
    )
    tunnel_protection: Optional[
        Union[OneOfTunnelProtectionOptionsDef1, OneOfTunnelProtectionOptionsDef2]
    ] = _field(default=None, metadata={"alias": "tunnelProtection"})
    tunnel_source_type: Optional[
        Union[TunnelSourceType1, TunnelSourceType2, TunnelSourceType3, TunnelSourceType4]
    ] = _field(default=None, metadata={"alias": "tunnelSourceType"})


@dataclass
class Basic2:
    if_name: Union[OneOfIfNameOptionsDef1, OneOfIfNameOptionsDef2] = _field(
        metadata={"alias": "ifName"}
    )
    tunnel_destination_v6: Union[OneOfIpv6AddressOptionsDef1, OneOfIpv6AddressOptionsDef2] = _field(
        metadata={"alias": "tunnelDestinationV6"}
    )
    address: Optional[Ipv4AddressAndMaskWithDefault] = _field(default=None)
    clear_dont_fragment: Optional[
        Union[
            OneOfClearDontFragmentOptionsDef1,
            OneOfClearDontFragmentOptionsDef2,
            OneOfClearDontFragmentOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "clearDontFragment"})
    description: Optional[
        Union[OneOfDescriptionOptionsDef1, OneOfDescriptionOptionsDef2, OneOfDescriptionOptionsDef3]
    ] = _field(default=None)
    dpd_interval: Optional[
        Union[OneOfDpdIntervalOptionsDef1, OneOfDpdIntervalOptionsDef2, OneOfDpdIntervalOptionsDef3]
    ] = _field(default=None, metadata={"alias": "dpdInterval"})
    dpd_retries: Optional[
        Union[OneOfDpdRetriesOptionsDef1, OneOfDpdRetriesOptionsDef2, OneOfDpdRetriesOptionsDef3]
    ] = _field(default=None, metadata={"alias": "dpdRetries"})
    ike_ciphersuite: Optional[
        Union[
            OneOfIkeCiphersuiteOptionsDef1,
            OneOfIkeCiphersuiteOptionsDef2,
            OneOfIkeCiphersuiteOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ikeCiphersuite"})
    ike_group: Optional[
        Union[OneOfIkeGroupOptionsDef1, OneOfIkeGroupOptionsDef2, OneOfIkeGroupOptionsDef3]
    ] = _field(default=None, metadata={"alias": "ikeGroup"})
    ike_local_id: Optional[
        Union[OneOfIkeLocalIdOptionsDef1, OneOfIkeLocalIdOptionsDef2, OneOfIkeLocalIdOptionsDef3]
    ] = _field(default=None, metadata={"alias": "ikeLocalId"})
    ike_mode: Optional[
        Union[OneOfIkeModeOptionsDef1, OneOfIkeModeOptionsDef2, OneOfIkeModeOptionsDef3]
    ] = _field(default=None, metadata={"alias": "ikeMode"})
    ike_rekey_interval: Optional[
        Union[
            OneOfIkeRekeyIntervalOptionsDef1,
            OneOfIkeRekeyIntervalOptionsDef2,
            OneOfIkeRekeyIntervalOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ikeRekeyInterval"})
    ike_remote_id: Optional[
        Union[OneOfIkeRemoteIdOptionsDef1, OneOfIkeRemoteIdOptionsDef2, OneOfIkeRemoteIdOptionsDef3]
    ] = _field(default=None, metadata={"alias": "ikeRemoteId"})
    ike_version: Optional[Union[OneOfIkeVersionOptionsDef1, OneOfIkeVersionOptionsDef2]] = _field(
        default=None, metadata={"alias": "ikeVersion"}
    )
    ipsec_ciphersuite: Optional[
        Union[
            OneOfIpsecCiphersuiteOptionsDef1,
            OneOfIpsecCiphersuiteOptionsDef2,
            OneOfIpsecCiphersuiteOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ipsecCiphersuite"})
    ipsec_rekey_interval: Optional[
        Union[
            OneOfIpsecRekeyIntervalOptionsDef1,
            OneOfIpsecRekeyIntervalOptionsDef2,
            OneOfIpsecRekeyIntervalOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ipsecRekeyInterval"})
    ipsec_replay_window: Optional[
        Union[
            OneOfIpsecReplayWindowOptionsDef1,
            OneOfIpsecReplayWindowOptionsDef2,
            OneOfIpsecReplayWindowOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ipsecReplayWindow"})
    ipv6_address: Optional[
        Union[OneOfIpv6PrefixOptionsDef1, OneOfIpv6PrefixOptionsDef2, OneOfIpv6PrefixOptionsDef3]
    ] = _field(default=None, metadata={"alias": "ipv6Address"})
    mtu: Optional[Union[OneOfMtuOptionsDef1, OneOfMtuOptionsDef2, OneOfMtuOptionsDef3]] = _field(
        default=None
    )
    mtu_v6: Optional[Union[OneOfMtuV6OptionsDef1, OneOfMtuV6OptionsDef2, OneOfMtuV6OptionsDef3]] = (
        _field(default=None, metadata={"alias": "mtuV6"})
    )
    multiplexing: Optional[
        Union[
            OneOfMultiplexingOptionsDef1, OneOfMultiplexingOptionsDef2, OneOfMultiplexingOptionsDef3
        ]
    ] = _field(default=None)
    perfect_forward_secrecy: Optional[
        Union[
            OneOfPerfectForwardSecrecyOptionsDef1,
            OneOfPerfectForwardSecrecyOptionsDef2,
            OneOfPerfectForwardSecrecyOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "perfectForwardSecrecy"})
    pre_shared_secret: Optional[
        Union[
            OneOfPreSharedSecretOptionsDef1,
            OneOfPreSharedSecretOptionsDef2,
            OneOfPreSharedSecretOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "preSharedSecret"})
    shutdown: Optional[
        Union[OneOfShutdownOptionsDef1, OneOfShutdownOptionsDef2, OneOfShutdownOptionsDef3]
    ] = _field(default=None)
    tcp_mss_adjust: Optional[
        Union[
            OneOfTcpMssAdjustOptionsDef1, OneOfTcpMssAdjustOptionsDef2, OneOfTcpMssAdjustOptionsDef3
        ]
    ] = _field(default=None, metadata={"alias": "tcpMssAdjust"})
    tcp_mss_adjust_v6: Optional[
        Union[
            OneOfTcpMssAdjustV6OptionsDef1,
            OneOfTcpMssAdjustV6OptionsDef2,
            OneOfTcpMssAdjustV6OptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tcpMssAdjustV6"})
    tunnel_destination: Optional[
        Union[OneOfTunnelDestinationOptionsDef1, OneOfTunnelDestinationOptionsDef2]
    ] = _field(default=None, metadata={"alias": "tunnelDestination"})
    tunnel_mode: Optional[Union[OneOfTunnelModeOptionsDef1, OneOfTunnelModeOptionsDef2]] = _field(
        default=None, metadata={"alias": "tunnelMode"}
    )
    tunnel_protection: Optional[
        Union[OneOfTunnelProtectionOptionsDef1, OneOfTunnelProtectionOptionsDef2]
    ] = _field(default=None, metadata={"alias": "tunnelProtection"})
    tunnel_source_type: Optional[
        Union[TunnelSourceType1, TunnelSourceType2, TunnelSourceType3, TunnelSourceType4]
    ] = _field(default=None, metadata={"alias": "tunnelSourceType"})


@dataclass
class OneOfApplicationOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ApplicationDef


@dataclass
class OneOfApplicationOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class Advanced:
    """
    advanced
    """

    application: Optional[Union[OneOfApplicationOptionsDef1, OneOfApplicationOptionsDef2]] = _field(
        default=None
    )


@dataclass
class GreData:
    # basic configuration
    basic: Union[Basic1, Basic2]
    advanced: Optional[Advanced] = _field(default=None)


@dataclass
class Payload:
    """
    WAN VPN Interface GRE profile parcel schema for request
    """

    data: GreData
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
    # WAN VPN Interface GRE profile parcel schema for request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdwanTransportWanVpnInterfaceGrePayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateWanVpnInterfaceGreParcelForTransportPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class InterfaceGreData:
    # basic configuration
    basic: Union[Basic1, Basic2]
    advanced: Optional[Advanced] = _field(default=None)


@dataclass
class CreateWanVpnInterfaceGreParcelForTransportPostRequest:
    """
    WAN VPN Interface GRE profile parcel schema for request
    """

    data: InterfaceGreData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class GetSingleSdwanTransportWanVpnInterfaceGrePayload:
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
    # WAN VPN Interface GRE profile parcel schema for request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class EditWanVpnInterfaceGreParcelForTransportPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class VpnInterfaceGreData:
    # basic configuration
    basic: Union[Basic1, Basic2]
    advanced: Optional[Advanced] = _field(default=None)


@dataclass
class EditWanVpnInterfaceGreParcelForTransportPutRequest:
    """
    WAN VPN Interface GRE profile parcel schema for request
    """

    data: VpnInterfaceGreData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)
