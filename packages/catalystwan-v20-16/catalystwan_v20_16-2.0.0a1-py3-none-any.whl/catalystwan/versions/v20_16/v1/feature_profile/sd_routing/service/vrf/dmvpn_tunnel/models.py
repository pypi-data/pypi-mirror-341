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

ModeTypeDef = Literal["ipv4", "ipv6"]


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
class Overlay:
    """
    overlay Attributes
    """

    ipv4_address: Optional[Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2]] = (
        _field(default=None, metadata={"alias": "ipv4Address"})
    )
    ipv6_prefix: Optional[
        Union[
            OneOfIpv6PrefixGlobalVariableWithoutDefault1,
            OneOfIpv6PrefixGlobalVariableWithoutDefault2,
        ]
    ] = _field(default=None, metadata={"alias": "ipv6Prefix"})
    subnet_mask: Optional[Union[OneOfIpV4SubnetMaskOptionsDef1, OneOfIpV4SubnetMaskOptionsDef2]] = (
        _field(default=None, metadata={"alias": "subnetMask"})
    )


@dataclass
class OneOfTunnelKeyOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfTunnelKeyOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTunnelKeyOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfModeTypeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ModeTypeDef


@dataclass
class OneOfInterfaceNameV2OptionsNoDefaultDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfInterfaceNameV2OptionsNoDefaultDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfVrfOptionsWithoutDefault1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfVrfOptionsWithoutDefault2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class TunnelVrf1:
    vrf: Union[OneOfVrfOptionsWithoutDefault1, OneOfVrfOptionsWithoutDefault2]


@dataclass
class BooleanDefaultTrueOptionsDef:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class TunnelVrf2:
    global_vrf: BooleanDefaultTrueOptionsDef = _field(metadata={"alias": "globalVrf"})


@dataclass
class Underlay:
    """
    BFD Attributes
    """

    tunnel_source: Union[
        OneOfInterfaceNameV2OptionsNoDefaultDef1, OneOfInterfaceNameV2OptionsNoDefaultDef2
    ] = _field(metadata={"alias": "tunnelSource"})
    type_: OneOfModeTypeOptionsDef = _field(metadata={"alias": "type"})
    tunnel_vrf: Optional[Union[TunnelVrf1, TunnelVrf2]] = _field(
        default=None, metadata={"alias": "tunnelVrf"}
    )


@dataclass
class RefId:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfRefIdOptionsWithDefault1:
    ref_id: RefId = _field(metadata={"alias": "refId"})


@dataclass
class OneOfRefIdOptionsWithDefault2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class TunnelAttribute:
    """
    DMVPN tunnel basic Attributes
    """

    interface_name: Union[OneOfIfNameOptionsDef1, OneOfIfNameOptionsDef2] = _field(
        metadata={"alias": "interfaceName"}
    )
    ipsec_profile: Union[OneOfRefIdOptionsWithDefault1, OneOfRefIdOptionsWithDefault2] = _field(
        metadata={"alias": "ipsecProfile"}
    )
    # overlay Attributes
    overlay: Overlay
    tunnel_key: Union[
        OneOfTunnelKeyOptionsDef1, OneOfTunnelKeyOptionsDef2, OneOfTunnelKeyOptionsDef3
    ] = _field(metadata={"alias": "tunnelKey"})
    # BFD Attributes
    underlay: Underlay
    description: Optional[
        Union[OneOfVpnNameOptionsDef1, OneOfVpnNameOptionsDef2, OneOfVpnNameOptionsDef3]
    ] = _field(default=None)
    shutdown: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class OneOfNetworkIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNetworkIdOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfHoldTimeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfHoldTimeOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfHoldTimeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfKeyAuthKeyOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfKeyAuthKeyOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfKeyAuthKeyOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfIpv4PrefixOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfIpv4PrefixOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class NhrpSummaryMap:
    ipv4_prefix: Union[OneOfIpv4PrefixOptionsDef1, OneOfIpv4PrefixOptionsDef2] = _field(
        metadata={"alias": "ipv4Prefix"}
    )


@dataclass
class Ipv4:
    """
    ipv4 Attributes
    """

    # IPv4 NHS summary Map
    nhrp_summary_map: Optional[List[NhrpSummaryMap]] = _field(
        default=None, metadata={"alias": "nhrpSummaryMap"}
    )


@dataclass
class DmvpnTunnelNhrpSummaryMap:
    ipv6_prefix: Union[
        OneOfIpv6PrefixGlobalVariableWithoutDefault1, OneOfIpv6PrefixGlobalVariableWithoutDefault2
    ] = _field(metadata={"alias": "ipv6Prefix"})


