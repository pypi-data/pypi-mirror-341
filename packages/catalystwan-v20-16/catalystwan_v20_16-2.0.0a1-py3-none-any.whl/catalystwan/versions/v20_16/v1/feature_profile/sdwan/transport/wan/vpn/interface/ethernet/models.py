# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

VariableOptionTypeDef = Literal["variable"]

DefaultOptionTypeDef = Literal["default"]

PortChannelLoadBalanceDef = Literal["flow", "vlan"]

PortChannelLacpModeDef = Literal["active", "passive"]

PortChannelLacpModeActiveDef = Literal["active"]

LacpRateDef = Literal["fast", "normal"]

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

ModeDef = Literal["hub", "spoke"]

CarrierDef = Literal[
    "carrier1",
    "carrier2",
    "carrier3",
    "carrier4",
    "carrier5",
    "carrier6",
    "carrier7",
    "carrier8",
    "default",
]

DefaultCarrierDef = Literal["default"]

ColorDef = Literal[
    "3g",
    "biz-internet",
    "blue",
    "bronze",
    "custom1",
    "custom2",
    "custom3",
    "default",
    "gold",
    "green",
    "lte",
    "metro-ethernet",
    "mpls",
    "private1",
    "private2",
    "private3",
    "private4",
    "private5",
    "private6",
    "public-internet",
    "red",
    "silver",
]

Value = Literal["mpls"]

EncapsulationEncapDef = Literal["gre", "ipsec"]

CoreRegionDef = Literal["core", "core-shared"]

DefaultCoreRegionDef = Literal["core-shared"]

SecondaryRegionDef = Literal["secondary-only", "secondary-shared"]

DefaultSecondaryRegionDef = Literal["secondary-shared"]

NatChoiceDef = Literal["interface", "loopback", "pool"]

DefaultNatChoiceDef = Literal["interface"]

StaticNatDirectionDef = Literal["inside"]

DefaultStaticNatDirectionDef = Literal["inside"]

StaticPortForwardProtocolDef = Literal["tcp", "udp"]

DuplexDef = Literal["auto", "full", "half"]

SpeedDef = Literal["10", "100", "1000", "10000", "2500", "25000"]

MediaTypeDef = Literal["auto-select", "rj45", "sfp"]

EthernetPortChannelLoadBalanceDef = Literal["flow", "vlan"]

EthernetPortChannelLacpModeDef = Literal["active", "passive"]

EthernetPortChannelLacpModeActiveDef = Literal["active"]

EthernetLacpRateDef = Literal["fast", "normal"]

InterfaceEthernetPortChannelLoadBalanceDef = Literal["flow", "vlan"]

EthernetModeDef = Literal["hub", "spoke"]

EthernetCarrierDef = Literal[
    "carrier1",
    "carrier2",
    "carrier3",
    "carrier4",
    "carrier5",
    "carrier6",
    "carrier7",
    "carrier8",
    "default",
]

EthernetDefaultCarrierDef = Literal["default"]

EthernetColorDef = Literal[
    "3g",
    "biz-internet",
    "blue",
    "bronze",
    "custom1",
    "custom2",
    "custom3",
    "default",
    "gold",
    "green",
    "lte",
    "metro-ethernet",
    "mpls",
    "private1",
    "private2",
    "private3",
    "private4",
    "private5",
    "private6",
    "public-internet",
    "red",
    "silver",
]

EthernetEncapsulationEncapDef = Literal["gre", "ipsec"]

EthernetCoreRegionDef = Literal["core", "core-shared"]

EthernetDefaultCoreRegionDef = Literal["core-shared"]

EthernetSecondaryRegionDef = Literal["secondary-only", "secondary-shared"]

EthernetDefaultSecondaryRegionDef = Literal["secondary-shared"]

EthernetNatChoiceDef = Literal["interface", "loopback", "pool"]

EthernetDefaultNatChoiceDef = Literal["interface"]

EthernetStaticNatDirectionDef = Literal["inside"]

EthernetDefaultStaticNatDirectionDef = Literal["inside"]

EthernetStaticPortForwardProtocolDef = Literal["tcp", "udp"]

InterfaceEthernetStaticNatDirectionDef = Literal["inside"]

InterfaceEthernetDefaultStaticNatDirectionDef = Literal["inside"]

EthernetDuplexDef = Literal["auto", "full", "half"]

EthernetSpeedDef = Literal["10", "100", "1000", "10000", "2500", "25000"]

EthernetMediaTypeDef = Literal["auto-select", "rj45", "sfp"]

VpnInterfaceEthernetPortChannelLoadBalanceDef = Literal["flow", "vlan"]

InterfaceEthernetPortChannelLacpModeDef = Literal["active", "passive"]

InterfaceEthernetPortChannelLacpModeActiveDef = Literal["active"]

InterfaceEthernetLacpRateDef = Literal["fast", "normal"]

WanVpnInterfaceEthernetPortChannelLoadBalanceDef = Literal["flow", "vlan"]

InterfaceEthernetModeDef = Literal["hub", "spoke"]

InterfaceEthernetCarrierDef = Literal[
    "carrier1",
    "carrier2",
    "carrier3",
    "carrier4",
    "carrier5",
    "carrier6",
    "carrier7",
    "carrier8",
    "default",
]

InterfaceEthernetDefaultCarrierDef = Literal["default"]

InterfaceEthernetColorDef = Literal[
    "3g",
    "biz-internet",
    "blue",
    "bronze",
    "custom1",
    "custom2",
    "custom3",
    "default",
    "gold",
    "green",
    "lte",
    "metro-ethernet",
    "mpls",
    "private1",
    "private2",
    "private3",
    "private4",
    "private5",
    "private6",
    "public-internet",
    "red",
    "silver",
]

InterfaceEthernetEncapsulationEncapDef = Literal["gre", "ipsec"]

InterfaceEthernetCoreRegionDef = Literal["core", "core-shared"]

InterfaceEthernetDefaultCoreRegionDef = Literal["core-shared"]

InterfaceEthernetSecondaryRegionDef = Literal["secondary-only", "secondary-shared"]

InterfaceEthernetDefaultSecondaryRegionDef = Literal["secondary-shared"]

InterfaceEthernetNatChoiceDef = Literal["interface", "loopback", "pool"]

InterfaceEthernetDefaultNatChoiceDef = Literal["interface"]

VpnInterfaceEthernetStaticNatDirectionDef = Literal["inside"]

VpnInterfaceEthernetDefaultStaticNatDirectionDef = Literal["inside"]

InterfaceEthernetStaticPortForwardProtocolDef = Literal["tcp", "udp"]

WanVpnInterfaceEthernetStaticNatDirectionDef = Literal["inside"]

WanVpnInterfaceEthernetDefaultStaticNatDirectionDef = Literal["inside"]

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
class OneOfPortChannelOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfPortChannelOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfPortChannelQosAggregateOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfPortChannelQosAggregateOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfPortChannelQosAggregateOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfPortChannelLoadBalanceOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: PortChannelLoadBalanceDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfPortChannelLoadBalanceOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfPortChannelLoadBalanceOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfLacpFastSwitchoverOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfLacpFastSwitchoverOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfLacpFastSwitchoverOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfLacpMinBundleOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfLacpMinBundleOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfLacpMinBundleOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfLacpMaxBundleOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfLacpMaxBundleOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfLacpMaxBundleOptionsDef3:
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
class ParcelReferenceDef:
    ref_id: RefId = _field(metadata={"alias": "refId"})


@dataclass
class OneOfLacpModeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: PortChannelLacpModeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfLacpModeOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfLacpModeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: PortChannelLacpModeActiveDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfLacpRateOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: LacpRateDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfLacpRateOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfLacpRateOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfLacpPortPriorityOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfLacpPortPriorityOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfLacpPortPriorityOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class PortChannelMemberLinks:
    interface: ParcelReferenceDef
    lacp_mode: Union[
        OneOfLacpModeOptionsDef1, OneOfLacpModeOptionsDef2, OneOfLacpModeOptionsDef3
    ] = _field(metadata={"alias": "lacpMode"})
    lacp_port_priority: Optional[
        Union[
            OneOfLacpPortPriorityOptionsDef1,
            OneOfLacpPortPriorityOptionsDef2,
            OneOfLacpPortPriorityOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "lacpPortPriority"})
    lacp_rate: Optional[
        Union[OneOfLacpRateOptionsDef1, OneOfLacpRateOptionsDef2, OneOfLacpRateOptionsDef3]
    ] = _field(default=None, metadata={"alias": "lacpRate"})


@dataclass
class LacpModeMainInterface:
    # Configure Port-Channel member links
    port_channel_member_links: List[PortChannelMemberLinks] = _field(
        metadata={"alias": "portChannelMemberLinks"}
    )
    lacp_fast_switchover: Optional[
        Union[
            OneOfLacpFastSwitchoverOptionsDef1,
            OneOfLacpFastSwitchoverOptionsDef2,
            OneOfLacpFastSwitchoverOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "lacpFastSwitchover"})
    lacp_max_bundle: Optional[
        Union[
            OneOfLacpMaxBundleOptionsDef1,
            OneOfLacpMaxBundleOptionsDef2,
            OneOfLacpMaxBundleOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "lacpMaxBundle"})
    lacp_min_bundle: Optional[
        Union[
            OneOfLacpMinBundleOptionsDef1,
            OneOfLacpMinBundleOptionsDef2,
            OneOfLacpMinBundleOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "lacpMinBundle"})
    load_balance: Optional[
        Union[
            OneOfPortChannelLoadBalanceOptionsDef1,
            OneOfPortChannelLoadBalanceOptionsDef2,
            OneOfPortChannelLoadBalanceOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "loadBalance"})
    port_channel_qos_aggregate: Optional[
        Union[
            OneOfPortChannelQosAggregateOptionsDef1,
            OneOfPortChannelQosAggregateOptionsDef2,
            OneOfPortChannelQosAggregateOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "portChannelQosAggregate"})


@dataclass
class MainInterface1:
    """
    Port-channel Lacp mode Main Interface
    """

    lacp_mode_main_interface: LacpModeMainInterface = _field(
        metadata={"alias": "lacpModeMainInterface"}
    )


@dataclass
class EthernetPortChannelMemberLinks:
    interface: ParcelReferenceDef


@dataclass
class StaticModeMainInterface:
    # Configure Port-Channel member links
    port_channel_member_links: List[EthernetPortChannelMemberLinks] = _field(
        metadata={"alias": "portChannelMemberLinks"}
    )
    load_balance: Optional[
        Union[
            OneOfPortChannelLoadBalanceOptionsDef1,
            OneOfPortChannelLoadBalanceOptionsDef2,
            OneOfPortChannelLoadBalanceOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "loadBalance"})
    port_channel_qos_aggregate: Optional[
        Union[
            OneOfPortChannelQosAggregateOptionsDef1,
            OneOfPortChannelQosAggregateOptionsDef2,
            OneOfPortChannelQosAggregateOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "portChannelQosAggregate"})


@dataclass
class MainInterface2:
    """
    Port-channel Static mode Main Interface
    """

    static_mode_main_interface: StaticModeMainInterface = _field(
        metadata={"alias": "staticModeMainInterface"}
    )


@dataclass
class PortChannel1:
    """
    Port-channel Main Interface
    """

    main_interface: Union[MainInterface1, MainInterface2] = _field(
        metadata={"alias": "mainInterface"}
    )


@dataclass
class Wan:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class SubInterface:
    wan: Wan


@dataclass
class PortChannel2:
    """
    Port-channel Wan Sub Interface
    """

    sub_interface: SubInterface = _field(metadata={"alias": "subInterface"})


@dataclass
class OneOfPortChannelMemberOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfPortChannelMemberOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


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
class OneOfIpV4AddressOptionsDef3:
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
        OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2, OneOfIpV4AddressOptionsDef3
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
class DhcpClient:
    """
    Enable DHCPv6
    """

    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


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
class SecondaryIpV6Address:
    address: Union[
        OneOfIpv6PrefixGlobalVariableWithoutDefault1, OneOfIpv6PrefixGlobalVariableWithoutDefault2
    ]


@dataclass
class EthernetDynamic:
    # Enable DHCPv6
    dhcp_client: DhcpClient = _field(metadata={"alias": "dhcpClient"})
    # secondary IPv6 addresses
    secondary_ip_v6_address: Optional[List[SecondaryIpV6Address]] = _field(
        default=None, metadata={"alias": "secondaryIpV6Address"}
    )


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
    # Static secondary IPv6 addresses
    secondary_ip_v6_address: Optional[List[SecondaryIpV6Address]] = _field(
        default=None, metadata={"alias": "secondaryIpV6Address"}
    )


@dataclass
class IntfIpV6Address2:
    static: EthernetStatic


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
class OneOfBlockNonSourceIpOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfBlockNonSourceIpOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfBlockNonSourceIpOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfServiceProviderOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfServiceProviderOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfServiceProviderOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfBandwidthUpstreamOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfBandwidthUpstreamOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfBandwidthUpstreamOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfBandwidthDownstreamOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfBandwidthDownstreamOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfBandwidthDownstreamOptionsDef3:
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
class OneOfTunnelInterfaceOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfTunnelInterfaceOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfPerTunnelQosOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfPerTunnelQosOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfPerTunnelQosOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfModeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ModeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfModeOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfBandwidthPercentOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfBandwidthPercentOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfBandwidthPercentOptionsDef3:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfBindOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfBindOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfBindOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfCarrierOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: CarrierDef


@dataclass
class OneOfCarrierOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfCarrierOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultCarrierDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfColorOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ColorDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfColorOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfColorOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Value  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfHelloIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfHelloIntervalOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfHelloIntervalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfHelloToleranceOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfHelloToleranceOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfHelloToleranceOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfLastResortCircuitOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfLastResortCircuitOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfLastResortCircuitOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfTlocExtensionGreToOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfTlocExtensionGreToOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTlocExtensionGreToOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfRestrictOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfRestrictOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfRestrictOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfGroupOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfGroupOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfGroupOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfBorderOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfBorderOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfBorderOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfMaxControlConnectionsOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfMaxControlConnectionsOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfMaxControlConnectionsOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfNatRefreshIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNatRefreshIntervalOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfNatRefreshIntervalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfVbondAsStunServerOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfVbondAsStunServerOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfVbondAsStunServerOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfControllerGroupListOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[int]


@dataclass
class OneOfControllerGroupListOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfControllerGroupListOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfVmanageConnectionPreferenceOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfVmanageConnectionPreferenceOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfVmanageConnectionPreferenceOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfPortHopOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfPortHopOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfPortHopOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfLowBandwidthLinkOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfLowBandwidthLinkOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfLowBandwidthLinkOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfTunnelTcpMssAdjustOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfTunnelTcpMssAdjustOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTunnelTcpMssAdjustOptionsDef3:
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
    value: bool


