# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

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

VariableOptionTypeDef = Literal["variable"]

ModeDef = Literal["access", "trunk"]

DefaultOptionTypeDef = Literal["default"]

DefaultModeDef = Literal["trunk"]

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

TypeDef = Literal["none", "primary", "secondary(1)"]

WanColorDef = Literal[
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

WanModeDef = Literal["access", "trunk"]

WanDefaultModeDef = Literal["trunk"]

WanTypeDef = Literal["none", "primary", "secondary(1)"]

NetworksWanColorDef = Literal[
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

NetworksWanModeDef = Literal["access", "trunk"]

NetworksWanDefaultModeDef = Literal["trunk"]

NetworksWanTypeDef = Literal["none", "primary", "secondary(1)"]


@dataclass
class CreateNfvirtualWanParcelPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


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
class OneOfWanInterfaceNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfWanInterfaceNameOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfNetworkNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfNetworkNameOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfBridgeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfBridgeOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


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
class OneOfModeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Optional[DefaultModeDef] = _field(default=None)


@dataclass
class OneOfDhcpOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfDhcpOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Optional[bool] = _field(default=None)


@dataclass
class OneOfIpv4AddressOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfIpv4AddressOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfNetmaskOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Ipv4SubnetMaskDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfNetmaskOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfShutdownOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfShutdownOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Optional[bool] = _field(default=None)


@dataclass
class OneOfDefaultGatewayOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfDefaultGatewayOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTypeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: TypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfVlanOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfVlanOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfNativeVlanOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNativeVlanOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class Data:
    bridge: Optional[Union[OneOfBridgeOptionsDef1, OneOfBridgeOptionsDef2]] = _field(default=None)
    color: Optional[Union[OneOfColorOptionsDef1, OneOfColorOptionsDef2]] = _field(default=None)
    default_gateway: Optional[
        Union[OneOfDefaultGatewayOptionsDef1, OneOfDefaultGatewayOptionsDef2]
    ] = _field(default=None, metadata={"alias": "defaultGateway"})
    dhcp: Optional[Union[OneOfDhcpOptionsDef1, OneOfDhcpOptionsDef2]] = _field(default=None)
    interface_name: Optional[
        Union[OneOfWanInterfaceNameOptionsDef1, OneOfWanInterfaceNameOptionsDef2]
    ] = _field(default=None)
    ip_address: Optional[Union[OneOfIpv4AddressOptionsDef1, OneOfIpv4AddressOptionsDef2]] = _field(
        default=None
    )
    mode: Optional[Union[OneOfModeOptionsDef1, OneOfModeOptionsDef2, OneOfModeOptionsDef3]] = (
        _field(default=None)
    )
    native_vlan: Optional[Union[OneOfNativeVlanOptionsDef1, OneOfNativeVlanOptionsDef2]] = _field(
        default=None
    )
    netmask: Optional[Union[OneOfNetmaskOptionsDef1, OneOfNetmaskOptionsDef2]] = _field(
        default=None
    )
    network_name: Optional[Union[OneOfNetworkNameOptionsDef1, OneOfNetworkNameOptionsDef2]] = (
        _field(default=None)
    )
    shutdown: Optional[Union[OneOfShutdownOptionsDef1, OneOfShutdownOptionsDef2]] = _field(
        default=None
    )
    type_: Optional[OneOfTypeOptionsDef] = _field(default=None, metadata={"alias": "type"})
    vlan: Optional[Union[OneOfVlanOptionsDef1, OneOfVlanOptionsDef2]] = _field(default=None)


@dataclass
class CreateNfvirtualWanParcelPostRequest:
    """
    WAN  profile parcel schema for POST request
    """

    data: Data
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class WanOneOfColorOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: WanColorDef  # pytype: disable=annotation-type-mismatch


@dataclass
class WanOneOfWanInterfaceNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class WanOneOfNetworkNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class WanOneOfBridgeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class WanOneOfModeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: WanModeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class WanOneOfModeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Optional[WanDefaultModeDef] = _field(default=None)


@dataclass
class WanOneOfIpv4AddressOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class WanOneOfDefaultGatewayOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class WanOneOfTypeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: WanTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class WanOneOfVlanOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class WanOneOfNativeVlanOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class WanData:
    bridge: Optional[Union[WanOneOfBridgeOptionsDef1, OneOfBridgeOptionsDef2]] = _field(
        default=None
    )
    color: Optional[Union[WanOneOfColorOptionsDef1, OneOfColorOptionsDef2]] = _field(default=None)
    default_gateway: Optional[
        Union[WanOneOfDefaultGatewayOptionsDef1, OneOfDefaultGatewayOptionsDef2]
    ] = _field(default=None, metadata={"alias": "defaultGateway"})
    dhcp: Optional[Union[OneOfDhcpOptionsDef1, OneOfDhcpOptionsDef2]] = _field(default=None)
    interface_name: Optional[
        Union[WanOneOfWanInterfaceNameOptionsDef1, OneOfWanInterfaceNameOptionsDef2]
    ] = _field(default=None)
    ip_address: Optional[Union[WanOneOfIpv4AddressOptionsDef1, OneOfIpv4AddressOptionsDef2]] = (
        _field(default=None)
    )
    mode: Optional[
        Union[WanOneOfModeOptionsDef1, OneOfModeOptionsDef2, WanOneOfModeOptionsDef3]
    ] = _field(default=None)
    native_vlan: Optional[Union[WanOneOfNativeVlanOptionsDef1, OneOfNativeVlanOptionsDef2]] = (
        _field(default=None)
    )
    netmask: Optional[Union[OneOfNetmaskOptionsDef1, OneOfNetmaskOptionsDef2]] = _field(
        default=None
    )
    network_name: Optional[Union[WanOneOfNetworkNameOptionsDef1, OneOfNetworkNameOptionsDef2]] = (
        _field(default=None)
    )
    shutdown: Optional[Union[OneOfShutdownOptionsDef1, OneOfShutdownOptionsDef2]] = _field(
        default=None
    )
    type_: Optional[WanOneOfTypeOptionsDef] = _field(default=None, metadata={"alias": "type"})
    vlan: Optional[Union[WanOneOfVlanOptionsDef1, OneOfVlanOptionsDef2]] = _field(default=None)


@dataclass
class Payload:
    """
    WAN  profile parcel schema for PUT request
    """

    data: WanData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class GetSingleNfvirtualNetworksWanPayload:
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
    # WAN  profile parcel schema for PUT request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class EditNfvirtualWanParcelPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class NetworksWanOneOfColorOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: NetworksWanColorDef  # pytype: disable=annotation-type-mismatch


@dataclass
class NetworksWanOneOfWanInterfaceNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class NetworksWanOneOfNetworkNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class NetworksWanOneOfBridgeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class NetworksWanOneOfModeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: NetworksWanModeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class NetworksWanOneOfModeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Optional[NetworksWanDefaultModeDef] = _field(default=None)


@dataclass
class NetworksWanOneOfIpv4AddressOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class NetworksWanOneOfDefaultGatewayOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class NetworksWanOneOfTypeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: NetworksWanTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class NetworksWanOneOfVlanOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class NetworksWanOneOfNativeVlanOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class NetworksWanData:
    bridge: Optional[Union[NetworksWanOneOfBridgeOptionsDef1, OneOfBridgeOptionsDef2]] = _field(
        default=None
    )
    color: Optional[Union[NetworksWanOneOfColorOptionsDef1, OneOfColorOptionsDef2]] = _field(
        default=None
    )
    default_gateway: Optional[
        Union[NetworksWanOneOfDefaultGatewayOptionsDef1, OneOfDefaultGatewayOptionsDef2]
    ] = _field(default=None, metadata={"alias": "defaultGateway"})
    dhcp: Optional[Union[OneOfDhcpOptionsDef1, OneOfDhcpOptionsDef2]] = _field(default=None)
    interface_name: Optional[
        Union[NetworksWanOneOfWanInterfaceNameOptionsDef1, OneOfWanInterfaceNameOptionsDef2]
    ] = _field(default=None)
    ip_address: Optional[
        Union[NetworksWanOneOfIpv4AddressOptionsDef1, OneOfIpv4AddressOptionsDef2]
    ] = _field(default=None)
    mode: Optional[
        Union[
            NetworksWanOneOfModeOptionsDef1, OneOfModeOptionsDef2, NetworksWanOneOfModeOptionsDef3
        ]
    ] = _field(default=None)
    native_vlan: Optional[
        Union[NetworksWanOneOfNativeVlanOptionsDef1, OneOfNativeVlanOptionsDef2]
    ] = _field(default=None)
    netmask: Optional[Union[OneOfNetmaskOptionsDef1, OneOfNetmaskOptionsDef2]] = _field(
        default=None
    )
    network_name: Optional[
        Union[NetworksWanOneOfNetworkNameOptionsDef1, OneOfNetworkNameOptionsDef2]
    ] = _field(default=None)
    shutdown: Optional[Union[OneOfShutdownOptionsDef1, OneOfShutdownOptionsDef2]] = _field(
        default=None
    )
    type_: Optional[NetworksWanOneOfTypeOptionsDef] = _field(
        default=None, metadata={"alias": "type"}
    )
    vlan: Optional[Union[NetworksWanOneOfVlanOptionsDef1, OneOfVlanOptionsDef2]] = _field(
        default=None
    )


@dataclass
class EditNfvirtualWanParcelPutRequest:
    """
    WAN  profile parcel schema for PUT request
    """

    data: NetworksWanData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)