@dataclass
class Ipv6:
    """
    ipv6 Attributes
    """

    # IPv6 NHS summary Map
    nhrp_summary_map: Optional[List[DmvpnTunnelNhrpSummaryMap]] = _field(
        default=None, metadata={"alias": "nhrpSummaryMap"}
    )


@dataclass
class Common:
    """
    common Attributes
    """

    network_id: Union[OneOfNetworkIdOptionsDef1, OneOfNetworkIdOptionsDef2] = _field(
        metadata={"alias": "networkId"}
    )
    auth_key: Optional[
        Union[OneOfKeyAuthKeyOptionsDef1, OneOfKeyAuthKeyOptionsDef2, OneOfKeyAuthKeyOptionsDef3]
    ] = _field(default=None, metadata={"alias": "authKey"})
    hold_time: Optional[
        Union[OneOfHoldTimeOptionsDef1, OneOfHoldTimeOptionsDef2, OneOfHoldTimeOptionsDef3]
    ] = _field(default=None, metadata={"alias": "holdTime"})
    # ipv4 Attributes
    ipv4: Optional[Ipv4] = _field(default=None)
    # ipv6 Attributes
    ipv6: Optional[Ipv6] = _field(default=None)


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
class Hub:
    """
    hub Attributes
    """

    redirect: Optional[
        Union[
            OneOfOnBooleanDefaultTrueOptionsDef1,
            OneOfOnBooleanDefaultTrueOptionsDef2,
            OneOfOnBooleanDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class NbmaMap:
    nbma_ip_address: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2] = _field(
        metadata={"alias": "nbmaIpAddress"}
    )
    nhs_ip_address: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2] = _field(
        metadata={"alias": "nhsIpAddress"}
    )
    multicast: Optional[
        Union[
            OneOfOnBooleanDefaultTrueOptionsDef1,
            OneOfOnBooleanDefaultTrueOptionsDef2,
            OneOfOnBooleanDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class DmvpnTunnelIpv4:
    """
    ipv4 Attributes
    """

    # IPv4 NHS NBMA Map
    nbma_map: Optional[List[NbmaMap]] = _field(default=None, metadata={"alias": "nbmaMap"})


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
class DmvpnTunnelNbmaMap:
    nbma_ip_address: Union[OneOfIpAddressOptionsDef1, OneOfIpAddressOptionsDef2] = _field(
        metadata={"alias": "nbmaIpAddress"}
    )
    nhs_ip_address: Union[
        OneOfIpv6AddrGlobalVariableOptionsDef1, OneOfIpv6AddrGlobalVariableOptionsDef2
    ] = _field(metadata={"alias": "nhsIpAddress"})
    multicast: Optional[
        Union[
            OneOfOnBooleanDefaultTrueOptionsDef1,
            OneOfOnBooleanDefaultTrueOptionsDef2,
            OneOfOnBooleanDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class DmvpnTunnelIpv6:
    """
    ipv6 Attributes
    """

    # IPv6 NHS NBMA Map
    nbma_map: Optional[List[DmvpnTunnelNbmaMap]] = _field(
        default=None, metadata={"alias": "nbmaMap"}
    )


@dataclass
class Spoke:
    """
    spoke Attributes
    """

    # ipv4 Attributes
    ipv4: Optional[DmvpnTunnelIpv4] = _field(default=None)
    # ipv6 Attributes
    ipv6: Optional[DmvpnTunnelIpv6] = _field(default=None)
    shortcut: Optional[
        Union[
            OneOfOnBooleanDefaultTrueOptionsDef1,
            OneOfOnBooleanDefaultTrueOptionsDef2,
            OneOfOnBooleanDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class Nhrp:
    """
    NHRP
    """

    # common Attributes
    common: Common
    # hub Attributes
    hub: Optional[Hub] = _field(default=None)
    # spoke Attributes
    spoke: Optional[Spoke] = _field(default=None)


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
class OneOfTransmitIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfTransmitIntervalOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTransmitIntervalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfReceiveIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfReceiveIntervalOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfReceiveIntervalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfMultiplierOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfMultiplierOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfMultiplierOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class Bfd:
    """
    BFD Attributes
    """

    enable: Union[
        OneOfOnBooleanDefaultFalseNoVariableOptionsDef1,
        OneOfOnBooleanDefaultFalseNoVariableOptionsDef2,
    ]
    multiplier: Optional[
        Union[OneOfMultiplierOptionsDef1, OneOfMultiplierOptionsDef2, OneOfMultiplierOptionsDef3]
    ] = _field(default=None)
    receive_interval: Optional[
        Union[
            OneOfReceiveIntervalOptionsDef1,
            OneOfReceiveIntervalOptionsDef2,
            OneOfReceiveIntervalOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "receiveInterval"})
    transmit_interval: Optional[
        Union[
            OneOfTransmitIntervalOptionsDef1,
            OneOfTransmitIntervalOptionsDef2,
            OneOfTransmitIntervalOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "transmitInterval"})


@dataclass
class OneOfIpv4MtuOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIpv4MtuOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpv4MtuOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIpv6MtuOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIpv6MtuOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpv6MtuOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIpv4TcpMssMtuOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIpv4TcpMssMtuOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpv4TcpMssMtuOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIpv6TcpMssMtuOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIpv6TcpMssMtuOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpv6TcpMssMtuOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfDelayOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfDelayOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfDelayOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfBandwidthOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfBandwidthOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfBandwidthOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class Advanced:
    """
    DMVPN tunnel advance Attributes
    """

    bandwidth: Optional[
        Union[OneOfBandwidthOptionsDef1, OneOfBandwidthOptionsDef2, OneOfBandwidthOptionsDef3]
    ] = _field(default=None)
    delay: Optional[Union[OneOfDelayOptionsDef1, OneOfDelayOptionsDef2, OneOfDelayOptionsDef3]] = (
        _field(default=None)
    )
    ipv4_mtu: Optional[
        Union[OneOfIpv4MtuOptionsDef1, OneOfIpv4MtuOptionsDef2, OneOfIpv4MtuOptionsDef3]
    ] = _field(default=None, metadata={"alias": "ipv4Mtu"})
    ipv4_tcp_mss: Optional[
        Union[
            OneOfIpv4TcpMssMtuOptionsDef1,
            OneOfIpv4TcpMssMtuOptionsDef2,
            OneOfIpv4TcpMssMtuOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ipv4TcpMss"})
    ipv6_mtu: Optional[
        Union[OneOfIpv6MtuOptionsDef1, OneOfIpv6MtuOptionsDef2, OneOfIpv6MtuOptionsDef3]
    ] = _field(default=None, metadata={"alias": "ipv6Mtu"})
    ipv6_tcp_mss: Optional[
        Union[
            OneOfIpv6TcpMssMtuOptionsDef1,
            OneOfIpv6TcpMssMtuOptionsDef2,
            OneOfIpv6TcpMssMtuOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ipv6TcpMss"})


@dataclass
class DmvpnTunnelData:
    # NHRP
    nhrp: Nhrp
    # DMVPN tunnel basic Attributes
    tunnel_attribute: TunnelAttribute = _field(metadata={"alias": "tunnelAttribute"})
    # DMVPN tunnel advance Attributes
    advanced: Optional[Advanced] = _field(default=None)
    # BFD Attributes
    bfd: Optional[Bfd] = _field(default=None)


@dataclass
class Payload:
    """
    SD-Routing DMVPN tunnel feature schema
    """

    data: DmvpnTunnelData
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
    # SD-Routing DMVPN tunnel feature schema
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdRoutingServiceVrfLanDmvpnTunnelPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateSdroutingServiceVrfDmvpnTunnelFeaturePostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class VrfDmvpnTunnelData:
    # NHRP
    nhrp: Nhrp
    # DMVPN tunnel basic Attributes
    tunnel_attribute: TunnelAttribute = _field(metadata={"alias": "tunnelAttribute"})
    # DMVPN tunnel advance Attributes
    advanced: Optional[Advanced] = _field(default=None)
    # BFD Attributes
    bfd: Optional[Bfd] = _field(default=None)


@dataclass
class CreateSdroutingServiceVrfDmvpnTunnelFeaturePostRequest:
    """
    SD-Routing DMVPN tunnel feature schema
    """

    data: VrfDmvpnTunnelData
    name: str
    # Set the feature description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetSingleSdRoutingServiceVrfLanDmvpnTunnelPayload:
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
    # SD-Routing DMVPN tunnel feature schema
    payload: Optional[Payload] = _field(default=None)


@dataclass
class EditSdroutingServiceVrfDmvpnTunnelFeaturePutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class ServiceVrfDmvpnTunnelData:
    # NHRP
    nhrp: Nhrp
    # DMVPN tunnel basic Attributes
    tunnel_attribute: TunnelAttribute = _field(metadata={"alias": "tunnelAttribute"})
    # DMVPN tunnel advance Attributes
    advanced: Optional[Advanced] = _field(default=None)
    # BFD Attributes
    bfd: Optional[Bfd] = _field(default=None)


@dataclass
class EditSdroutingServiceVrfDmvpnTunnelFeaturePutRequest:
    """
    SD-Routing DMVPN tunnel feature schema
    """

    data: ServiceVrfDmvpnTunnelData
    name: str
    # Set the feature description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