@dataclass
class OneOfPropagateSgtOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfPropagateSgtOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfPropagateSgtOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfNetworkBroadcastOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfNetworkBroadcastOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfNetworkBroadcastOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAllowFragmentationDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAllowFragmentationDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAllowFragmentationDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfSetSdwanTunnelMtuToMaxDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfSetSdwanTunnelMtuToMaxDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfSetSdwanTunnelMtuToMaxDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class Tunnel:
    """
    Tunnel Interface Attributes
    """

    allow_fragmentation: Optional[
        Union[OneOfAllowFragmentationDef1, OneOfAllowFragmentationDef2, OneOfAllowFragmentationDef3]
    ] = _field(default=None, metadata={"alias": "allowFragmentation"})
    bandwidth_percent: Optional[
        Union[
            OneOfBandwidthPercentOptionsDef1,
            OneOfBandwidthPercentOptionsDef2,
            OneOfBandwidthPercentOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "bandwidthPercent"})
    bind: Optional[Union[OneOfBindOptionsDef1, OneOfBindOptionsDef2, OneOfBindOptionsDef3]] = (
        _field(default=None)
    )
    border: Optional[
        Union[OneOfBorderOptionsDef1, OneOfBorderOptionsDef2, OneOfBorderOptionsDef3]
    ] = _field(default=None)
    carrier: Optional[
        Union[OneOfCarrierOptionsDef1, OneOfCarrierOptionsDef2, OneOfCarrierOptionsDef3]
    ] = _field(default=None)
    clear_dont_fragment: Optional[
        Union[
            OneOfClearDontFragmentOptionsDef1,
            OneOfClearDontFragmentOptionsDef2,
            OneOfClearDontFragmentOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "clearDontFragment"})
    color: Optional[Union[OneOfColorOptionsDef1, OneOfColorOptionsDef2, OneOfColorOptionsDef3]] = (
        _field(default=None)
    )
    cts_sgt_propagation: Optional[
        Union[
            OneOfPropagateSgtOptionsDef1, OneOfPropagateSgtOptionsDef2, OneOfPropagateSgtOptionsDef3
        ]
    ] = _field(default=None, metadata={"alias": "ctsSgtPropagation"})
    exclude_controller_group_list: Optional[
        Union[
            OneOfControllerGroupListOptionsDef1,
            OneOfControllerGroupListOptionsDef2,
            OneOfControllerGroupListOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "excludeControllerGroupList"})
    group: Optional[Union[OneOfGroupOptionsDef1, OneOfGroupOptionsDef2, OneOfGroupOptionsDef3]] = (
        _field(default=None)
    )
    hello_interval: Optional[
        Union[
            OneOfHelloIntervalOptionsDef1,
            OneOfHelloIntervalOptionsDef2,
            OneOfHelloIntervalOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "helloInterval"})
    hello_tolerance: Optional[
        Union[
            OneOfHelloToleranceOptionsDef1,
            OneOfHelloToleranceOptionsDef2,
            OneOfHelloToleranceOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "helloTolerance"})
    last_resort_circuit: Optional[
        Union[
            OneOfLastResortCircuitOptionsDef1,
            OneOfLastResortCircuitOptionsDef2,
            OneOfLastResortCircuitOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "lastResortCircuit"})
    low_bandwidth_link: Optional[
        Union[
            OneOfLowBandwidthLinkOptionsDef1,
            OneOfLowBandwidthLinkOptionsDef2,
            OneOfLowBandwidthLinkOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "lowBandwidthLink"})
    max_control_connections: Optional[
        Union[
            OneOfMaxControlConnectionsOptionsDef1,
            OneOfMaxControlConnectionsOptionsDef2,
            OneOfMaxControlConnectionsOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "maxControlConnections"})
    mode: Optional[Union[OneOfModeOptionsDef1, OneOfModeOptionsDef2]] = _field(default=None)
    nat_refresh_interval: Optional[
        Union[
            OneOfNatRefreshIntervalOptionsDef1,
            OneOfNatRefreshIntervalOptionsDef2,
            OneOfNatRefreshIntervalOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "natRefreshInterval"})
    network_broadcast: Optional[
        Union[
            OneOfNetworkBroadcastOptionsDef1,
            OneOfNetworkBroadcastOptionsDef2,
            OneOfNetworkBroadcastOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "networkBroadcast"})
    per_tunnel_qos: Optional[
        Union[
            OneOfPerTunnelQosOptionsDef1, OneOfPerTunnelQosOptionsDef2, OneOfPerTunnelQosOptionsDef3
        ]
    ] = _field(default=None, metadata={"alias": "perTunnelQos"})
    port_hop: Optional[
        Union[OneOfPortHopOptionsDef1, OneOfPortHopOptionsDef2, OneOfPortHopOptionsDef3]
    ] = _field(default=None, metadata={"alias": "portHop"})
    restrict: Optional[
        Union[OneOfRestrictOptionsDef1, OneOfRestrictOptionsDef2, OneOfRestrictOptionsDef3]
    ] = _field(default=None)
    set_sdwan_tunnel_mtu_to_max: Optional[
        Union[
            OneOfSetSdwanTunnelMtuToMaxDef1,
            OneOfSetSdwanTunnelMtuToMaxDef2,
            OneOfSetSdwanTunnelMtuToMaxDef3,
        ]
    ] = _field(default=None, metadata={"alias": "setSdwanTunnelMTUToMax"})
    tloc_extension_gre_to: Optional[
        Union[
            OneOfTlocExtensionGreToOptionsDef1,
            OneOfTlocExtensionGreToOptionsDef2,
            OneOfTlocExtensionGreToOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tlocExtensionGreTo"})
    tunnel_tcp_mss: Optional[
        Union[
            OneOfTunnelTcpMssAdjustOptionsDef1,
            OneOfTunnelTcpMssAdjustOptionsDef2,
            OneOfTunnelTcpMssAdjustOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tunnelTcpMss"})
    v_bond_as_stun_server: Optional[
        Union[
            OneOfVbondAsStunServerOptionsDef1,
            OneOfVbondAsStunServerOptionsDef2,
            OneOfVbondAsStunServerOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "vBondAsStunServer"})
    v_manage_connection_preference: Optional[
        Union[
            OneOfVmanageConnectionPreferenceOptionsDef1,
            OneOfVmanageConnectionPreferenceOptionsDef2,
            OneOfVmanageConnectionPreferenceOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "vManageConnectionPreference"})


@dataclass
class OneOfAllowAllOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAllowAllOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAllowAllOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAllowBgpOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAllowBgpOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAllowBgpOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAllowDhcpOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAllowDhcpOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAllowDhcpOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAllowNtpOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAllowNtpOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAllowNtpOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAllowSshOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAllowSshOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAllowSshOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAllowServiceTrueOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAllowServiceTrueOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAllowServiceTrueOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAllowServiceFalseOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAllowServiceFalseOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAllowServiceFalseOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class AllowService:
    """
    Tunnel Interface Attributes
    """

    all: Optional[
        Union[OneOfAllowAllOptionsDef1, OneOfAllowAllOptionsDef2, OneOfAllowAllOptionsDef3]
    ] = _field(default=None)
    bfd: Optional[
        Union[
            OneOfAllowServiceFalseOptionsDef1,
            OneOfAllowServiceFalseOptionsDef2,
            OneOfAllowServiceFalseOptionsDef3,
        ]
    ] = _field(default=None)
    bgp: Optional[
        Union[OneOfAllowBgpOptionsDef1, OneOfAllowBgpOptionsDef2, OneOfAllowBgpOptionsDef3]
    ] = _field(default=None)
    dhcp: Optional[
        Union[OneOfAllowDhcpOptionsDef1, OneOfAllowDhcpOptionsDef2, OneOfAllowDhcpOptionsDef3]
    ] = _field(default=None)
    dns: Optional[
        Union[
            OneOfAllowServiceTrueOptionsDef1,
            OneOfAllowServiceTrueOptionsDef2,
            OneOfAllowServiceTrueOptionsDef3,
        ]
    ] = _field(default=None)
    https: Optional[
        Union[
            OneOfAllowServiceTrueOptionsDef1,
            OneOfAllowServiceTrueOptionsDef2,
            OneOfAllowServiceTrueOptionsDef3,
        ]
    ] = _field(default=None)
    icmp: Optional[
        Union[
            OneOfAllowServiceTrueOptionsDef1,
            OneOfAllowServiceTrueOptionsDef2,
            OneOfAllowServiceTrueOptionsDef3,
        ]
    ] = _field(default=None)
    netconf: Optional[
        Union[
            OneOfAllowServiceFalseOptionsDef1,
            OneOfAllowServiceFalseOptionsDef2,
            OneOfAllowServiceFalseOptionsDef3,
        ]
    ] = _field(default=None)
    ntp: Optional[
        Union[OneOfAllowNtpOptionsDef1, OneOfAllowNtpOptionsDef2, OneOfAllowNtpOptionsDef3]
    ] = _field(default=None)
    ospf: Optional[
        Union[
            OneOfAllowServiceFalseOptionsDef1,
            OneOfAllowServiceFalseOptionsDef2,
            OneOfAllowServiceFalseOptionsDef3,
        ]
    ] = _field(default=None)
    snmp: Optional[
        Union[
            OneOfAllowServiceFalseOptionsDef1,
            OneOfAllowServiceFalseOptionsDef2,
            OneOfAllowServiceFalseOptionsDef3,
        ]
    ] = _field(default=None)
    ssh: Optional[
        Union[OneOfAllowSshOptionsDef1, OneOfAllowSshOptionsDef2, OneOfAllowSshOptionsDef3]
    ] = _field(default=None)
    stun: Optional[
        Union[
            OneOfAllowServiceFalseOptionsDef1,
            OneOfAllowServiceFalseOptionsDef2,
            OneOfAllowServiceFalseOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class OneOfEncapsulationEncapOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EncapsulationEncapDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfEncapsulationPreferenceOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfEncapsulationPreferenceOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfEncapsulationPreferenceOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfEncapsulationWeightOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfEncapsulationWeightOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfEncapsulationWeightOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class Encapsulation:
    encap: OneOfEncapsulationEncapOptionsDef
    preference: Optional[
        Union[
            OneOfEncapsulationPreferenceOptionsDef1,
            OneOfEncapsulationPreferenceOptionsDef2,
            OneOfEncapsulationPreferenceOptionsDef3,
        ]
    ] = _field(default=None)
    weight: Optional[
        Union[
            OneOfEncapsulationWeightOptionsDef1,
            OneOfEncapsulationWeightOptionsDef2,
            OneOfEncapsulationWeightOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class OneOfEnableRegionDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfEnableRegionDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfCoreRegionDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: CoreRegionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfCoreRegionDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultCoreRegionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfSecondaryRegionDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SecondaryRegionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfSecondaryRegionDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultSecondaryRegionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class MultiRegionFabric:
    """
    Multi-Region Fabric
    """

    core_region: Optional[Union[OneOfCoreRegionDef1, OneOfCoreRegionDef2]] = _field(
        default=None, metadata={"alias": "coreRegion"}
    )
    enable_core_region: Optional[Union[OneOfEnableRegionDef1, OneOfEnableRegionDef2]] = _field(
        default=None, metadata={"alias": "enableCoreRegion"}
    )
    enable_secondary_region: Optional[Union[OneOfEnableRegionDef1, OneOfEnableRegionDef2]] = _field(
        default=None, metadata={"alias": "enableSecondaryRegion"}
    )
    secondary_region: Optional[Union[OneOfSecondaryRegionDef1, OneOfSecondaryRegionDef2]] = _field(
        default=None, metadata={"alias": "secondaryRegion"}
    )


@dataclass
class OneOfNatOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfNatOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfNatOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfNatTypeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: NatChoiceDef


@dataclass
class OneOfNatTypeOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultNatChoiceDef  # pytype: disable=annotation-type-mismatch


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
class NatPool:
    """
    NAT Pool
    """

    prefix_length: Union[
        OneOfNatPoolPrefixLengthOptionsDef1, OneOfNatPoolPrefixLengthOptionsDef2
    ] = _field(metadata={"alias": "prefixLength"})
    range_end: Union[OneOfNatPoolRangeEndOptionsDef1, OneOfNatPoolRangeEndOptionsDef2] = _field(
        metadata={"alias": "rangeEnd"}
    )
    range_start: Union[OneOfNatPoolRangeStartOptionsDef1, OneOfNatPoolRangeStartOptionsDef2] = (
        _field(metadata={"alias": "rangeStart"})
    )
    overload: Optional[
        Union[
            OneOfNatPoolOverloadOptionsDef1,
            OneOfNatPoolOverloadOptionsDef2,
            OneOfNatPoolOverloadOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class OneOfLoopbackInterfaceOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfLoopbackInterfaceOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfLoopbackInterfaceOptionsDef3:
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
class MultiplePool:
    name: Union[OneOfNatPoolNameOptionsDef1, OneOfNatPoolNameOptionsDef2]
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
    enable_dual_router_ha_mapping: Optional[
        Union[
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef1,
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "enableDualRouterHAMapping"})


@dataclass
class MultipleLoopback:
    loopback_interface: Union[
        OneOfLoopbackInterfaceOptionsDef1,
        OneOfLoopbackInterfaceOptionsDef2,
        OneOfLoopbackInterfaceOptionsDef3,
    ] = _field(metadata={"alias": "loopbackInterface"})


@dataclass
class OneOfUdpTimeoutOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfUdpTimeoutOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfUdpTimeoutOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfTcpTimeoutOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfTcpTimeoutOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTcpTimeoutOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfStaticSourceIpOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfStaticSourceIpOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfStaticTranslateIpOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfStaticTranslateIpOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfStaticNatDirectionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: StaticNatDirectionDef


@dataclass
class OneOfStaticNatDirectionOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultStaticNatDirectionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfStaticSourceVpnOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfStaticSourceVpnOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfStaticSourceVpnOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class NewStaticNat:
    source_ip: Union[OneOfStaticSourceIpOptionsDef1, OneOfStaticSourceIpOptionsDef2] = _field(
        metadata={"alias": "sourceIp"}
    )
    source_vpn: Union[
        OneOfStaticSourceVpnOptionsDef1,
        OneOfStaticSourceVpnOptionsDef2,
        OneOfStaticSourceVpnOptionsDef3,
    ] = _field(metadata={"alias": "sourceVpn"})
    static_nat_direction: Union[
        OneOfStaticNatDirectionOptionsDef1, OneOfStaticNatDirectionOptionsDef2
    ] = _field(metadata={"alias": "staticNatDirection"})
    translate_ip: Union[OneOfStaticTranslateIpOptionsDef1, OneOfStaticTranslateIpOptionsDef2] = (
        _field(metadata={"alias": "translateIp"})
    )
    enable_dual_router_ha_mapping: Optional[
        Union[
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef1,
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "enableDualRouterHAMapping"})


@dataclass
class OneOfStaticPortForwardProtocolOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: StaticPortForwardProtocolDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfStaticPortForwardProtocolOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfStaticSourcePortOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfStaticSourcePortOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfStaticTranslatePortOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfStaticTranslatePortOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class StaticPortForward:
    protocol: Union[
        OneOfStaticPortForwardProtocolOptionsDef1, OneOfStaticPortForwardProtocolOptionsDef2
    ]
    source_ip: Union[OneOfStaticSourceIpOptionsDef1, OneOfStaticSourceIpOptionsDef2] = _field(
        metadata={"alias": "sourceIp"}
    )
    source_port: Union[OneOfStaticSourcePortOptionsDef1, OneOfStaticSourcePortOptionsDef2] = _field(
        metadata={"alias": "sourcePort"}
    )
    source_vpn: Union[
        OneOfStaticSourceVpnOptionsDef1,
        OneOfStaticSourceVpnOptionsDef2,
        OneOfStaticSourceVpnOptionsDef3,
    ] = _field(metadata={"alias": "sourceVpn"})
    static_nat_direction: Union[
        OneOfStaticNatDirectionOptionsDef1, OneOfStaticNatDirectionOptionsDef2
    ] = _field(metadata={"alias": "staticNatDirection"})
    translate_ip: Union[OneOfStaticTranslateIpOptionsDef1, OneOfStaticTranslateIpOptionsDef2] = (
        _field(metadata={"alias": "translateIp"})
    )
    translate_port: Union[
        OneOfStaticTranslatePortOptionsDef1, OneOfStaticTranslatePortOptionsDef2
    ] = _field(metadata={"alias": "translatePort"})
    enable_dual_router_ha_mapping: Optional[
        Union[
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef1,
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "enableDualRouterHAMapping"})


@dataclass
class NatAttributesIpv4:
    """
    NAT Attributes IpV4
    """

    nat_type: Union[OneOfNatTypeOptionsDef1, OneOfNatTypeOptionsDef2] = _field(
        metadata={"alias": "natType"}
    )
    tcp_timeout: Union[
        OneOfTcpTimeoutOptionsDef1, OneOfTcpTimeoutOptionsDef2, OneOfTcpTimeoutOptionsDef3
    ] = _field(metadata={"alias": "tcpTimeout"})
    udp_timeout: Union[
        OneOfUdpTimeoutOptionsDef1, OneOfUdpTimeoutOptionsDef2, OneOfUdpTimeoutOptionsDef3
    ] = _field(metadata={"alias": "udpTimeout"})
    match_interface: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "matchInterface"})
    # NAT Multiple Loopback
    multiple_loopback: Optional[List[MultipleLoopback]] = _field(
        default=None, metadata={"alias": "multipleLoopback"}
    )
    # NAT Multiple Pool
    multiple_pool: Optional[List[MultiplePool]] = _field(
        default=None, metadata={"alias": "multiplePool"}
    )
    nat_loopback: Optional[
        Union[
            OneOfLoopbackInterfaceOptionsDef1,
            OneOfLoopbackInterfaceOptionsDef2,
            OneOfLoopbackInterfaceOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "natLoopback"})
    # NAT Pool
    nat_pool: Optional[NatPool] = _field(default=None, metadata={"alias": "natPool"})
    # static NAT
    new_static_nat: Optional[List[NewStaticNat]] = _field(
        default=None, metadata={"alias": "newStaticNat"}
    )
    # Configure Port Forward entries
    static_port_forward: Optional[List[StaticPortForward]] = _field(
        default=None, metadata={"alias": "staticPortForward"}
    )


@dataclass
class OneOfNat64Nat66OptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfNat64Nat66OptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfStaticNat66SourcePrefixOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfStaticNat66SourcePrefixOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfStaticNat66TranslatedSourcePrefixOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfStaticNat66TranslatedSourcePrefixOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfStaticNat66TranslatedSourcePrefixOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfStaticNat66SourceVpnIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfStaticNat66SourceVpnIdOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfStaticNat66SourceVpnIdOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class StaticNat66:
    source_prefix: Union[
        OneOfStaticNat66SourcePrefixOptionsDef1, OneOfStaticNat66SourcePrefixOptionsDef2
    ] = _field(metadata={"alias": "sourcePrefix"})
    source_vpn_id: Union[
        OneOfStaticNat66SourceVpnIdOptionsDef1,
        OneOfStaticNat66SourceVpnIdOptionsDef2,
        OneOfStaticNat66SourceVpnIdOptionsDef3,
    ] = _field(metadata={"alias": "sourceVpnId"})
    egress_interface: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "egressInterface"})
    translated_source_prefix: Optional[
        Union[
            OneOfStaticNat66TranslatedSourcePrefixOptionsDef1,
            OneOfStaticNat66TranslatedSourcePrefixOptionsDef2,
            OneOfStaticNat66TranslatedSourcePrefixOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "translatedSourcePrefix"})


@dataclass
class NatAttributesIpv6:
    """
    NAT Attributes Ipv6
    """

    nat64: Optional[Union[OneOfNat64Nat66OptionsDef1, OneOfNat64Nat66OptionsDef2]] = _field(
        default=None
    )
    nat66: Optional[Union[OneOfNat64Nat66OptionsDef1, OneOfNat64Nat66OptionsDef2]] = _field(
        default=None
    )
    # static NAT66
    static_nat66: Optional[List[StaticNat66]] = _field(
        default=None, metadata={"alias": "staticNat66"}
    )


@dataclass
class OneOfQosAdaptiveOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfQosAdaptiveOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfPeriodOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfPeriodOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfPeriodOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class ShapingRateUpstream:
    value: Optional[Any] = _field(default=None)


@dataclass
class OneOfShapingRateUpOrDownstreamOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfShapingRateUpOrDownstreamOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class ShapingRateUpstreamConfig:
    """
    adaptiveQoS Shaping Rate Upstream config
    """

    default_shaping_rate_upstream: Union[
        OneOfShapingRateUpOrDownstreamOptionsDef1, OneOfShapingRateUpOrDownstreamOptionsDef2
    ] = _field(metadata={"alias": "defaultShapingRateUpstream"})
    max_shaping_rate_upstream: Union[
        OneOfShapingRateUpOrDownstreamOptionsDef1, OneOfShapingRateUpOrDownstreamOptionsDef2
    ] = _field(metadata={"alias": "maxShapingRateUpstream"})
    min_shaping_rate_upstream: Union[
        OneOfShapingRateUpOrDownstreamOptionsDef1, OneOfShapingRateUpOrDownstreamOptionsDef2
    ] = _field(metadata={"alias": "minShapingRateUpstream"})


@dataclass
class OneOfShapingRateDownstreamOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfShapingRateDownstreamOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class ShapingRateDownstreamConfig:
    """
    adaptiveQoS Shaping Rate Downstream config
    """

    default_shaping_rate_downstream: Union[
        OneOfShapingRateUpOrDownstreamOptionsDef1, OneOfShapingRateUpOrDownstreamOptionsDef2
    ] = _field(metadata={"alias": "defaultShapingRateDownstream"})
    max_shaping_rate_downstream: Union[
        OneOfShapingRateUpOrDownstreamOptionsDef1, OneOfShapingRateUpOrDownstreamOptionsDef2
    ] = _field(metadata={"alias": "maxShapingRateDownstream"})
    min_shaping_rate_downstream: Union[
        OneOfShapingRateUpOrDownstreamOptionsDef1, OneOfShapingRateUpOrDownstreamOptionsDef2
    ] = _field(metadata={"alias": "minShapingRateDownstream"})


@dataclass
class OneOfShapingRateOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfShapingRateOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfShapingRateOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class AclQos1:
    adaptive_qo_s: Union[OneOfQosAdaptiveOptionsDef1, OneOfQosAdaptiveOptionsDef2] = _field(
        metadata={"alias": "adaptiveQoS"}
    )
    shaping_rate_upstream: ShapingRateUpstream = _field(metadata={"alias": "shapingRateUpstream"})
    # adaptiveQoS Shaping Rate Upstream config
    shaping_rate_upstream_config: ShapingRateUpstreamConfig = _field(
        metadata={"alias": "shapingRateUpstreamConfig"}
    )
    adapt_period: Optional[
        Union[OneOfPeriodOptionsDef1, OneOfPeriodOptionsDef2, OneOfPeriodOptionsDef3]
    ] = _field(default=None, metadata={"alias": "adaptPeriod"})
    ipv4_acl_egress: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "ipv4AclEgress"}
    )
    ipv4_acl_ingress: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "ipv4AclIngress"}
    )
    ipv6_acl_egress: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "ipv6AclEgress"}
    )
    ipv6_acl_ingress: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "ipv6AclIngress"}
    )
    shaping_rate: Optional[
        Union[OneOfShapingRateOptionsDef1, OneOfShapingRateOptionsDef2, OneOfShapingRateOptionsDef3]
    ] = _field(default=None, metadata={"alias": "shapingRate"})
    shaping_rate_downstream: Optional[
        Union[OneOfShapingRateDownstreamOptionsDef1, OneOfShapingRateDownstreamOptionsDef2]
    ] = _field(default=None, metadata={"alias": "shapingRateDownstream"})
    # adaptiveQoS Shaping Rate Downstream config
    shaping_rate_downstream_config: Optional[ShapingRateDownstreamConfig] = _field(
        default=None, metadata={"alias": "shapingRateDownstreamConfig"}
    )


@dataclass
class OneOfShapingRateUpstreamOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfShapingRateUpstreamOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class AclQos2:
    adaptive_qo_s: Union[OneOfQosAdaptiveOptionsDef1, OneOfQosAdaptiveOptionsDef2] = _field(
        metadata={"alias": "adaptiveQoS"}
    )
    adapt_period: Optional[
        Union[OneOfPeriodOptionsDef1, OneOfPeriodOptionsDef2, OneOfPeriodOptionsDef3]
    ] = _field(default=None, metadata={"alias": "adaptPeriod"})
    ipv4_acl_egress: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "ipv4AclEgress"}
    )
    ipv4_acl_ingress: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "ipv4AclIngress"}
    )
    ipv6_acl_egress: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "ipv6AclEgress"}
    )
    ipv6_acl_ingress: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "ipv6AclIngress"}
    )
    shaping_rate: Optional[
        Union[OneOfShapingRateOptionsDef1, OneOfShapingRateOptionsDef2, OneOfShapingRateOptionsDef3]
    ] = _field(default=None, metadata={"alias": "shapingRate"})
    shaping_rate_downstream: Optional[
        Union[OneOfShapingRateDownstreamOptionsDef1, OneOfShapingRateDownstreamOptionsDef2]
    ] = _field(default=None, metadata={"alias": "shapingRateDownstream"})
    # adaptiveQoS Shaping Rate Downstream config
    shaping_rate_downstream_config: Optional[ShapingRateDownstreamConfig] = _field(
        default=None, metadata={"alias": "shapingRateDownstreamConfig"}
    )
    shaping_rate_upstream: Optional[
        Union[OneOfShapingRateUpstreamOptionsDef1, OneOfShapingRateUpstreamOptionsDef2]
    ] = _field(default=None, metadata={"alias": "shapingRateUpstream"})
    # adaptiveQoS Shaping Rate Upstream config
    shaping_rate_upstream_config: Optional[ShapingRateUpstreamConfig] = _field(
        default=None, metadata={"alias": "shapingRateUpstreamConfig"}
    )


@dataclass
class OneOfMacAddressOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfMacAddressOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfMacAddressOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class Arp:
    ip_address: Union[
        OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2, OneOfIpV4AddressOptionsDef3
    ] = _field(metadata={"alias": "ipAddress"})
    mac_address: Union[
        OneOfMacAddressOptionsDef1, OneOfMacAddressOptionsDef2, OneOfMacAddressOptionsDef3
    ] = _field(metadata={"alias": "macAddress"})


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
    value: int


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
class OneOfTlocExtensionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfTlocExtensionOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTlocExtensionOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfTlocExtensionGreFromOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfTlocExtensionGreFromOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTlocExtensionGreFromOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfXconnectOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfXconnectOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfXconnectOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class TlocExtensionGreFrom:
    """
    Extend remote TLOC over a GRE tunnel to a local WAN interface
    """

    source_ip: Optional[
        Union[
            OneOfTlocExtensionGreFromOptionsDef1,
            OneOfTlocExtensionGreFromOptionsDef2,
            OneOfTlocExtensionGreFromOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sourceIp"})
    xconnect: Optional[
        Union[OneOfXconnectOptionsDef1, OneOfXconnectOptionsDef2, OneOfXconnectOptionsDef3]
    ] = _field(default=None)


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
class OneOfTrackerOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfTrackerOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTrackerOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


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

    arp_timeout: Optional[
        Union[OneOfArpTimeoutOptionsDef1, OneOfArpTimeoutOptionsDef2, OneOfArpTimeoutOptionsDef3]
    ] = _field(default=None, metadata={"alias": "arpTimeout"})
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
            OneOfOnBooleanDefaultTrueOptionsDef1,
            OneOfOnBooleanDefaultTrueOptionsDef2,
            OneOfOnBooleanDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "icmpRedirectDisable"})
    intrf_mtu: Optional[
        Union[OneOfIntrfMtuOptionsDef1, OneOfIntrfMtuOptionsDef2, OneOfIntrfMtuOptionsDef3]
    ] = _field(default=None, metadata={"alias": "intrfMtu"})
    ip_directed_broadcast: Optional[
        Union[
            OneOfIpDirectedBroadcastOptionsDef1,
            OneOfIpDirectedBroadcastOptionsDef2,
            OneOfIpDirectedBroadcastOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ipDirectedBroadcast"})
    ip_mtu: Optional[Union[OneOfMtuOptionsDef1, OneOfMtuOptionsDef2, OneOfMtuOptionsDef3]] = _field(
        default=None, metadata={"alias": "ipMtu"}
    )
    load_interval: Optional[
        Union[
            OneOfLoadIntervalOptionsDef1, OneOfLoadIntervalOptionsDef2, OneOfLoadIntervalOptionsDef3
        ]
    ] = _field(default=None, metadata={"alias": "loadInterval"})
    mac_address: Optional[
        Union[OneOfMacAddressOptionsDef1, OneOfMacAddressOptionsDef2, OneOfMacAddressOptionsDef3]
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
    tloc_extension: Optional[
        Union[
            OneOfTlocExtensionOptionsDef1,
            OneOfTlocExtensionOptionsDef2,
            OneOfTlocExtensionOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tlocExtension"})
    # Extend remote TLOC over a GRE tunnel to a local WAN interface
    tloc_extension_gre_from: Optional[TlocExtensionGreFrom] = _field(
        default=None, metadata={"alias": "tlocExtensionGreFrom"}
    )
    tracker: Optional[
        Union[OneOfTrackerOptionsDef1, OneOfTrackerOptionsDef2, OneOfTrackerOptionsDef3]
    ] = _field(default=None)


@dataclass
class EthernetData:
    description: Union[
        OneOfDescriptionOptionsDef1, OneOfDescriptionOptionsDef2, OneOfDescriptionOptionsDef3
    ]
    interface_name: Union[OneOfInterfaceNameOptionsDef1, OneOfInterfaceNameOptionsDef2] = _field(
        metadata={"alias": "interfaceName"}
    )
    shutdown: Union[OneOfShutdownOptionsDef1, OneOfShutdownOptionsDef2, OneOfShutdownOptionsDef3]
    tunnel_interface: Union[OneOfTunnelInterfaceOptionsDef1, OneOfTunnelInterfaceOptionsDef2] = (
        _field(metadata={"alias": "tunnelInterface"})
    )
    # ACL/QOS
    acl_qos: Optional[Union[AclQos1, AclQos2]] = _field(default=None, metadata={"alias": "aclQos"})
    # Advanced Attributes
    advanced: Optional[Advanced] = _field(default=None)
    # Tunnel Interface Attributes
    allow_service: Optional[AllowService] = _field(default=None, metadata={"alias": "allowService"})
    # Configure ARP entries
    arp: Optional[List[Arp]] = _field(default=None)
    auto_detect_bandwidth: Optional[
        Union[
            OneOfAutoBandwidthDetectOptionsDef1,
            OneOfAutoBandwidthDetectOptionsDef2,
            OneOfAutoBandwidthDetectOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "autoDetectBandwidth"})
    bandwidth_downstream: Optional[
        Union[
            OneOfBandwidthDownstreamOptionsDef1,
            OneOfBandwidthDownstreamOptionsDef2,
            OneOfBandwidthDownstreamOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "bandwidthDownstream"})
    bandwidth_upstream: Optional[
        Union[
            OneOfBandwidthUpstreamOptionsDef1,
            OneOfBandwidthUpstreamOptionsDef2,
            OneOfBandwidthUpstreamOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "bandwidthUpstream"})
    block_non_source_ip: Optional[
        Union[
            OneOfBlockNonSourceIpOptionsDef1,
            OneOfBlockNonSourceIpOptionsDef2,
            OneOfBlockNonSourceIpOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "blockNonSourceIp"})
    dhcp_helper: Optional[
        Union[OneOfListOfIpV4OptionsDef1, OneOfListOfIpV4OptionsDef2, OneOfListOfIpV4OptionsDef3]
    ] = _field(default=None, metadata={"alias": "dhcpHelper"})
    enable_ha_interlink_interface: Optional[
        Union[
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef1,
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "enableHAInterlinkInterface"})
    # Encapsulation for TLOC
    encapsulation: Optional[List[Encapsulation]] = _field(default=None)
    intf_ip_address: Optional[Union[IntfIpAddress1, IntfIpAddress2]] = _field(
        default=None, metadata={"alias": "intfIpAddress"}
    )
    intf_ip_v6_address: Optional[Union[IntfIpV6Address1, IntfIpV6Address2]] = _field(
        default=None, metadata={"alias": "intfIpV6Address"}
    )
    iperf_server: Optional[
        Union[OneOfIperfServerOptionsDef1, OneOfIperfServerOptionsDef2, OneOfIperfServerOptionsDef3]
    ] = _field(default=None, metadata={"alias": "iperfServer"})
    # Multi-Region Fabric
    multi_region_fabric: Optional[MultiRegionFabric] = _field(
        default=None, metadata={"alias": "multiRegionFabric"}
    )
    nat: Optional[Union[OneOfNatOptionsDef1, OneOfNatOptionsDef2, OneOfNatOptionsDef3]] = _field(
        default=None
    )
    # NAT Attributes IpV4
    nat_attributes_ipv4: Optional[NatAttributesIpv4] = _field(
        default=None, metadata={"alias": "natAttributesIpv4"}
    )
    # NAT Attributes Ipv6
    nat_attributes_ipv6: Optional[NatAttributesIpv6] = _field(
        default=None, metadata={"alias": "natAttributesIpv6"}
    )
    nat_ipv6: Optional[Union[OneOfNatOptionsDef1, OneOfNatOptionsDef2, OneOfNatOptionsDef3]] = (
        _field(default=None, metadata={"alias": "natIpv6"})
    )
    port_channel: Optional[Union[PortChannel1, PortChannel2]] = _field(
        default=None, metadata={"alias": "portChannel"}
    )
    port_channel_interface: Optional[
        Union[OneOfPortChannelOptionsDef1, OneOfPortChannelOptionsDef2]
    ] = _field(default=None, metadata={"alias": "portChannelInterface"})
    port_channel_member_interface: Optional[
        Union[OneOfPortChannelMemberOptionsDef1, OneOfPortChannelMemberOptionsDef2]
    ] = _field(default=None, metadata={"alias": "portChannelMemberInterface"})
    service_provider: Optional[
        Union[
            OneOfServiceProviderOptionsDef1,
            OneOfServiceProviderOptionsDef2,
            OneOfServiceProviderOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "serviceProvider"})
    # Tunnel Interface Attributes
    tunnel: Optional[Tunnel] = _field(default=None)


@dataclass
class Payload:
    """
    WAN VPN Interface Ethernet profile parcel schema for POST request
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
    # WAN VPN Interface Ethernet profile parcel schema for POST request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdwanTransportWanVpnInterfaceEthernetPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateWanVpnInterfaceEthernetParcelForTransportPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class InterfaceEthernetData:
    description: Union[
        OneOfDescriptionOptionsDef1, OneOfDescriptionOptionsDef2, OneOfDescriptionOptionsDef3
    ]
    interface_name: Union[OneOfInterfaceNameOptionsDef1, OneOfInterfaceNameOptionsDef2] = _field(
        metadata={"alias": "interfaceName"}
    )
    shutdown: Union[OneOfShutdownOptionsDef1, OneOfShutdownOptionsDef2, OneOfShutdownOptionsDef3]
    tunnel_interface: Union[OneOfTunnelInterfaceOptionsDef1, OneOfTunnelInterfaceOptionsDef2] = (
        _field(metadata={"alias": "tunnelInterface"})
    )
    # ACL/QOS
    acl_qos: Optional[Union[AclQos1, AclQos2]] = _field(default=None, metadata={"alias": "aclQos"})
    # Advanced Attributes
    advanced: Optional[Advanced] = _field(default=None)
    # Tunnel Interface Attributes
    allow_service: Optional[AllowService] = _field(default=None, metadata={"alias": "allowService"})
    # Configure ARP entries
    arp: Optional[List[Arp]] = _field(default=None)
    auto_detect_bandwidth: Optional[
        Union[
            OneOfAutoBandwidthDetectOptionsDef1,
            OneOfAutoBandwidthDetectOptionsDef2,
            OneOfAutoBandwidthDetectOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "autoDetectBandwidth"})
    bandwidth_downstream: Optional[
        Union[
            OneOfBandwidthDownstreamOptionsDef1,
            OneOfBandwidthDownstreamOptionsDef2,
            OneOfBandwidthDownstreamOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "bandwidthDownstream"})
    bandwidth_upstream: Optional[
        Union[
            OneOfBandwidthUpstreamOptionsDef1,
            OneOfBandwidthUpstreamOptionsDef2,
            OneOfBandwidthUpstreamOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "bandwidthUpstream"})
    block_non_source_ip: Optional[
        Union[
            OneOfBlockNonSourceIpOptionsDef1,
            OneOfBlockNonSourceIpOptionsDef2,
            OneOfBlockNonSourceIpOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "blockNonSourceIp"})
    dhcp_helper: Optional[
        Union[OneOfListOfIpV4OptionsDef1, OneOfListOfIpV4OptionsDef2, OneOfListOfIpV4OptionsDef3]
    ] = _field(default=None, metadata={"alias": "dhcpHelper"})
    enable_ha_interlink_interface: Optional[
        Union[
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef1,
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "enableHAInterlinkInterface"})
    # Encapsulation for TLOC
    encapsulation: Optional[List[Encapsulation]] = _field(default=None)
    intf_ip_address: Optional[Union[IntfIpAddress1, IntfIpAddress2]] = _field(
        default=None, metadata={"alias": "intfIpAddress"}
    )
    intf_ip_v6_address: Optional[Union[IntfIpV6Address1, IntfIpV6Address2]] = _field(
        default=None, metadata={"alias": "intfIpV6Address"}
    )
    iperf_server: Optional[
        Union[OneOfIperfServerOptionsDef1, OneOfIperfServerOptionsDef2, OneOfIperfServerOptionsDef3]
    ] = _field(default=None, metadata={"alias": "iperfServer"})
    # Multi-Region Fabric
    multi_region_fabric: Optional[MultiRegionFabric] = _field(
        default=None, metadata={"alias": "multiRegionFabric"}
    )
    nat: Optional[Union[OneOfNatOptionsDef1, OneOfNatOptionsDef2, OneOfNatOptionsDef3]] = _field(
        default=None
    )
    # NAT Attributes IpV4
    nat_attributes_ipv4: Optional[NatAttributesIpv4] = _field(
        default=None, metadata={"alias": "natAttributesIpv4"}
    )
    # NAT Attributes Ipv6
    nat_attributes_ipv6: Optional[NatAttributesIpv6] = _field(
        default=None, metadata={"alias": "natAttributesIpv6"}
    )
    nat_ipv6: Optional[Union[OneOfNatOptionsDef1, OneOfNatOptionsDef2, OneOfNatOptionsDef3]] = (
        _field(default=None, metadata={"alias": "natIpv6"})
    )
    port_channel: Optional[Union[PortChannel1, PortChannel2]] = _field(
        default=None, metadata={"alias": "portChannel"}
    )
    port_channel_interface: Optional[
        Union[OneOfPortChannelOptionsDef1, OneOfPortChannelOptionsDef2]
    ] = _field(default=None, metadata={"alias": "portChannelInterface"})
    port_channel_member_interface: Optional[
        Union[OneOfPortChannelMemberOptionsDef1, OneOfPortChannelMemberOptionsDef2]
    ] = _field(default=None, metadata={"alias": "portChannelMemberInterface"})
    service_provider: Optional[
        Union[
            OneOfServiceProviderOptionsDef1,
            OneOfServiceProviderOptionsDef2,
            OneOfServiceProviderOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "serviceProvider"})
    # Tunnel Interface Attributes
    tunnel: Optional[Tunnel] = _field(default=None)


@dataclass
class CreateWanVpnInterfaceEthernetParcelForTransportPostRequest:
    """
    WAN VPN Interface Ethernet profile parcel schema for POST request
    """

    data: InterfaceEthernetData
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class EthernetOneOfPortChannelLoadBalanceOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EthernetPortChannelLoadBalanceDef  # pytype: disable=annotation-type-mismatch


@dataclass
class EthernetOneOfLacpMinBundleOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class EthernetOneOfLacpMaxBundleOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class EthernetOneOfLacpModeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EthernetPortChannelLacpModeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class EthernetOneOfLacpModeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EthernetPortChannelLacpModeActiveDef  # pytype: disable=annotation-type-mismatch


@dataclass
class EthernetOneOfLacpRateOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EthernetLacpRateDef  # pytype: disable=annotation-type-mismatch


@dataclass
class EthernetOneOfLacpPortPriorityOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceEthernetPortChannelMemberLinks:
    interface: ParcelReferenceDef
    lacp_mode: Union[
        EthernetOneOfLacpModeOptionsDef1, OneOfLacpModeOptionsDef2, EthernetOneOfLacpModeOptionsDef3
    ] = _field(metadata={"alias": "lacpMode"})
    lacp_port_priority: Optional[
        Union[
            EthernetOneOfLacpPortPriorityOptionsDef1,
            OneOfLacpPortPriorityOptionsDef2,
            OneOfLacpPortPriorityOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "lacpPortPriority"})
    lacp_rate: Optional[
        Union[EthernetOneOfLacpRateOptionsDef1, OneOfLacpRateOptionsDef2, OneOfLacpRateOptionsDef3]
    ] = _field(default=None, metadata={"alias": "lacpRate"})


@dataclass
class EthernetLacpModeMainInterface:
    # Configure Port-Channel member links
    port_channel_member_links: List[InterfaceEthernetPortChannelMemberLinks] = _field(
        metadata={"alias": "portChannelMemberLinks"}
    )
    lacp_fast_switchover: Optional[
        Union[
            OneOfLacpFastSwitchoverOptionsDef1,
            OneOfLacpFastSwitchoverOptionsDef2,
            OneOfLacpFastSwitchoverOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "lacpFastSwitchover"})
    lacp_max_bundle: Optional[
        Union[
            EthernetOneOfLacpMaxBundleOptionsDef1,
            OneOfLacpMaxBundleOptionsDef2,
            OneOfLacpMaxBundleOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "lacpMaxBundle"})
    lacp_min_bundle: Optional[
        Union[
            EthernetOneOfLacpMinBundleOptionsDef1,
            OneOfLacpMinBundleOptionsDef2,
            OneOfLacpMinBundleOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "lacpMinBundle"})
    load_balance: Optional[
        Union[
            EthernetOneOfPortChannelLoadBalanceOptionsDef1,
            OneOfPortChannelLoadBalanceOptionsDef2,
            OneOfPortChannelLoadBalanceOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "loadBalance"})
    port_channel_qos_aggregate: Optional[
        Union[
            OneOfPortChannelQosAggregateOptionsDef1,
            OneOfPortChannelQosAggregateOptionsDef2,
            OneOfPortChannelQosAggregateOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "portChannelQosAggregate"})


@dataclass
class EthernetMainInterface1:
    """
    Port-channel Lacp mode Main Interface
    """

    lacp_mode_main_interface: EthernetLacpModeMainInterface = _field(
        metadata={"alias": "lacpModeMainInterface"}
    )


@dataclass
class InterfaceEthernetOneOfPortChannelLoadBalanceOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceEthernetPortChannelLoadBalanceDef  # pytype: disable=annotation-type-mismatch


@dataclass
class VpnInterfaceEthernetPortChannelMemberLinks:
    interface: ParcelReferenceDef


@dataclass
class EthernetStaticModeMainInterface:
    # Configure Port-Channel member links
    port_channel_member_links: List[VpnInterfaceEthernetPortChannelMemberLinks] = _field(
        metadata={"alias": "portChannelMemberLinks"}
    )
    load_balance: Optional[
        Union[
            InterfaceEthernetOneOfPortChannelLoadBalanceOptionsDef1,
            OneOfPortChannelLoadBalanceOptionsDef2,
            OneOfPortChannelLoadBalanceOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "loadBalance"})
    port_channel_qos_aggregate: Optional[
        Union[
            OneOfPortChannelQosAggregateOptionsDef1,
            OneOfPortChannelQosAggregateOptionsDef2,
            OneOfPortChannelQosAggregateOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "portChannelQosAggregate"})


@dataclass
class EthernetMainInterface2:
    """
    Port-channel Static mode Main Interface
    """

    static_mode_main_interface: EthernetStaticModeMainInterface = _field(
        metadata={"alias": "staticModeMainInterface"}
    )


@dataclass
class EthernetPortChannel1:
    """
    Port-channel Main Interface
    """

    main_interface: Union[EthernetMainInterface1, EthernetMainInterface2] = _field(
        metadata={"alias": "mainInterface"}
    )


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
class EthernetOneOfIpV4AddressOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class EthernetStaticIpV4AddressPrimary:
    """
    Static IpV4Address Primary
    """

    ip_address: Union[
        OneOfIpV4AddressOptionsDef1,
        EthernetOneOfIpV4AddressOptionsDef2,
        OneOfIpV4AddressOptionsDef3,
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
class EthernetOneOfBandwidthUpstreamOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class EthernetOneOfBandwidthDownstreamOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class EthernetOneOfModeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EthernetModeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class EthernetOneOfBindOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class EthernetOneOfCarrierOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EthernetCarrierDef


@dataclass
class EthernetOneOfCarrierOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EthernetDefaultCarrierDef  # pytype: disable=annotation-type-mismatch


@dataclass
class EthernetOneOfColorOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EthernetColorDef  # pytype: disable=annotation-type-mismatch


@dataclass
class EthernetOneOfHelloIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class EthernetOneOfHelloIntervalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class EthernetOneOfHelloToleranceOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class EthernetOneOfHelloToleranceOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class EthernetOneOfTlocExtensionGreToOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class EthernetOneOfGroupOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class EthernetOneOfMaxControlConnectionsOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class EthernetOneOfNatRefreshIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class EthernetOneOfNatRefreshIntervalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class EthernetOneOfControllerGroupListOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[int]


@dataclass
class EthernetOneOfVmanageConnectionPreferenceOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class EthernetOneOfVmanageConnectionPreferenceOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class EthernetOneOfTunnelTcpMssAdjustOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class EthernetTunnel:
    """
    Tunnel Interface Attributes
    """

    allow_fragmentation: Optional[
        Union[OneOfAllowFragmentationDef1, OneOfAllowFragmentationDef2, OneOfAllowFragmentationDef3]
    ] = _field(default=None, metadata={"alias": "allowFragmentation"})
    bandwidth_percent: Optional[
        Union[
            OneOfBandwidthPercentOptionsDef1,
            OneOfBandwidthPercentOptionsDef2,
            OneOfBandwidthPercentOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "bandwidthPercent"})
    bind: Optional[
        Union[EthernetOneOfBindOptionsDef1, OneOfBindOptionsDef2, OneOfBindOptionsDef3]
    ] = _field(default=None)
    border: Optional[
        Union[OneOfBorderOptionsDef1, OneOfBorderOptionsDef2, OneOfBorderOptionsDef3]
    ] = _field(default=None)
    carrier: Optional[
        Union[
            EthernetOneOfCarrierOptionsDef1,
            OneOfCarrierOptionsDef2,
            EthernetOneOfCarrierOptionsDef3,
        ]
    ] = _field(default=None)
    clear_dont_fragment: Optional[
        Union[
            OneOfClearDontFragmentOptionsDef1,
            OneOfClearDontFragmentOptionsDef2,
            OneOfClearDontFragmentOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "clearDontFragment"})
    color: Optional[
        Union[EthernetOneOfColorOptionsDef1, OneOfColorOptionsDef2, OneOfColorOptionsDef3]
    ] = _field(default=None)
    cts_sgt_propagation: Optional[
        Union[
            OneOfPropagateSgtOptionsDef1, OneOfPropagateSgtOptionsDef2, OneOfPropagateSgtOptionsDef3
        ]
    ] = _field(default=None, metadata={"alias": "ctsSgtPropagation"})
    exclude_controller_group_list: Optional[
        Union[
            EthernetOneOfControllerGroupListOptionsDef1,
            OneOfControllerGroupListOptionsDef2,
            OneOfControllerGroupListOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "excludeControllerGroupList"})
    group: Optional[
        Union[EthernetOneOfGroupOptionsDef1, OneOfGroupOptionsDef2, OneOfGroupOptionsDef3]
    ] = _field(default=None)
    hello_interval: Optional[
        Union[
            EthernetOneOfHelloIntervalOptionsDef1,
            OneOfHelloIntervalOptionsDef2,
            EthernetOneOfHelloIntervalOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "helloInterval"})
    hello_tolerance: Optional[
        Union[
            EthernetOneOfHelloToleranceOptionsDef1,
            OneOfHelloToleranceOptionsDef2,
            EthernetOneOfHelloToleranceOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "helloTolerance"})
    last_resort_circuit: Optional[
        Union[
            OneOfLastResortCircuitOptionsDef1,
            OneOfLastResortCircuitOptionsDef2,
            OneOfLastResortCircuitOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "lastResortCircuit"})
    low_bandwidth_link: Optional[
        Union[
            OneOfLowBandwidthLinkOptionsDef1,
            OneOfLowBandwidthLinkOptionsDef2,
            OneOfLowBandwidthLinkOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "lowBandwidthLink"})
    max_control_connections: Optional[
        Union[
            EthernetOneOfMaxControlConnectionsOptionsDef1,
            OneOfMaxControlConnectionsOptionsDef2,
            OneOfMaxControlConnectionsOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "maxControlConnections"})
    mode: Optional[Union[EthernetOneOfModeOptionsDef1, OneOfModeOptionsDef2]] = _field(default=None)
    nat_refresh_interval: Optional[
        Union[
            EthernetOneOfNatRefreshIntervalOptionsDef1,
            OneOfNatRefreshIntervalOptionsDef2,
            EthernetOneOfNatRefreshIntervalOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "natRefreshInterval"})
    network_broadcast: Optional[
        Union[
            OneOfNetworkBroadcastOptionsDef1,
            OneOfNetworkBroadcastOptionsDef2,
            OneOfNetworkBroadcastOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "networkBroadcast"})
    per_tunnel_qos: Optional[
        Union[
            OneOfPerTunnelQosOptionsDef1, OneOfPerTunnelQosOptionsDef2, OneOfPerTunnelQosOptionsDef3
        ]
    ] = _field(default=None, metadata={"alias": "perTunnelQos"})
    port_hop: Optional[
        Union[OneOfPortHopOptionsDef1, OneOfPortHopOptionsDef2, OneOfPortHopOptionsDef3]
    ] = _field(default=None, metadata={"alias": "portHop"})
    restrict: Optional[
        Union[OneOfRestrictOptionsDef1, OneOfRestrictOptionsDef2, OneOfRestrictOptionsDef3]
    ] = _field(default=None)
    set_sdwan_tunnel_mtu_to_max: Optional[
        Union[
            OneOfSetSdwanTunnelMtuToMaxDef1,
            OneOfSetSdwanTunnelMtuToMaxDef2,
            OneOfSetSdwanTunnelMtuToMaxDef3,
        ]
    ] = _field(default=None, metadata={"alias": "setSdwanTunnelMTUToMax"})
    tloc_extension_gre_to: Optional[
        Union[
            EthernetOneOfTlocExtensionGreToOptionsDef1,
            OneOfTlocExtensionGreToOptionsDef2,
            OneOfTlocExtensionGreToOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tlocExtensionGreTo"})
    tunnel_tcp_mss: Optional[
        Union[
            EthernetOneOfTunnelTcpMssAdjustOptionsDef1,
            OneOfTunnelTcpMssAdjustOptionsDef2,
            OneOfTunnelTcpMssAdjustOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tunnelTcpMss"})
    v_bond_as_stun_server: Optional[
        Union[
            OneOfVbondAsStunServerOptionsDef1,
            OneOfVbondAsStunServerOptionsDef2,
            OneOfVbondAsStunServerOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "vBondAsStunServer"})
    v_manage_connection_preference: Optional[
        Union[
            EthernetOneOfVmanageConnectionPreferenceOptionsDef1,
            OneOfVmanageConnectionPreferenceOptionsDef2,
            EthernetOneOfVmanageConnectionPreferenceOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "vManageConnectionPreference"})


@dataclass
class EthernetAllowService:
    """
    Tunnel Interface Attributes
    """

    all: Optional[
        Union[OneOfAllowAllOptionsDef1, OneOfAllowAllOptionsDef2, OneOfAllowAllOptionsDef3]
    ] = _field(default=None)
    bfd: Optional[
        Union[
            OneOfAllowServiceFalseOptionsDef1,
            OneOfAllowServiceFalseOptionsDef2,
            OneOfAllowServiceFalseOptionsDef3,
        ]
    ] = _field(default=None)
    bgp: Optional[
        Union[OneOfAllowBgpOptionsDef1, OneOfAllowBgpOptionsDef2, OneOfAllowBgpOptionsDef3]
    ] = _field(default=None)
    dhcp: Optional[
        Union[OneOfAllowDhcpOptionsDef1, OneOfAllowDhcpOptionsDef2, OneOfAllowDhcpOptionsDef3]
    ] = _field(default=None)
    dns: Optional[
        Union[
            OneOfAllowServiceTrueOptionsDef1,
            OneOfAllowServiceTrueOptionsDef2,
            OneOfAllowServiceTrueOptionsDef3,
        ]
    ] = _field(default=None)
    https: Optional[
        Union[
            OneOfAllowServiceTrueOptionsDef1,
            OneOfAllowServiceTrueOptionsDef2,
            OneOfAllowServiceTrueOptionsDef3,
        ]
    ] = _field(default=None)
    icmp: Optional[
        Union[
            OneOfAllowServiceTrueOptionsDef1,
            OneOfAllowServiceTrueOptionsDef2,
            OneOfAllowServiceTrueOptionsDef3,
        ]
    ] = _field(default=None)
    netconf: Optional[
        Union[
            OneOfAllowServiceFalseOptionsDef1,
            OneOfAllowServiceFalseOptionsDef2,
            OneOfAllowServiceFalseOptionsDef3,
        ]
    ] = _field(default=None)
    ntp: Optional[
        Union[OneOfAllowNtpOptionsDef1, OneOfAllowNtpOptionsDef2, OneOfAllowNtpOptionsDef3]
    ] = _field(default=None)
    ospf: Optional[
        Union[
            OneOfAllowServiceFalseOptionsDef1,
            OneOfAllowServiceFalseOptionsDef2,
            OneOfAllowServiceFalseOptionsDef3,
        ]
    ] = _field(default=None)
    snmp: Optional[
        Union[
            OneOfAllowServiceFalseOptionsDef1,
            OneOfAllowServiceFalseOptionsDef2,
            OneOfAllowServiceFalseOptionsDef3,
        ]
    ] = _field(default=None)
    ssh: Optional[
        Union[OneOfAllowSshOptionsDef1, OneOfAllowSshOptionsDef2, OneOfAllowSshOptionsDef3]
    ] = _field(default=None)
    stun: Optional[
        Union[
            OneOfAllowServiceFalseOptionsDef1,
            OneOfAllowServiceFalseOptionsDef2,
            OneOfAllowServiceFalseOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class EthernetOneOfEncapsulationEncapOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EthernetEncapsulationEncapDef  # pytype: disable=annotation-type-mismatch


@dataclass
class EthernetOneOfEncapsulationPreferenceOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class EthernetOneOfEncapsulationWeightOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class EthernetOneOfEncapsulationWeightOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class EthernetEncapsulation:
    encap: EthernetOneOfEncapsulationEncapOptionsDef
    preference: Optional[
        Union[
            EthernetOneOfEncapsulationPreferenceOptionsDef1,
            OneOfEncapsulationPreferenceOptionsDef2,
            OneOfEncapsulationPreferenceOptionsDef3,
        ]
    ] = _field(default=None)
    weight: Optional[
        Union[
            EthernetOneOfEncapsulationWeightOptionsDef1,
            OneOfEncapsulationWeightOptionsDef2,
            EthernetOneOfEncapsulationWeightOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class EthernetOneOfCoreRegionDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EthernetCoreRegionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class EthernetOneOfCoreRegionDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EthernetDefaultCoreRegionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class EthernetOneOfSecondaryRegionDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EthernetSecondaryRegionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class EthernetOneOfSecondaryRegionDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EthernetDefaultSecondaryRegionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class EthernetMultiRegionFabric:
    """
    Multi-Region Fabric
    """

    core_region: Optional[Union[EthernetOneOfCoreRegionDef1, EthernetOneOfCoreRegionDef2]] = _field(
        default=None, metadata={"alias": "coreRegion"}
    )
    enable_core_region: Optional[Union[OneOfEnableRegionDef1, OneOfEnableRegionDef2]] = _field(
        default=None, metadata={"alias": "enableCoreRegion"}
    )
    enable_secondary_region: Optional[Union[OneOfEnableRegionDef1, OneOfEnableRegionDef2]] = _field(
        default=None, metadata={"alias": "enableSecondaryRegion"}
    )
    secondary_region: Optional[
        Union[EthernetOneOfSecondaryRegionDef1, EthernetOneOfSecondaryRegionDef2]
    ] = _field(default=None, metadata={"alias": "secondaryRegion"})


@dataclass
class EthernetOneOfNatTypeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EthernetNatChoiceDef


@dataclass
class EthernetOneOfNatTypeOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EthernetDefaultNatChoiceDef  # pytype: disable=annotation-type-mismatch


@dataclass
class EthernetOneOfNatPoolRangeStartOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class EthernetOneOfNatPoolRangeEndOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class EthernetOneOfNatPoolPrefixLengthOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class EthernetNatPool:
    """
    NAT Pool
    """

    prefix_length: Union[
        OneOfNatPoolPrefixLengthOptionsDef1, EthernetOneOfNatPoolPrefixLengthOptionsDef2
    ] = _field(metadata={"alias": "prefixLength"})
    range_end: Union[OneOfNatPoolRangeEndOptionsDef1, EthernetOneOfNatPoolRangeEndOptionsDef2] = (
        _field(metadata={"alias": "rangeEnd"})
    )
    range_start: Union[
        OneOfNatPoolRangeStartOptionsDef1, EthernetOneOfNatPoolRangeStartOptionsDef2
    ] = _field(metadata={"alias": "rangeStart"})
    overload: Optional[
        Union[
            OneOfNatPoolOverloadOptionsDef1,
            OneOfNatPoolOverloadOptionsDef2,
            OneOfNatPoolOverloadOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class EthernetOneOfNatPoolNameOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceEthernetOneOfNatPoolRangeStartOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class InterfaceEthernetOneOfNatPoolRangeEndOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class InterfaceEthernetOneOfNatPoolPrefixLengthOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class EthernetMultiplePool:
    name: Union[OneOfNatPoolNameOptionsDef1, EthernetOneOfNatPoolNameOptionsDef2]
    overload: Union[
        OneOfNatPoolOverloadOptionsDef1,
        OneOfNatPoolOverloadOptionsDef2,
        OneOfNatPoolOverloadOptionsDef3,
    ]
    prefix_length: Union[
        OneOfNatPoolPrefixLengthOptionsDef1, InterfaceEthernetOneOfNatPoolPrefixLengthOptionsDef2
    ] = _field(metadata={"alias": "prefixLength"})
    range_end: Union[
        OneOfNatPoolRangeEndOptionsDef1, InterfaceEthernetOneOfNatPoolRangeEndOptionsDef2
    ] = _field(metadata={"alias": "rangeEnd"})
    range_start: Union[
        OneOfNatPoolRangeStartOptionsDef1, InterfaceEthernetOneOfNatPoolRangeStartOptionsDef2
    ] = _field(metadata={"alias": "rangeStart"})
    enable_dual_router_ha_mapping: Optional[
        Union[
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef1,
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "enableDualRouterHAMapping"})


@dataclass
class EthernetMultipleLoopback:
    loopback_interface: Union[
        OneOfLoopbackInterfaceOptionsDef1,
        OneOfLoopbackInterfaceOptionsDef2,
        OneOfLoopbackInterfaceOptionsDef3,
    ] = _field(metadata={"alias": "loopbackInterface"})


@dataclass
class EthernetOneOfUdpTimeoutOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class EthernetOneOfUdpTimeoutOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class EthernetOneOfTcpTimeoutOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class EthernetOneOfTcpTimeoutOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class EthernetOneOfStaticSourceIpOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class EthernetOneOfStaticTranslateIpOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class EthernetOneOfStaticNatDirectionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EthernetStaticNatDirectionDef


@dataclass
class EthernetOneOfStaticNatDirectionOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EthernetDefaultStaticNatDirectionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class EthernetOneOfStaticSourceVpnOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class EthernetOneOfStaticSourceVpnOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class EthernetNewStaticNat:
    source_ip: Union[EthernetOneOfStaticSourceIpOptionsDef1, OneOfStaticSourceIpOptionsDef2] = (
        _field(metadata={"alias": "sourceIp"})
    )
    source_vpn: Union[
        EthernetOneOfStaticSourceVpnOptionsDef1,
        OneOfStaticSourceVpnOptionsDef2,
        EthernetOneOfStaticSourceVpnOptionsDef3,
    ] = _field(metadata={"alias": "sourceVpn"})
    static_nat_direction: Union[
        EthernetOneOfStaticNatDirectionOptionsDef1, EthernetOneOfStaticNatDirectionOptionsDef2
    ] = _field(metadata={"alias": "staticNatDirection"})
    translate_ip: Union[
        EthernetOneOfStaticTranslateIpOptionsDef1, OneOfStaticTranslateIpOptionsDef2
    ] = _field(metadata={"alias": "translateIp"})
    enable_dual_router_ha_mapping: Optional[
        Union[
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef1,
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "enableDualRouterHAMapping"})


@dataclass
class EthernetOneOfStaticPortForwardProtocolOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EthernetStaticPortForwardProtocolDef  # pytype: disable=annotation-type-mismatch


@dataclass
class InterfaceEthernetOneOfStaticSourceIpOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class EthernetOneOfStaticSourcePortOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceEthernetOneOfStaticTranslateIpOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class EthernetOneOfStaticTranslatePortOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceEthernetOneOfStaticNatDirectionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceEthernetStaticNatDirectionDef


@dataclass
class InterfaceEthernetOneOfStaticNatDirectionOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceEthernetDefaultStaticNatDirectionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class InterfaceEthernetOneOfStaticSourceVpnOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceEthernetOneOfStaticSourceVpnOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class EthernetStaticPortForward:
    protocol: Union[
        EthernetOneOfStaticPortForwardProtocolOptionsDef1, OneOfStaticPortForwardProtocolOptionsDef2
    ]
    source_ip: Union[
        InterfaceEthernetOneOfStaticSourceIpOptionsDef1, OneOfStaticSourceIpOptionsDef2
    ] = _field(metadata={"alias": "sourceIp"})
    source_port: Union[
        EthernetOneOfStaticSourcePortOptionsDef1, OneOfStaticSourcePortOptionsDef2
    ] = _field(metadata={"alias": "sourcePort"})
    source_vpn: Union[
        InterfaceEthernetOneOfStaticSourceVpnOptionsDef1,
        OneOfStaticSourceVpnOptionsDef2,
        InterfaceEthernetOneOfStaticSourceVpnOptionsDef3,
    ] = _field(metadata={"alias": "sourceVpn"})
    static_nat_direction: Union[
        InterfaceEthernetOneOfStaticNatDirectionOptionsDef1,
        InterfaceEthernetOneOfStaticNatDirectionOptionsDef2,
    ] = _field(metadata={"alias": "staticNatDirection"})
    translate_ip: Union[
        InterfaceEthernetOneOfStaticTranslateIpOptionsDef1, OneOfStaticTranslateIpOptionsDef2
    ] = _field(metadata={"alias": "translateIp"})
    translate_port: Union[
        EthernetOneOfStaticTranslatePortOptionsDef1, OneOfStaticTranslatePortOptionsDef2
    ] = _field(metadata={"alias": "translatePort"})
    enable_dual_router_ha_mapping: Optional[
        Union[
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef1,
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "enableDualRouterHAMapping"})


@dataclass
class EthernetNatAttributesIpv4:
    """
    NAT Attributes IpV4
    """

    nat_type: Union[EthernetOneOfNatTypeOptionsDef1, EthernetOneOfNatTypeOptionsDef2] = _field(
        metadata={"alias": "natType"}
    )
    tcp_timeout: Union[
        EthernetOneOfTcpTimeoutOptionsDef1,
        OneOfTcpTimeoutOptionsDef2,
        EthernetOneOfTcpTimeoutOptionsDef3,
    ] = _field(metadata={"alias": "tcpTimeout"})
    udp_timeout: Union[
        EthernetOneOfUdpTimeoutOptionsDef1,
        OneOfUdpTimeoutOptionsDef2,
        EthernetOneOfUdpTimeoutOptionsDef3,
    ] = _field(metadata={"alias": "udpTimeout"})
    match_interface: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "matchInterface"})
    # NAT Multiple Loopback
    multiple_loopback: Optional[List[EthernetMultipleLoopback]] = _field(
        default=None, metadata={"alias": "multipleLoopback"}
    )
    # NAT Multiple Pool
    multiple_pool: Optional[List[EthernetMultiplePool]] = _field(
        default=None, metadata={"alias": "multiplePool"}
    )
    nat_loopback: Optional[
        Union[
            OneOfLoopbackInterfaceOptionsDef1,
            OneOfLoopbackInterfaceOptionsDef2,
            OneOfLoopbackInterfaceOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "natLoopback"})
    # NAT Pool
    nat_pool: Optional[EthernetNatPool] = _field(default=None, metadata={"alias": "natPool"})
    # static NAT
    new_static_nat: Optional[List[EthernetNewStaticNat]] = _field(
        default=None, metadata={"alias": "newStaticNat"}
    )
    # Configure Port Forward entries
    static_port_forward: Optional[List[EthernetStaticPortForward]] = _field(
        default=None, metadata={"alias": "staticPortForward"}
    )


@dataclass
class EthernetOneOfStaticNat66TranslatedSourcePrefixOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class EthernetOneOfStaticNat66SourceVpnIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class EthernetStaticNat66:
    source_prefix: Union[
        OneOfStaticNat66SourcePrefixOptionsDef1, OneOfStaticNat66SourcePrefixOptionsDef2
    ] = _field(metadata={"alias": "sourcePrefix"})
    source_vpn_id: Union[
        EthernetOneOfStaticNat66SourceVpnIdOptionsDef1,
        OneOfStaticNat66SourceVpnIdOptionsDef2,
        OneOfStaticNat66SourceVpnIdOptionsDef3,
    ] = _field(metadata={"alias": "sourceVpnId"})
    egress_interface: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "egressInterface"})
    translated_source_prefix: Optional[
        Union[
            EthernetOneOfStaticNat66TranslatedSourcePrefixOptionsDef1,
            OneOfStaticNat66TranslatedSourcePrefixOptionsDef2,
            OneOfStaticNat66TranslatedSourcePrefixOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "translatedSourcePrefix"})


@dataclass
class EthernetNatAttributesIpv6:
    """
    NAT Attributes Ipv6
    """

    nat64: Optional[Union[OneOfNat64Nat66OptionsDef1, OneOfNat64Nat66OptionsDef2]] = _field(
        default=None
    )
    nat66: Optional[Union[OneOfNat64Nat66OptionsDef1, OneOfNat64Nat66OptionsDef2]] = _field(
        default=None
    )
    # static NAT66
    static_nat66: Optional[List[EthernetStaticNat66]] = _field(
        default=None, metadata={"alias": "staticNat66"}
    )


@dataclass
class EthernetOneOfPeriodOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class EthernetOneOfPeriodOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class EthernetOneOfShapingRateUpOrDownstreamOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceEthernetOneOfShapingRateUpOrDownstreamOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VpnInterfaceEthernetOneOfShapingRateUpOrDownstreamOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class EthernetShapingRateUpstreamConfig:
    """
    adaptiveQoS Shaping Rate Upstream config
    """

    default_shaping_rate_upstream: Union[
        VpnInterfaceEthernetOneOfShapingRateUpOrDownstreamOptionsDef1,
        OneOfShapingRateUpOrDownstreamOptionsDef2,
    ] = _field(metadata={"alias": "defaultShapingRateUpstream"})
    max_shaping_rate_upstream: Union[
        InterfaceEthernetOneOfShapingRateUpOrDownstreamOptionsDef1,
        OneOfShapingRateUpOrDownstreamOptionsDef2,
    ] = _field(metadata={"alias": "maxShapingRateUpstream"})
    min_shaping_rate_upstream: Union[
        EthernetOneOfShapingRateUpOrDownstreamOptionsDef1, OneOfShapingRateUpOrDownstreamOptionsDef2
    ] = _field(metadata={"alias": "minShapingRateUpstream"})


@dataclass
class WanVpnInterfaceEthernetOneOfShapingRateUpOrDownstreamOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class TransportWanVpnInterfaceEthernetOneOfShapingRateUpOrDownstreamOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SdwanTransportWanVpnInterfaceEthernetOneOfShapingRateUpOrDownstreamOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class EthernetShapingRateDownstreamConfig:
    """
    adaptiveQoS Shaping Rate Downstream config
    """

    default_shaping_rate_downstream: Union[
        SdwanTransportWanVpnInterfaceEthernetOneOfShapingRateUpOrDownstreamOptionsDef1,
        OneOfShapingRateUpOrDownstreamOptionsDef2,
    ] = _field(metadata={"alias": "defaultShapingRateDownstream"})
    max_shaping_rate_downstream: Union[
        TransportWanVpnInterfaceEthernetOneOfShapingRateUpOrDownstreamOptionsDef1,
        OneOfShapingRateUpOrDownstreamOptionsDef2,
    ] = _field(metadata={"alias": "maxShapingRateDownstream"})
    min_shaping_rate_downstream: Union[
        WanVpnInterfaceEthernetOneOfShapingRateUpOrDownstreamOptionsDef1,
        OneOfShapingRateUpOrDownstreamOptionsDef2,
    ] = _field(metadata={"alias": "minShapingRateDownstream"})


@dataclass
class EthernetAclQos1:
    adaptive_qo_s: Union[OneOfQosAdaptiveOptionsDef1, OneOfQosAdaptiveOptionsDef2] = _field(
        metadata={"alias": "adaptiveQoS"}
    )
    shaping_rate_upstream: ShapingRateUpstream = _field(metadata={"alias": "shapingRateUpstream"})
    # adaptiveQoS Shaping Rate Upstream config
    shaping_rate_upstream_config: EthernetShapingRateUpstreamConfig = _field(
        metadata={"alias": "shapingRateUpstreamConfig"}
    )
    adapt_period: Optional[
        Union[
            EthernetOneOfPeriodOptionsDef1, OneOfPeriodOptionsDef2, EthernetOneOfPeriodOptionsDef3
        ]
    ] = _field(default=None, metadata={"alias": "adaptPeriod"})
    ipv4_acl_egress: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "ipv4AclEgress"}
    )
    ipv4_acl_ingress: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "ipv4AclIngress"}
    )
    ipv6_acl_egress: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "ipv6AclEgress"}
    )
    ipv6_acl_ingress: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "ipv6AclIngress"}
    )
    shaping_rate: Optional[
        Union[OneOfShapingRateOptionsDef1, OneOfShapingRateOptionsDef2, OneOfShapingRateOptionsDef3]
    ] = _field(default=None, metadata={"alias": "shapingRate"})
    shaping_rate_downstream: Optional[
        Union[OneOfShapingRateDownstreamOptionsDef1, OneOfShapingRateDownstreamOptionsDef2]
    ] = _field(default=None, metadata={"alias": "shapingRateDownstream"})
    # adaptiveQoS Shaping Rate Downstream config
    shaping_rate_downstream_config: Optional[EthernetShapingRateDownstreamConfig] = _field(
        default=None, metadata={"alias": "shapingRateDownstreamConfig"}
    )


@dataclass
class InterfaceEthernetOneOfPeriodOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceEthernetOneOfPeriodOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class FeatureProfileSdwanTransportWanVpnInterfaceEthernetOneOfShapingRateUpOrDownstreamOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class V1FeatureProfileSdwanTransportWanVpnInterfaceEthernetOneOfShapingRateUpOrDownstreamOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfShapingRateUpOrDownstreamOptionsDef11:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceEthernetShapingRateUpstreamConfig:
    """
    adaptiveQoS Shaping Rate Upstream config
    """

    default_shaping_rate_upstream: Union[
        OneOfShapingRateUpOrDownstreamOptionsDef11, OneOfShapingRateUpOrDownstreamOptionsDef2
    ] = _field(metadata={"alias": "defaultShapingRateUpstream"})
    max_shaping_rate_upstream: Union[
        V1FeatureProfileSdwanTransportWanVpnInterfaceEthernetOneOfShapingRateUpOrDownstreamOptionsDef1,
        OneOfShapingRateUpOrDownstreamOptionsDef2,
    ] = _field(metadata={"alias": "maxShapingRateUpstream"})
    min_shaping_rate_upstream: Union[
        FeatureProfileSdwanTransportWanVpnInterfaceEthernetOneOfShapingRateUpOrDownstreamOptionsDef1,
        OneOfShapingRateUpOrDownstreamOptionsDef2,
    ] = _field(metadata={"alias": "minShapingRateUpstream"})


@dataclass
class OneOfShapingRateUpOrDownstreamOptionsDef12:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfShapingRateUpOrDownstreamOptionsDef13:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfShapingRateUpOrDownstreamOptionsDef14:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceEthernetShapingRateDownstreamConfig:
    """
    adaptiveQoS Shaping Rate Downstream config
    """

    default_shaping_rate_downstream: Union[
        OneOfShapingRateUpOrDownstreamOptionsDef14, OneOfShapingRateUpOrDownstreamOptionsDef2
    ] = _field(metadata={"alias": "defaultShapingRateDownstream"})
    max_shaping_rate_downstream: Union[
        OneOfShapingRateUpOrDownstreamOptionsDef13, OneOfShapingRateUpOrDownstreamOptionsDef2
    ] = _field(metadata={"alias": "maxShapingRateDownstream"})
    min_shaping_rate_downstream: Union[
        OneOfShapingRateUpOrDownstreamOptionsDef12, OneOfShapingRateUpOrDownstreamOptionsDef2
    ] = _field(metadata={"alias": "minShapingRateDownstream"})


@dataclass
class EthernetAclQos2:
    adaptive_qo_s: Union[OneOfQosAdaptiveOptionsDef1, OneOfQosAdaptiveOptionsDef2] = _field(
        metadata={"alias": "adaptiveQoS"}
    )
    adapt_period: Optional[
        Union[
            InterfaceEthernetOneOfPeriodOptionsDef1,
            OneOfPeriodOptionsDef2,
            InterfaceEthernetOneOfPeriodOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "adaptPeriod"})
    ipv4_acl_egress: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "ipv4AclEgress"}
    )
    ipv4_acl_ingress: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "ipv4AclIngress"}
    )
    ipv6_acl_egress: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "ipv6AclEgress"}
    )
    ipv6_acl_ingress: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "ipv6AclIngress"}
    )
    shaping_rate: Optional[
        Union[OneOfShapingRateOptionsDef1, OneOfShapingRateOptionsDef2, OneOfShapingRateOptionsDef3]
    ] = _field(default=None, metadata={"alias": "shapingRate"})
    shaping_rate_downstream: Optional[
        Union[OneOfShapingRateDownstreamOptionsDef1, OneOfShapingRateDownstreamOptionsDef2]
    ] = _field(default=None, metadata={"alias": "shapingRateDownstream"})
    # adaptiveQoS Shaping Rate Downstream config
    shaping_rate_downstream_config: Optional[InterfaceEthernetShapingRateDownstreamConfig] = _field(
        default=None, metadata={"alias": "shapingRateDownstreamConfig"}
    )
    shaping_rate_upstream: Optional[
        Union[OneOfShapingRateUpstreamOptionsDef1, OneOfShapingRateUpstreamOptionsDef2]
    ] = _field(default=None, metadata={"alias": "shapingRateUpstream"})
    # adaptiveQoS Shaping Rate Upstream config
    shaping_rate_upstream_config: Optional[InterfaceEthernetShapingRateUpstreamConfig] = _field(
        default=None, metadata={"alias": "shapingRateUpstreamConfig"}
    )


@dataclass
class InterfaceEthernetOneOfIpV4AddressOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class EthernetArp:
    ip_address: Union[
        OneOfIpV4AddressOptionsDef1,
        InterfaceEthernetOneOfIpV4AddressOptionsDef2,
        OneOfIpV4AddressOptionsDef3,
    ] = _field(metadata={"alias": "ipAddress"})
    mac_address: Union[
        OneOfMacAddressOptionsDef1, OneOfMacAddressOptionsDef2, OneOfMacAddressOptionsDef3
    ] = _field(metadata={"alias": "macAddress"})


@dataclass
class EthernetOneOfDuplexOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EthernetDuplexDef  # pytype: disable=annotation-type-mismatch


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
class EthernetOneOfIntrfMtuOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
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
class EthernetOneOfTlocExtensionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class EthernetOneOfTlocExtensionGreFromOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class EthernetOneOfXconnectOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class EthernetTlocExtensionGreFrom:
    """
    Extend remote TLOC over a GRE tunnel to a local WAN interface
    """

    source_ip: Optional[
        Union[
            EthernetOneOfTlocExtensionGreFromOptionsDef1,
            OneOfTlocExtensionGreFromOptionsDef2,
            OneOfTlocExtensionGreFromOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sourceIp"})
    xconnect: Optional[
        Union[EthernetOneOfXconnectOptionsDef1, OneOfXconnectOptionsDef2, OneOfXconnectOptionsDef3]
    ] = _field(default=None)


@dataclass
class EthernetOneOfLoadIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class EthernetOneOfTrackerOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class EthernetAdvanced:
    """
    Advanced Attributes
    """

    arp_timeout: Optional[
        Union[
            EthernetOneOfArpTimeoutOptionsDef1,
            OneOfArpTimeoutOptionsDef2,
            EthernetOneOfArpTimeoutOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "arpTimeout"})
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
            OneOfOnBooleanDefaultTrueOptionsDef1,
            OneOfOnBooleanDefaultTrueOptionsDef2,
            OneOfOnBooleanDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "icmpRedirectDisable"})
    intrf_mtu: Optional[
        Union[
            EthernetOneOfIntrfMtuOptionsDef1,
            OneOfIntrfMtuOptionsDef2,
            EthernetOneOfIntrfMtuOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "intrfMtu"})
    ip_directed_broadcast: Optional[
        Union[
            OneOfIpDirectedBroadcastOptionsDef1,
            OneOfIpDirectedBroadcastOptionsDef2,
            OneOfIpDirectedBroadcastOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ipDirectedBroadcast"})
    ip_mtu: Optional[
        Union[EthernetOneOfMtuOptionsDef1, OneOfMtuOptionsDef2, EthernetOneOfMtuOptionsDef3]
    ] = _field(default=None, metadata={"alias": "ipMtu"})
    load_interval: Optional[
        Union[
            EthernetOneOfLoadIntervalOptionsDef1,
            OneOfLoadIntervalOptionsDef2,
            OneOfLoadIntervalOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "loadInterval"})
    mac_address: Optional[
        Union[OneOfMacAddressOptionsDef1, OneOfMacAddressOptionsDef2, OneOfMacAddressOptionsDef3]
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
    tloc_extension: Optional[
        Union[
            EthernetOneOfTlocExtensionOptionsDef1,
            OneOfTlocExtensionOptionsDef2,
            OneOfTlocExtensionOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tlocExtension"})
    # Extend remote TLOC over a GRE tunnel to a local WAN interface
    tloc_extension_gre_from: Optional[EthernetTlocExtensionGreFrom] = _field(
        default=None, metadata={"alias": "tlocExtensionGreFrom"}
    )
    tracker: Optional[
        Union[EthernetOneOfTrackerOptionsDef1, OneOfTrackerOptionsDef2, OneOfTrackerOptionsDef3]
    ] = _field(default=None)


@dataclass
class VpnInterfaceEthernetData:
    description: Union[
        OneOfDescriptionOptionsDef1, OneOfDescriptionOptionsDef2, OneOfDescriptionOptionsDef3
    ]
    interface_name: Union[OneOfInterfaceNameOptionsDef1, OneOfInterfaceNameOptionsDef2] = _field(
        metadata={"alias": "interfaceName"}
    )
    shutdown: Union[OneOfShutdownOptionsDef1, OneOfShutdownOptionsDef2, OneOfShutdownOptionsDef3]
    tunnel_interface: Union[OneOfTunnelInterfaceOptionsDef1, OneOfTunnelInterfaceOptionsDef2] = (
        _field(metadata={"alias": "tunnelInterface"})
    )
    # ACL/QOS
    acl_qos: Optional[Union[EthernetAclQos1, EthernetAclQos2]] = _field(
        default=None, metadata={"alias": "aclQos"}
    )
    # Advanced Attributes
    advanced: Optional[EthernetAdvanced] = _field(default=None)
    # Tunnel Interface Attributes
    allow_service: Optional[EthernetAllowService] = _field(
        default=None, metadata={"alias": "allowService"}
    )
    # Configure ARP entries
    arp: Optional[List[EthernetArp]] = _field(default=None)
    auto_detect_bandwidth: Optional[
        Union[
            OneOfAutoBandwidthDetectOptionsDef1,
            OneOfAutoBandwidthDetectOptionsDef2,
            OneOfAutoBandwidthDetectOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "autoDetectBandwidth"})
    bandwidth_downstream: Optional[
        Union[
            EthernetOneOfBandwidthDownstreamOptionsDef1,
            OneOfBandwidthDownstreamOptionsDef2,
            OneOfBandwidthDownstreamOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "bandwidthDownstream"})
    bandwidth_upstream: Optional[
        Union[
            EthernetOneOfBandwidthUpstreamOptionsDef1,
            OneOfBandwidthUpstreamOptionsDef2,
            OneOfBandwidthUpstreamOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "bandwidthUpstream"})
    block_non_source_ip: Optional[
        Union[
            OneOfBlockNonSourceIpOptionsDef1,
            OneOfBlockNonSourceIpOptionsDef2,
            OneOfBlockNonSourceIpOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "blockNonSourceIp"})
    dhcp_helper: Optional[
        Union[
            OneOfListOfIpV4OptionsDef1,
            EthernetOneOfListOfIpV4OptionsDef2,
            OneOfListOfIpV4OptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "dhcpHelper"})
    enable_ha_interlink_interface: Optional[
        Union[
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef1,
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "enableHAInterlinkInterface"})
    # Encapsulation for TLOC
    encapsulation: Optional[List[EthernetEncapsulation]] = _field(default=None)
    intf_ip_address: Optional[Union[EthernetIntfIpAddress1, EthernetIntfIpAddress2]] = _field(
        default=None, metadata={"alias": "intfIpAddress"}
    )
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
    # Multi-Region Fabric
    multi_region_fabric: Optional[EthernetMultiRegionFabric] = _field(
        default=None, metadata={"alias": "multiRegionFabric"}
    )
    nat: Optional[Union[OneOfNatOptionsDef1, OneOfNatOptionsDef2, OneOfNatOptionsDef3]] = _field(
        default=None
    )
    # NAT Attributes IpV4
    nat_attributes_ipv4: Optional[EthernetNatAttributesIpv4] = _field(
        default=None, metadata={"alias": "natAttributesIpv4"}
    )
    # NAT Attributes Ipv6
    nat_attributes_ipv6: Optional[EthernetNatAttributesIpv6] = _field(
        default=None, metadata={"alias": "natAttributesIpv6"}
    )
    nat_ipv6: Optional[Union[OneOfNatOptionsDef1, OneOfNatOptionsDef2, OneOfNatOptionsDef3]] = (
        _field(default=None, metadata={"alias": "natIpv6"})
    )
    port_channel: Optional[Union[EthernetPortChannel1, PortChannel2]] = _field(
        default=None, metadata={"alias": "portChannel"}
    )
    port_channel_interface: Optional[
        Union[OneOfPortChannelOptionsDef1, OneOfPortChannelOptionsDef2]
    ] = _field(default=None, metadata={"alias": "portChannelInterface"})
    port_channel_member_interface: Optional[
        Union[OneOfPortChannelMemberOptionsDef1, OneOfPortChannelMemberOptionsDef2]
    ] = _field(default=None, metadata={"alias": "portChannelMemberInterface"})
    service_provider: Optional[
        Union[
            OneOfServiceProviderOptionsDef1,
            OneOfServiceProviderOptionsDef2,
            OneOfServiceProviderOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "serviceProvider"})
    # Tunnel Interface Attributes
    tunnel: Optional[EthernetTunnel] = _field(default=None)


@dataclass
class EthernetPayload:
    """
    WAN VPN Interface Ethernet profile parcel schema for PUT request
    """

    data: VpnInterfaceEthernetData
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetSingleSdwanTransportWanVpnInterfaceEthernetPayload:
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
    # WAN VPN Interface Ethernet profile parcel schema for PUT request
    payload: Optional[EthernetPayload] = _field(default=None)


@dataclass
class EditWanVpnInterfaceEthernetParcelForTransportPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class VpnInterfaceEthernetOneOfPortChannelLoadBalanceOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: VpnInterfaceEthernetPortChannelLoadBalanceDef  # pytype: disable=annotation-type-mismatch


@dataclass
class InterfaceEthernetOneOfLacpMinBundleOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceEthernetOneOfLacpMaxBundleOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceEthernetOneOfLacpModeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceEthernetPortChannelLacpModeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class InterfaceEthernetOneOfLacpModeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceEthernetPortChannelLacpModeActiveDef  # pytype: disable=annotation-type-mismatch


@dataclass
class InterfaceEthernetOneOfLacpRateOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceEthernetLacpRateDef  # pytype: disable=annotation-type-mismatch


@dataclass
class InterfaceEthernetOneOfLacpPortPriorityOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class WanVpnInterfaceEthernetPortChannelMemberLinks:
    interface: ParcelReferenceDef
    lacp_mode: Union[
        InterfaceEthernetOneOfLacpModeOptionsDef1,
        OneOfLacpModeOptionsDef2,
        InterfaceEthernetOneOfLacpModeOptionsDef3,
    ] = _field(metadata={"alias": "lacpMode"})
    lacp_port_priority: Optional[
        Union[
            InterfaceEthernetOneOfLacpPortPriorityOptionsDef1,
            OneOfLacpPortPriorityOptionsDef2,
            OneOfLacpPortPriorityOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "lacpPortPriority"})
    lacp_rate: Optional[
        Union[
            InterfaceEthernetOneOfLacpRateOptionsDef1,
            OneOfLacpRateOptionsDef2,
            OneOfLacpRateOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "lacpRate"})


@dataclass
class InterfaceEthernetLacpModeMainInterface:
    # Configure Port-Channel member links
    port_channel_member_links: List[WanVpnInterfaceEthernetPortChannelMemberLinks] = _field(
        metadata={"alias": "portChannelMemberLinks"}
    )
    lacp_fast_switchover: Optional[
        Union[
            OneOfLacpFastSwitchoverOptionsDef1,
            OneOfLacpFastSwitchoverOptionsDef2,
            OneOfLacpFastSwitchoverOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "lacpFastSwitchover"})
    lacp_max_bundle: Optional[
        Union[
            InterfaceEthernetOneOfLacpMaxBundleOptionsDef1,
            OneOfLacpMaxBundleOptionsDef2,
            OneOfLacpMaxBundleOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "lacpMaxBundle"})
    lacp_min_bundle: Optional[
        Union[
            InterfaceEthernetOneOfLacpMinBundleOptionsDef1,
            OneOfLacpMinBundleOptionsDef2,
            OneOfLacpMinBundleOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "lacpMinBundle"})
    load_balance: Optional[
        Union[
            VpnInterfaceEthernetOneOfPortChannelLoadBalanceOptionsDef1,
            OneOfPortChannelLoadBalanceOptionsDef2,
            OneOfPortChannelLoadBalanceOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "loadBalance"})
    port_channel_qos_aggregate: Optional[
        Union[
            OneOfPortChannelQosAggregateOptionsDef1,
            OneOfPortChannelQosAggregateOptionsDef2,
            OneOfPortChannelQosAggregateOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "portChannelQosAggregate"})


@dataclass
class InterfaceEthernetMainInterface1:
    """
    Port-channel Lacp mode Main Interface
    """

    lacp_mode_main_interface: InterfaceEthernetLacpModeMainInterface = _field(
        metadata={"alias": "lacpModeMainInterface"}
    )


@dataclass
class WanVpnInterfaceEthernetOneOfPortChannelLoadBalanceOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: (
        WanVpnInterfaceEthernetPortChannelLoadBalanceDef  # pytype: disable=annotation-type-mismatch
    )


@dataclass
class TransportWanVpnInterfaceEthernetPortChannelMemberLinks:
    interface: ParcelReferenceDef


@dataclass
class InterfaceEthernetStaticModeMainInterface:
    # Configure Port-Channel member links
    port_channel_member_links: List[TransportWanVpnInterfaceEthernetPortChannelMemberLinks] = (
        _field(metadata={"alias": "portChannelMemberLinks"})
    )
    load_balance: Optional[
        Union[
            WanVpnInterfaceEthernetOneOfPortChannelLoadBalanceOptionsDef1,
            OneOfPortChannelLoadBalanceOptionsDef2,
            OneOfPortChannelLoadBalanceOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "loadBalance"})
    port_channel_qos_aggregate: Optional[
        Union[
            OneOfPortChannelQosAggregateOptionsDef1,
            OneOfPortChannelQosAggregateOptionsDef2,
            OneOfPortChannelQosAggregateOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "portChannelQosAggregate"})


@dataclass
class InterfaceEthernetMainInterface2:
    """
    Port-channel Static mode Main Interface
    """

    static_mode_main_interface: InterfaceEthernetStaticModeMainInterface = _field(
        metadata={"alias": "staticModeMainInterface"}
    )


@dataclass
class InterfaceEthernetPortChannel1:
    """
    Port-channel Main Interface
    """

    main_interface: Union[InterfaceEthernetMainInterface1, InterfaceEthernetMainInterface2] = (
        _field(metadata={"alias": "mainInterface"})
    )


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
class VpnInterfaceEthernetOneOfIpV4AddressOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class InterfaceEthernetStaticIpV4AddressPrimary:
    """
    Static IpV4Address Primary
    """

    ip_address: Union[
        OneOfIpV4AddressOptionsDef1,
        VpnInterfaceEthernetOneOfIpV4AddressOptionsDef2,
        OneOfIpV4AddressOptionsDef3,
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
class InterfaceEthernetOneOfBandwidthUpstreamOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceEthernetOneOfBandwidthDownstreamOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceEthernetOneOfModeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceEthernetModeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class InterfaceEthernetOneOfBindOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class InterfaceEthernetOneOfCarrierOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceEthernetCarrierDef


@dataclass
class InterfaceEthernetOneOfCarrierOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceEthernetDefaultCarrierDef  # pytype: disable=annotation-type-mismatch


@dataclass
class InterfaceEthernetOneOfColorOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceEthernetColorDef  # pytype: disable=annotation-type-mismatch


@dataclass
class InterfaceEthernetOneOfHelloIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceEthernetOneOfHelloIntervalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceEthernetOneOfHelloToleranceOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceEthernetOneOfHelloToleranceOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceEthernetOneOfTlocExtensionGreToOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class InterfaceEthernetOneOfGroupOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceEthernetOneOfMaxControlConnectionsOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceEthernetOneOfNatRefreshIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceEthernetOneOfNatRefreshIntervalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceEthernetOneOfControllerGroupListOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[int]


@dataclass
class InterfaceEthernetOneOfVmanageConnectionPreferenceOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceEthernetOneOfVmanageConnectionPreferenceOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceEthernetOneOfTunnelTcpMssAdjustOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceEthernetTunnel:
    """
    Tunnel Interface Attributes
    """

    allow_fragmentation: Optional[
        Union[OneOfAllowFragmentationDef1, OneOfAllowFragmentationDef2, OneOfAllowFragmentationDef3]
    ] = _field(default=None, metadata={"alias": "allowFragmentation"})
    bandwidth_percent: Optional[
        Union[
            OneOfBandwidthPercentOptionsDef1,
            OneOfBandwidthPercentOptionsDef2,
            OneOfBandwidthPercentOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "bandwidthPercent"})
    bind: Optional[
        Union[InterfaceEthernetOneOfBindOptionsDef1, OneOfBindOptionsDef2, OneOfBindOptionsDef3]
    ] = _field(default=None)
    border: Optional[
        Union[OneOfBorderOptionsDef1, OneOfBorderOptionsDef2, OneOfBorderOptionsDef3]
    ] = _field(default=None)
    carrier: Optional[
        Union[
            InterfaceEthernetOneOfCarrierOptionsDef1,
            OneOfCarrierOptionsDef2,
            InterfaceEthernetOneOfCarrierOptionsDef3,
        ]
    ] = _field(default=None)
    clear_dont_fragment: Optional[
        Union[
            OneOfClearDontFragmentOptionsDef1,
            OneOfClearDontFragmentOptionsDef2,
            OneOfClearDontFragmentOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "clearDontFragment"})
    color: Optional[
        Union[InterfaceEthernetOneOfColorOptionsDef1, OneOfColorOptionsDef2, OneOfColorOptionsDef3]
    ] = _field(default=None)
    cts_sgt_propagation: Optional[
        Union[
            OneOfPropagateSgtOptionsDef1, OneOfPropagateSgtOptionsDef2, OneOfPropagateSgtOptionsDef3
        ]
    ] = _field(default=None, metadata={"alias": "ctsSgtPropagation"})
    exclude_controller_group_list: Optional[
        Union[
            InterfaceEthernetOneOfControllerGroupListOptionsDef1,
            OneOfControllerGroupListOptionsDef2,
            OneOfControllerGroupListOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "excludeControllerGroupList"})
    group: Optional[
        Union[InterfaceEthernetOneOfGroupOptionsDef1, OneOfGroupOptionsDef2, OneOfGroupOptionsDef3]
    ] = _field(default=None)
    hello_interval: Optional[
        Union[
            InterfaceEthernetOneOfHelloIntervalOptionsDef1,
            OneOfHelloIntervalOptionsDef2,
            InterfaceEthernetOneOfHelloIntervalOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "helloInterval"})
    hello_tolerance: Optional[
        Union[
            InterfaceEthernetOneOfHelloToleranceOptionsDef1,
            OneOfHelloToleranceOptionsDef2,
            InterfaceEthernetOneOfHelloToleranceOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "helloTolerance"})
    last_resort_circuit: Optional[
        Union[
            OneOfLastResortCircuitOptionsDef1,
            OneOfLastResortCircuitOptionsDef2,
            OneOfLastResortCircuitOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "lastResortCircuit"})
    low_bandwidth_link: Optional[
        Union[
            OneOfLowBandwidthLinkOptionsDef1,
            OneOfLowBandwidthLinkOptionsDef2,
            OneOfLowBandwidthLinkOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "lowBandwidthLink"})
    max_control_connections: Optional[
        Union[
            InterfaceEthernetOneOfMaxControlConnectionsOptionsDef1,
            OneOfMaxControlConnectionsOptionsDef2,
            OneOfMaxControlConnectionsOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "maxControlConnections"})
    mode: Optional[Union[InterfaceEthernetOneOfModeOptionsDef1, OneOfModeOptionsDef2]] = _field(
        default=None
    )
    nat_refresh_interval: Optional[
        Union[
            InterfaceEthernetOneOfNatRefreshIntervalOptionsDef1,
            OneOfNatRefreshIntervalOptionsDef2,
            InterfaceEthernetOneOfNatRefreshIntervalOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "natRefreshInterval"})
    network_broadcast: Optional[
        Union[
            OneOfNetworkBroadcastOptionsDef1,
            OneOfNetworkBroadcastOptionsDef2,
            OneOfNetworkBroadcastOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "networkBroadcast"})
    per_tunnel_qos: Optional[
        Union[
            OneOfPerTunnelQosOptionsDef1, OneOfPerTunnelQosOptionsDef2, OneOfPerTunnelQosOptionsDef3
        ]
    ] = _field(default=None, metadata={"alias": "perTunnelQos"})
    port_hop: Optional[
        Union[OneOfPortHopOptionsDef1, OneOfPortHopOptionsDef2, OneOfPortHopOptionsDef3]
    ] = _field(default=None, metadata={"alias": "portHop"})
    restrict: Optional[
        Union[OneOfRestrictOptionsDef1, OneOfRestrictOptionsDef2, OneOfRestrictOptionsDef3]
    ] = _field(default=None)
    set_sdwan_tunnel_mtu_to_max: Optional[
        Union[
            OneOfSetSdwanTunnelMtuToMaxDef1,
            OneOfSetSdwanTunnelMtuToMaxDef2,
            OneOfSetSdwanTunnelMtuToMaxDef3,
        ]
    ] = _field(default=None, metadata={"alias": "setSdwanTunnelMTUToMax"})
    tloc_extension_gre_to: Optional[
        Union[
            InterfaceEthernetOneOfTlocExtensionGreToOptionsDef1,
            OneOfTlocExtensionGreToOptionsDef2,
            OneOfTlocExtensionGreToOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tlocExtensionGreTo"})
    tunnel_tcp_mss: Optional[
        Union[
            InterfaceEthernetOneOfTunnelTcpMssAdjustOptionsDef1,
            OneOfTunnelTcpMssAdjustOptionsDef2,
            OneOfTunnelTcpMssAdjustOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tunnelTcpMss"})
    v_bond_as_stun_server: Optional[
        Union[
            OneOfVbondAsStunServerOptionsDef1,
            OneOfVbondAsStunServerOptionsDef2,
            OneOfVbondAsStunServerOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "vBondAsStunServer"})
    v_manage_connection_preference: Optional[
        Union[
            InterfaceEthernetOneOfVmanageConnectionPreferenceOptionsDef1,
            OneOfVmanageConnectionPreferenceOptionsDef2,
            InterfaceEthernetOneOfVmanageConnectionPreferenceOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "vManageConnectionPreference"})


@dataclass
class InterfaceEthernetAllowService:
    """
    Tunnel Interface Attributes
    """

    all: Optional[
        Union[OneOfAllowAllOptionsDef1, OneOfAllowAllOptionsDef2, OneOfAllowAllOptionsDef3]
    ] = _field(default=None)
    bfd: Optional[
        Union[
            OneOfAllowServiceFalseOptionsDef1,
            OneOfAllowServiceFalseOptionsDef2,
            OneOfAllowServiceFalseOptionsDef3,
        ]
    ] = _field(default=None)
    bgp: Optional[
        Union[OneOfAllowBgpOptionsDef1, OneOfAllowBgpOptionsDef2, OneOfAllowBgpOptionsDef3]
    ] = _field(default=None)
    dhcp: Optional[
        Union[OneOfAllowDhcpOptionsDef1, OneOfAllowDhcpOptionsDef2, OneOfAllowDhcpOptionsDef3]
    ] = _field(default=None)
    dns: Optional[
        Union[
            OneOfAllowServiceTrueOptionsDef1,
            OneOfAllowServiceTrueOptionsDef2,
            OneOfAllowServiceTrueOptionsDef3,
        ]
    ] = _field(default=None)
    https: Optional[
        Union[
            OneOfAllowServiceTrueOptionsDef1,
            OneOfAllowServiceTrueOptionsDef2,
            OneOfAllowServiceTrueOptionsDef3,
        ]
    ] = _field(default=None)
    icmp: Optional[
        Union[
            OneOfAllowServiceTrueOptionsDef1,
            OneOfAllowServiceTrueOptionsDef2,
            OneOfAllowServiceTrueOptionsDef3,
        ]
    ] = _field(default=None)
    netconf: Optional[
        Union[
            OneOfAllowServiceFalseOptionsDef1,
            OneOfAllowServiceFalseOptionsDef2,
            OneOfAllowServiceFalseOptionsDef3,
        ]
    ] = _field(default=None)
    ntp: Optional[
        Union[OneOfAllowNtpOptionsDef1, OneOfAllowNtpOptionsDef2, OneOfAllowNtpOptionsDef3]
    ] = _field(default=None)
    ospf: Optional[
        Union[
            OneOfAllowServiceFalseOptionsDef1,
            OneOfAllowServiceFalseOptionsDef2,
            OneOfAllowServiceFalseOptionsDef3,
        ]
    ] = _field(default=None)
    snmp: Optional[
        Union[
            OneOfAllowServiceFalseOptionsDef1,
            OneOfAllowServiceFalseOptionsDef2,
            OneOfAllowServiceFalseOptionsDef3,
        ]
    ] = _field(default=None)
    ssh: Optional[
        Union[OneOfAllowSshOptionsDef1, OneOfAllowSshOptionsDef2, OneOfAllowSshOptionsDef3]
    ] = _field(default=None)
    stun: Optional[
        Union[
            OneOfAllowServiceFalseOptionsDef1,
            OneOfAllowServiceFalseOptionsDef2,
            OneOfAllowServiceFalseOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class InterfaceEthernetOneOfEncapsulationEncapOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceEthernetEncapsulationEncapDef  # pytype: disable=annotation-type-mismatch


@dataclass
class InterfaceEthernetOneOfEncapsulationPreferenceOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceEthernetOneOfEncapsulationWeightOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceEthernetOneOfEncapsulationWeightOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceEthernetEncapsulation:
    encap: InterfaceEthernetOneOfEncapsulationEncapOptionsDef
    preference: Optional[
        Union[
            InterfaceEthernetOneOfEncapsulationPreferenceOptionsDef1,
            OneOfEncapsulationPreferenceOptionsDef2,
            OneOfEncapsulationPreferenceOptionsDef3,
        ]
    ] = _field(default=None)
    weight: Optional[
        Union[
            InterfaceEthernetOneOfEncapsulationWeightOptionsDef1,
            OneOfEncapsulationWeightOptionsDef2,
            InterfaceEthernetOneOfEncapsulationWeightOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class InterfaceEthernetOneOfCoreRegionDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceEthernetCoreRegionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class InterfaceEthernetOneOfCoreRegionDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceEthernetDefaultCoreRegionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class InterfaceEthernetOneOfSecondaryRegionDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceEthernetSecondaryRegionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class InterfaceEthernetOneOfSecondaryRegionDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceEthernetDefaultSecondaryRegionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class InterfaceEthernetMultiRegionFabric:
    """
    Multi-Region Fabric
    """

    core_region: Optional[
        Union[InterfaceEthernetOneOfCoreRegionDef1, InterfaceEthernetOneOfCoreRegionDef2]
    ] = _field(default=None, metadata={"alias": "coreRegion"})
    enable_core_region: Optional[Union[OneOfEnableRegionDef1, OneOfEnableRegionDef2]] = _field(
        default=None, metadata={"alias": "enableCoreRegion"}
    )
    enable_secondary_region: Optional[Union[OneOfEnableRegionDef1, OneOfEnableRegionDef2]] = _field(
        default=None, metadata={"alias": "enableSecondaryRegion"}
    )
    secondary_region: Optional[
        Union[InterfaceEthernetOneOfSecondaryRegionDef1, InterfaceEthernetOneOfSecondaryRegionDef2]
    ] = _field(default=None, metadata={"alias": "secondaryRegion"})


@dataclass
class InterfaceEthernetOneOfNatTypeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceEthernetNatChoiceDef


@dataclass
class InterfaceEthernetOneOfNatTypeOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceEthernetDefaultNatChoiceDef  # pytype: disable=annotation-type-mismatch


@dataclass
class VpnInterfaceEthernetOneOfNatPoolRangeStartOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VpnInterfaceEthernetOneOfNatPoolRangeEndOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VpnInterfaceEthernetOneOfNatPoolPrefixLengthOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceEthernetNatPool:
    """
    NAT Pool
    """

    prefix_length: Union[
        OneOfNatPoolPrefixLengthOptionsDef1, VpnInterfaceEthernetOneOfNatPoolPrefixLengthOptionsDef2
    ] = _field(metadata={"alias": "prefixLength"})
    range_end: Union[
        OneOfNatPoolRangeEndOptionsDef1, VpnInterfaceEthernetOneOfNatPoolRangeEndOptionsDef2
    ] = _field(metadata={"alias": "rangeEnd"})
    range_start: Union[
        OneOfNatPoolRangeStartOptionsDef1, VpnInterfaceEthernetOneOfNatPoolRangeStartOptionsDef2
    ] = _field(metadata={"alias": "rangeStart"})
    overload: Optional[
        Union[
            OneOfNatPoolOverloadOptionsDef1,
            OneOfNatPoolOverloadOptionsDef2,
            OneOfNatPoolOverloadOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class InterfaceEthernetOneOfNatPoolNameOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class WanVpnInterfaceEthernetOneOfNatPoolRangeStartOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class WanVpnInterfaceEthernetOneOfNatPoolRangeEndOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class WanVpnInterfaceEthernetOneOfNatPoolPrefixLengthOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceEthernetMultiplePool:
    name: Union[OneOfNatPoolNameOptionsDef1, InterfaceEthernetOneOfNatPoolNameOptionsDef2]
    overload: Union[
        OneOfNatPoolOverloadOptionsDef1,
        OneOfNatPoolOverloadOptionsDef2,
        OneOfNatPoolOverloadOptionsDef3,
    ]
    prefix_length: Union[
        OneOfNatPoolPrefixLengthOptionsDef1,
        WanVpnInterfaceEthernetOneOfNatPoolPrefixLengthOptionsDef2,
    ] = _field(metadata={"alias": "prefixLength"})
    range_end: Union[
        OneOfNatPoolRangeEndOptionsDef1, WanVpnInterfaceEthernetOneOfNatPoolRangeEndOptionsDef2
    ] = _field(metadata={"alias": "rangeEnd"})
    range_start: Union[
        OneOfNatPoolRangeStartOptionsDef1, WanVpnInterfaceEthernetOneOfNatPoolRangeStartOptionsDef2
    ] = _field(metadata={"alias": "rangeStart"})
    enable_dual_router_ha_mapping: Optional[
        Union[
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef1,
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "enableDualRouterHAMapping"})


@dataclass
class InterfaceEthernetMultipleLoopback:
    loopback_interface: Union[
        OneOfLoopbackInterfaceOptionsDef1,
        OneOfLoopbackInterfaceOptionsDef2,
        OneOfLoopbackInterfaceOptionsDef3,
    ] = _field(metadata={"alias": "loopbackInterface"})


@dataclass
class InterfaceEthernetOneOfUdpTimeoutOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceEthernetOneOfUdpTimeoutOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceEthernetOneOfTcpTimeoutOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceEthernetOneOfTcpTimeoutOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VpnInterfaceEthernetOneOfStaticSourceIpOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VpnInterfaceEthernetOneOfStaticTranslateIpOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VpnInterfaceEthernetOneOfStaticNatDirectionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: VpnInterfaceEthernetStaticNatDirectionDef


@dataclass
class VpnInterfaceEthernetOneOfStaticNatDirectionOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: (
        VpnInterfaceEthernetDefaultStaticNatDirectionDef  # pytype: disable=annotation-type-mismatch
    )


@dataclass
class VpnInterfaceEthernetOneOfStaticSourceVpnOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VpnInterfaceEthernetOneOfStaticSourceVpnOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceEthernetNewStaticNat:
    source_ip: Union[
        VpnInterfaceEthernetOneOfStaticSourceIpOptionsDef1, OneOfStaticSourceIpOptionsDef2
    ] = _field(metadata={"alias": "sourceIp"})
    source_vpn: Union[
        VpnInterfaceEthernetOneOfStaticSourceVpnOptionsDef1,
        OneOfStaticSourceVpnOptionsDef2,
        VpnInterfaceEthernetOneOfStaticSourceVpnOptionsDef3,
    ] = _field(metadata={"alias": "sourceVpn"})
    static_nat_direction: Union[
        VpnInterfaceEthernetOneOfStaticNatDirectionOptionsDef1,
        VpnInterfaceEthernetOneOfStaticNatDirectionOptionsDef2,
    ] = _field(metadata={"alias": "staticNatDirection"})
    translate_ip: Union[
        VpnInterfaceEthernetOneOfStaticTranslateIpOptionsDef1, OneOfStaticTranslateIpOptionsDef2
    ] = _field(metadata={"alias": "translateIp"})
    enable_dual_router_ha_mapping: Optional[
        Union[
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef1,
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "enableDualRouterHAMapping"})


@dataclass
class InterfaceEthernetOneOfStaticPortForwardProtocolOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceEthernetStaticPortForwardProtocolDef  # pytype: disable=annotation-type-mismatch


@dataclass
class WanVpnInterfaceEthernetOneOfStaticSourceIpOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class InterfaceEthernetOneOfStaticSourcePortOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class WanVpnInterfaceEthernetOneOfStaticTranslateIpOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class InterfaceEthernetOneOfStaticTranslatePortOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class WanVpnInterfaceEthernetOneOfStaticNatDirectionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: WanVpnInterfaceEthernetStaticNatDirectionDef


@dataclass
class WanVpnInterfaceEthernetOneOfStaticNatDirectionOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: WanVpnInterfaceEthernetDefaultStaticNatDirectionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class WanVpnInterfaceEthernetOneOfStaticSourceVpnOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class WanVpnInterfaceEthernetOneOfStaticSourceVpnOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceEthernetStaticPortForward:
    protocol: Union[
        InterfaceEthernetOneOfStaticPortForwardProtocolOptionsDef1,
        OneOfStaticPortForwardProtocolOptionsDef2,
    ]
    source_ip: Union[
        WanVpnInterfaceEthernetOneOfStaticSourceIpOptionsDef1, OneOfStaticSourceIpOptionsDef2
    ] = _field(metadata={"alias": "sourceIp"})
    source_port: Union[
        InterfaceEthernetOneOfStaticSourcePortOptionsDef1, OneOfStaticSourcePortOptionsDef2
    ] = _field(metadata={"alias": "sourcePort"})
    source_vpn: Union[
        WanVpnInterfaceEthernetOneOfStaticSourceVpnOptionsDef1,
        OneOfStaticSourceVpnOptionsDef2,
        WanVpnInterfaceEthernetOneOfStaticSourceVpnOptionsDef3,
    ] = _field(metadata={"alias": "sourceVpn"})
    static_nat_direction: Union[
        WanVpnInterfaceEthernetOneOfStaticNatDirectionOptionsDef1,
        WanVpnInterfaceEthernetOneOfStaticNatDirectionOptionsDef2,
    ] = _field(metadata={"alias": "staticNatDirection"})
    translate_ip: Union[
        WanVpnInterfaceEthernetOneOfStaticTranslateIpOptionsDef1, OneOfStaticTranslateIpOptionsDef2
    ] = _field(metadata={"alias": "translateIp"})
    translate_port: Union[
        InterfaceEthernetOneOfStaticTranslatePortOptionsDef1, OneOfStaticTranslatePortOptionsDef2
    ] = _field(metadata={"alias": "translatePort"})
    enable_dual_router_ha_mapping: Optional[
        Union[
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef1,
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "enableDualRouterHAMapping"})


@dataclass
class InterfaceEthernetNatAttributesIpv4:
    """
    NAT Attributes IpV4
    """

    nat_type: Union[
        InterfaceEthernetOneOfNatTypeOptionsDef1, InterfaceEthernetOneOfNatTypeOptionsDef2
    ] = _field(metadata={"alias": "natType"})
    tcp_timeout: Union[
        InterfaceEthernetOneOfTcpTimeoutOptionsDef1,
        OneOfTcpTimeoutOptionsDef2,
        InterfaceEthernetOneOfTcpTimeoutOptionsDef3,
    ] = _field(metadata={"alias": "tcpTimeout"})
    udp_timeout: Union[
        InterfaceEthernetOneOfUdpTimeoutOptionsDef1,
        OneOfUdpTimeoutOptionsDef2,
        InterfaceEthernetOneOfUdpTimeoutOptionsDef3,
    ] = _field(metadata={"alias": "udpTimeout"})
    match_interface: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "matchInterface"})
    # NAT Multiple Loopback
    multiple_loopback: Optional[List[InterfaceEthernetMultipleLoopback]] = _field(
        default=None, metadata={"alias": "multipleLoopback"}
    )
    # NAT Multiple Pool
    multiple_pool: Optional[List[InterfaceEthernetMultiplePool]] = _field(
        default=None, metadata={"alias": "multiplePool"}
    )
    nat_loopback: Optional[
        Union[
            OneOfLoopbackInterfaceOptionsDef1,
            OneOfLoopbackInterfaceOptionsDef2,
            OneOfLoopbackInterfaceOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "natLoopback"})
    # NAT Pool
    nat_pool: Optional[InterfaceEthernetNatPool] = _field(
        default=None, metadata={"alias": "natPool"}
    )
    # static NAT
    new_static_nat: Optional[List[InterfaceEthernetNewStaticNat]] = _field(
        default=None, metadata={"alias": "newStaticNat"}
    )
    # Configure Port Forward entries
    static_port_forward: Optional[List[InterfaceEthernetStaticPortForward]] = _field(
        default=None, metadata={"alias": "staticPortForward"}
    )


@dataclass
class InterfaceEthernetOneOfStaticNat66TranslatedSourcePrefixOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class InterfaceEthernetOneOfStaticNat66SourceVpnIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceEthernetStaticNat66:
    source_prefix: Union[
        OneOfStaticNat66SourcePrefixOptionsDef1, OneOfStaticNat66SourcePrefixOptionsDef2
    ] = _field(metadata={"alias": "sourcePrefix"})
    source_vpn_id: Union[
        InterfaceEthernetOneOfStaticNat66SourceVpnIdOptionsDef1,
        OneOfStaticNat66SourceVpnIdOptionsDef2,
        OneOfStaticNat66SourceVpnIdOptionsDef3,
    ] = _field(metadata={"alias": "sourceVpnId"})
    egress_interface: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "egressInterface"})
    translated_source_prefix: Optional[
        Union[
            InterfaceEthernetOneOfStaticNat66TranslatedSourcePrefixOptionsDef1,
            OneOfStaticNat66TranslatedSourcePrefixOptionsDef2,
            OneOfStaticNat66TranslatedSourcePrefixOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "translatedSourcePrefix"})


@dataclass
class InterfaceEthernetNatAttributesIpv6:
    """
    NAT Attributes Ipv6
    """

    nat64: Optional[Union[OneOfNat64Nat66OptionsDef1, OneOfNat64Nat66OptionsDef2]] = _field(
        default=None
    )
    nat66: Optional[Union[OneOfNat64Nat66OptionsDef1, OneOfNat64Nat66OptionsDef2]] = _field(
        default=None
    )
    # static NAT66
    static_nat66: Optional[List[InterfaceEthernetStaticNat66]] = _field(
        default=None, metadata={"alias": "staticNat66"}
    )


@dataclass
class VpnInterfaceEthernetOneOfPeriodOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VpnInterfaceEthernetOneOfPeriodOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfShapingRateUpOrDownstreamOptionsDef15:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfShapingRateUpOrDownstreamOptionsDef16:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfShapingRateUpOrDownstreamOptionsDef17:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VpnInterfaceEthernetShapingRateUpstreamConfig:
    """
    adaptiveQoS Shaping Rate Upstream config
    """

    default_shaping_rate_upstream: Union[
        OneOfShapingRateUpOrDownstreamOptionsDef17, OneOfShapingRateUpOrDownstreamOptionsDef2
    ] = _field(metadata={"alias": "defaultShapingRateUpstream"})
    max_shaping_rate_upstream: Union[
        OneOfShapingRateUpOrDownstreamOptionsDef16, OneOfShapingRateUpOrDownstreamOptionsDef2
    ] = _field(metadata={"alias": "maxShapingRateUpstream"})
    min_shaping_rate_upstream: Union[
        OneOfShapingRateUpOrDownstreamOptionsDef15, OneOfShapingRateUpOrDownstreamOptionsDef2
    ] = _field(metadata={"alias": "minShapingRateUpstream"})


@dataclass
class OneOfShapingRateUpOrDownstreamOptionsDef18:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfShapingRateUpOrDownstreamOptionsDef19:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfShapingRateUpOrDownstreamOptionsDef110:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VpnInterfaceEthernetShapingRateDownstreamConfig:
    """
    adaptiveQoS Shaping Rate Downstream config
    """

    default_shaping_rate_downstream: Union[
        OneOfShapingRateUpOrDownstreamOptionsDef110, OneOfShapingRateUpOrDownstreamOptionsDef2
    ] = _field(metadata={"alias": "defaultShapingRateDownstream"})
    max_shaping_rate_downstream: Union[
        OneOfShapingRateUpOrDownstreamOptionsDef19, OneOfShapingRateUpOrDownstreamOptionsDef2
    ] = _field(metadata={"alias": "maxShapingRateDownstream"})
    min_shaping_rate_downstream: Union[
        OneOfShapingRateUpOrDownstreamOptionsDef18, OneOfShapingRateUpOrDownstreamOptionsDef2
    ] = _field(metadata={"alias": "minShapingRateDownstream"})


@dataclass
class InterfaceEthernetAclQos1:
    adaptive_qo_s: Union[OneOfQosAdaptiveOptionsDef1, OneOfQosAdaptiveOptionsDef2] = _field(
        metadata={"alias": "adaptiveQoS"}
    )
    shaping_rate_upstream: ShapingRateUpstream = _field(metadata={"alias": "shapingRateUpstream"})
    # adaptiveQoS Shaping Rate Upstream config
    shaping_rate_upstream_config: VpnInterfaceEthernetShapingRateUpstreamConfig = _field(
        metadata={"alias": "shapingRateUpstreamConfig"}
    )
    adapt_period: Optional[
        Union[
            VpnInterfaceEthernetOneOfPeriodOptionsDef1,
            OneOfPeriodOptionsDef2,
            VpnInterfaceEthernetOneOfPeriodOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "adaptPeriod"})
    ipv4_acl_egress: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "ipv4AclEgress"}
    )
    ipv4_acl_ingress: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "ipv4AclIngress"}
    )
    ipv6_acl_egress: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "ipv6AclEgress"}
    )
    ipv6_acl_ingress: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "ipv6AclIngress"}
    )
    shaping_rate: Optional[
        Union[OneOfShapingRateOptionsDef1, OneOfShapingRateOptionsDef2, OneOfShapingRateOptionsDef3]
    ] = _field(default=None, metadata={"alias": "shapingRate"})
    shaping_rate_downstream: Optional[
        Union[OneOfShapingRateDownstreamOptionsDef1, OneOfShapingRateDownstreamOptionsDef2]
    ] = _field(default=None, metadata={"alias": "shapingRateDownstream"})
    # adaptiveQoS Shaping Rate Downstream config
    shaping_rate_downstream_config: Optional[VpnInterfaceEthernetShapingRateDownstreamConfig] = (
        _field(default=None, metadata={"alias": "shapingRateDownstreamConfig"})
    )


@dataclass
class WanVpnInterfaceEthernetOneOfPeriodOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class WanVpnInterfaceEthernetOneOfPeriodOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfShapingRateUpOrDownstreamOptionsDef111:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfShapingRateUpOrDownstreamOptionsDef112:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfShapingRateUpOrDownstreamOptionsDef113:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class WanVpnInterfaceEthernetShapingRateUpstreamConfig:
    """
    adaptiveQoS Shaping Rate Upstream config
    """

    default_shaping_rate_upstream: Union[
        OneOfShapingRateUpOrDownstreamOptionsDef113, OneOfShapingRateUpOrDownstreamOptionsDef2
    ] = _field(metadata={"alias": "defaultShapingRateUpstream"})
    max_shaping_rate_upstream: Union[
        OneOfShapingRateUpOrDownstreamOptionsDef112, OneOfShapingRateUpOrDownstreamOptionsDef2
    ] = _field(metadata={"alias": "maxShapingRateUpstream"})
    min_shaping_rate_upstream: Union[
        OneOfShapingRateUpOrDownstreamOptionsDef111, OneOfShapingRateUpOrDownstreamOptionsDef2
    ] = _field(metadata={"alias": "minShapingRateUpstream"})


@dataclass
class OneOfShapingRateUpOrDownstreamOptionsDef114:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfShapingRateUpOrDownstreamOptionsDef115:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfShapingRateUpOrDownstreamOptionsDef116:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class WanVpnInterfaceEthernetShapingRateDownstreamConfig:
    """
    adaptiveQoS Shaping Rate Downstream config
    """

    default_shaping_rate_downstream: Union[
        OneOfShapingRateUpOrDownstreamOptionsDef116, OneOfShapingRateUpOrDownstreamOptionsDef2
    ] = _field(metadata={"alias": "defaultShapingRateDownstream"})
    max_shaping_rate_downstream: Union[
        OneOfShapingRateUpOrDownstreamOptionsDef115, OneOfShapingRateUpOrDownstreamOptionsDef2
    ] = _field(metadata={"alias": "maxShapingRateDownstream"})
    min_shaping_rate_downstream: Union[
        OneOfShapingRateUpOrDownstreamOptionsDef114, OneOfShapingRateUpOrDownstreamOptionsDef2
    ] = _field(metadata={"alias": "minShapingRateDownstream"})


@dataclass
class InterfaceEthernetAclQos2:
    adaptive_qo_s: Union[OneOfQosAdaptiveOptionsDef1, OneOfQosAdaptiveOptionsDef2] = _field(
        metadata={"alias": "adaptiveQoS"}
    )
    adapt_period: Optional[
        Union[
            WanVpnInterfaceEthernetOneOfPeriodOptionsDef1,
            OneOfPeriodOptionsDef2,
            WanVpnInterfaceEthernetOneOfPeriodOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "adaptPeriod"})
    ipv4_acl_egress: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "ipv4AclEgress"}
    )
    ipv4_acl_ingress: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "ipv4AclIngress"}
    )
    ipv6_acl_egress: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "ipv6AclEgress"}
    )
    ipv6_acl_ingress: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "ipv6AclIngress"}
    )
    shaping_rate: Optional[
        Union[OneOfShapingRateOptionsDef1, OneOfShapingRateOptionsDef2, OneOfShapingRateOptionsDef3]
    ] = _field(default=None, metadata={"alias": "shapingRate"})
    shaping_rate_downstream: Optional[
        Union[OneOfShapingRateDownstreamOptionsDef1, OneOfShapingRateDownstreamOptionsDef2]
    ] = _field(default=None, metadata={"alias": "shapingRateDownstream"})
    # adaptiveQoS Shaping Rate Downstream config
    shaping_rate_downstream_config: Optional[WanVpnInterfaceEthernetShapingRateDownstreamConfig] = (
        _field(default=None, metadata={"alias": "shapingRateDownstreamConfig"})
    )
    shaping_rate_upstream: Optional[
        Union[OneOfShapingRateUpstreamOptionsDef1, OneOfShapingRateUpstreamOptionsDef2]
    ] = _field(default=None, metadata={"alias": "shapingRateUpstream"})
    # adaptiveQoS Shaping Rate Upstream config
    shaping_rate_upstream_config: Optional[WanVpnInterfaceEthernetShapingRateUpstreamConfig] = (
        _field(default=None, metadata={"alias": "shapingRateUpstreamConfig"})
    )


@dataclass
class WanVpnInterfaceEthernetOneOfIpV4AddressOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class InterfaceEthernetArp:
    ip_address: Union[
        OneOfIpV4AddressOptionsDef1,
        WanVpnInterfaceEthernetOneOfIpV4AddressOptionsDef2,
        OneOfIpV4AddressOptionsDef3,
    ] = _field(metadata={"alias": "ipAddress"})
    mac_address: Union[
        OneOfMacAddressOptionsDef1, OneOfMacAddressOptionsDef2, OneOfMacAddressOptionsDef3
    ] = _field(metadata={"alias": "macAddress"})


@dataclass
class InterfaceEthernetOneOfDuplexOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceEthernetDuplexDef  # pytype: disable=annotation-type-mismatch


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
class InterfaceEthernetOneOfIntrfMtuOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
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
class InterfaceEthernetOneOfTlocExtensionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class InterfaceEthernetOneOfTlocExtensionGreFromOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class InterfaceEthernetOneOfXconnectOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class InterfaceEthernetTlocExtensionGreFrom:
    """
    Extend remote TLOC over a GRE tunnel to a local WAN interface
    """

    source_ip: Optional[
        Union[
            InterfaceEthernetOneOfTlocExtensionGreFromOptionsDef1,
            OneOfTlocExtensionGreFromOptionsDef2,
            OneOfTlocExtensionGreFromOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sourceIp"})
    xconnect: Optional[
        Union[
            InterfaceEthernetOneOfXconnectOptionsDef1,
            OneOfXconnectOptionsDef2,
            OneOfXconnectOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class InterfaceEthernetOneOfLoadIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfaceEthernetOneOfTrackerOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class InterfaceEthernetAdvanced:
    """
    Advanced Attributes
    """

    arp_timeout: Optional[
        Union[
            InterfaceEthernetOneOfArpTimeoutOptionsDef1,
            OneOfArpTimeoutOptionsDef2,
            InterfaceEthernetOneOfArpTimeoutOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "arpTimeout"})
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
            OneOfOnBooleanDefaultTrueOptionsDef1,
            OneOfOnBooleanDefaultTrueOptionsDef2,
            OneOfOnBooleanDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "icmpRedirectDisable"})
    intrf_mtu: Optional[
        Union[
            InterfaceEthernetOneOfIntrfMtuOptionsDef1,
            OneOfIntrfMtuOptionsDef2,
            InterfaceEthernetOneOfIntrfMtuOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "intrfMtu"})
    ip_directed_broadcast: Optional[
        Union[
            OneOfIpDirectedBroadcastOptionsDef1,
            OneOfIpDirectedBroadcastOptionsDef2,
            OneOfIpDirectedBroadcastOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ipDirectedBroadcast"})
    ip_mtu: Optional[
        Union[
            InterfaceEthernetOneOfMtuOptionsDef1,
            OneOfMtuOptionsDef2,
            InterfaceEthernetOneOfMtuOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ipMtu"})
    load_interval: Optional[
        Union[
            InterfaceEthernetOneOfLoadIntervalOptionsDef1,
            OneOfLoadIntervalOptionsDef2,
            OneOfLoadIntervalOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "loadInterval"})
    mac_address: Optional[
        Union[OneOfMacAddressOptionsDef1, OneOfMacAddressOptionsDef2, OneOfMacAddressOptionsDef3]
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
    tloc_extension: Optional[
        Union[
            InterfaceEthernetOneOfTlocExtensionOptionsDef1,
            OneOfTlocExtensionOptionsDef2,
            OneOfTlocExtensionOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tlocExtension"})
    # Extend remote TLOC over a GRE tunnel to a local WAN interface
    tloc_extension_gre_from: Optional[InterfaceEthernetTlocExtensionGreFrom] = _field(
        default=None, metadata={"alias": "tlocExtensionGreFrom"}
    )
    tracker: Optional[
        Union[
            InterfaceEthernetOneOfTrackerOptionsDef1,
            OneOfTrackerOptionsDef2,
            OneOfTrackerOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class WanVpnInterfaceEthernetData:
    description: Union[
        OneOfDescriptionOptionsDef1, OneOfDescriptionOptionsDef2, OneOfDescriptionOptionsDef3
    ]
    interface_name: Union[OneOfInterfaceNameOptionsDef1, OneOfInterfaceNameOptionsDef2] = _field(
        metadata={"alias": "interfaceName"}
    )
    shutdown: Union[OneOfShutdownOptionsDef1, OneOfShutdownOptionsDef2, OneOfShutdownOptionsDef3]
    tunnel_interface: Union[OneOfTunnelInterfaceOptionsDef1, OneOfTunnelInterfaceOptionsDef2] = (
        _field(metadata={"alias": "tunnelInterface"})
    )
    # ACL/QOS
    acl_qos: Optional[Union[InterfaceEthernetAclQos1, InterfaceEthernetAclQos2]] = _field(
        default=None, metadata={"alias": "aclQos"}
    )
    # Advanced Attributes
    advanced: Optional[InterfaceEthernetAdvanced] = _field(default=None)
    # Tunnel Interface Attributes
    allow_service: Optional[InterfaceEthernetAllowService] = _field(
        default=None, metadata={"alias": "allowService"}
    )
    # Configure ARP entries
    arp: Optional[List[InterfaceEthernetArp]] = _field(default=None)
    auto_detect_bandwidth: Optional[
        Union[
            OneOfAutoBandwidthDetectOptionsDef1,
            OneOfAutoBandwidthDetectOptionsDef2,
            OneOfAutoBandwidthDetectOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "autoDetectBandwidth"})
    bandwidth_downstream: Optional[
        Union[
            InterfaceEthernetOneOfBandwidthDownstreamOptionsDef1,
            OneOfBandwidthDownstreamOptionsDef2,
            OneOfBandwidthDownstreamOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "bandwidthDownstream"})
    bandwidth_upstream: Optional[
        Union[
            InterfaceEthernetOneOfBandwidthUpstreamOptionsDef1,
            OneOfBandwidthUpstreamOptionsDef2,
            OneOfBandwidthUpstreamOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "bandwidthUpstream"})
    block_non_source_ip: Optional[
        Union[
            OneOfBlockNonSourceIpOptionsDef1,
            OneOfBlockNonSourceIpOptionsDef2,
            OneOfBlockNonSourceIpOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "blockNonSourceIp"})
    dhcp_helper: Optional[
        Union[
            OneOfListOfIpV4OptionsDef1,
            InterfaceEthernetOneOfListOfIpV4OptionsDef2,
            OneOfListOfIpV4OptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "dhcpHelper"})
    enable_ha_interlink_interface: Optional[
        Union[
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef1,
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "enableHAInterlinkInterface"})
    # Encapsulation for TLOC
    encapsulation: Optional[List[InterfaceEthernetEncapsulation]] = _field(default=None)
    intf_ip_address: Optional[
        Union[InterfaceEthernetIntfIpAddress1, InterfaceEthernetIntfIpAddress2]
    ] = _field(default=None, metadata={"alias": "intfIpAddress"})
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
    # Multi-Region Fabric
    multi_region_fabric: Optional[InterfaceEthernetMultiRegionFabric] = _field(
        default=None, metadata={"alias": "multiRegionFabric"}
    )
    nat: Optional[Union[OneOfNatOptionsDef1, OneOfNatOptionsDef2, OneOfNatOptionsDef3]] = _field(
        default=None
    )
    # NAT Attributes IpV4
    nat_attributes_ipv4: Optional[InterfaceEthernetNatAttributesIpv4] = _field(
        default=None, metadata={"alias": "natAttributesIpv4"}
    )
    # NAT Attributes Ipv6
    nat_attributes_ipv6: Optional[InterfaceEthernetNatAttributesIpv6] = _field(
        default=None, metadata={"alias": "natAttributesIpv6"}
    )
    nat_ipv6: Optional[Union[OneOfNatOptionsDef1, OneOfNatOptionsDef2, OneOfNatOptionsDef3]] = (
        _field(default=None, metadata={"alias": "natIpv6"})
    )
    port_channel: Optional[Union[InterfaceEthernetPortChannel1, PortChannel2]] = _field(
        default=None, metadata={"alias": "portChannel"}
    )
    port_channel_interface: Optional[
        Union[OneOfPortChannelOptionsDef1, OneOfPortChannelOptionsDef2]
    ] = _field(default=None, metadata={"alias": "portChannelInterface"})
    port_channel_member_interface: Optional[
        Union[OneOfPortChannelMemberOptionsDef1, OneOfPortChannelMemberOptionsDef2]
    ] = _field(default=None, metadata={"alias": "portChannelMemberInterface"})
    service_provider: Optional[
        Union[
            OneOfServiceProviderOptionsDef1,
            OneOfServiceProviderOptionsDef2,
            OneOfServiceProviderOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "serviceProvider"})
    # Tunnel Interface Attributes
    tunnel: Optional[InterfaceEthernetTunnel] = _field(default=None)


@dataclass
class EditWanVpnInterfaceEthernetParcelForTransportPutRequest:
    """
    WAN VPN Interface Ethernet profile parcel schema for PUT request
    """

    data: WanVpnInterfaceEthernetData
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
