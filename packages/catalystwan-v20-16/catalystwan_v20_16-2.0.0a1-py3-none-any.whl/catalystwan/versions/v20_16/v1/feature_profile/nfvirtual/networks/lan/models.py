# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

VariableOptionTypeDef = Literal["variable"]

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

ModeDef = Literal["access", "trunk"]

DefaultOptionTypeDef = Literal["default"]

DefaultModeDef = Literal["trunk"]

LanModeDef = Literal["access", "trunk"]

LanDefaultModeDef = Literal["trunk"]

NetworksLanModeDef = Literal["access", "trunk"]

NetworksLanDefaultModeDef = Literal["trunk"]


@dataclass
class CreateNfvirtualLanParcelPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class OneOfPortOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfPortOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpAddressOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfIpAddressOptionsDef2:
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
    value: ModeDef


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
    interface_name: Optional[Union[OneOfPortOptionsDef1, OneOfPortOptionsDef2]] = _field(
        default=None
    )
    ip_address: Optional[Union[OneOfIpAddressOptionsDef1, OneOfIpAddressOptionsDef2]] = _field(
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
    vlan: Optional[Union[OneOfVlanOptionsDef1, OneOfVlanOptionsDef2]] = _field(default=None)


@dataclass
class CreateNfvirtualLanParcelPostRequest:
    """
    LAN profile parcel schema for POST request
    """

    data: Data
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class LanOneOfPortOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class LanOneOfIpAddressOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class LanOneOfNetworkNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class LanOneOfBridgeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class LanOneOfModeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: LanModeDef


@dataclass
class LanOneOfModeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Optional[LanDefaultModeDef] = _field(default=None)


@dataclass
class LanOneOfVlanOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class LanOneOfNativeVlanOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class LanData:
    bridge: Optional[Union[LanOneOfBridgeOptionsDef1, OneOfBridgeOptionsDef2]] = _field(
        default=None
    )
    interface_name: Optional[Union[LanOneOfPortOptionsDef1, OneOfPortOptionsDef2]] = _field(
        default=None
    )
    ip_address: Optional[Union[LanOneOfIpAddressOptionsDef1, OneOfIpAddressOptionsDef2]] = _field(
        default=None
    )
    mode: Optional[
        Union[LanOneOfModeOptionsDef1, OneOfModeOptionsDef2, LanOneOfModeOptionsDef3]
    ] = _field(default=None)
    native_vlan: Optional[Union[LanOneOfNativeVlanOptionsDef1, OneOfNativeVlanOptionsDef2]] = (
        _field(default=None)
    )
    netmask: Optional[Union[OneOfNetmaskOptionsDef1, OneOfNetmaskOptionsDef2]] = _field(
        default=None
    )
    network_name: Optional[Union[LanOneOfNetworkNameOptionsDef1, OneOfNetworkNameOptionsDef2]] = (
        _field(default=None)
    )
    vlan: Optional[Union[LanOneOfVlanOptionsDef1, OneOfVlanOptionsDef2]] = _field(default=None)


@dataclass
class Payload:
    """
    LAN profile parcel schema for PUT request
    """

    data: LanData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class GetSingleNfvirtualNetworksLanPayload:
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
    # LAN profile parcel schema for PUT request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class EditNfvirtualLanParcelPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class NetworksLanOneOfPortOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class NetworksLanOneOfIpAddressOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class NetworksLanOneOfNetworkNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class NetworksLanOneOfBridgeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class NetworksLanOneOfModeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: NetworksLanModeDef


@dataclass
class NetworksLanOneOfModeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Optional[NetworksLanDefaultModeDef] = _field(default=None)


@dataclass
class NetworksLanOneOfVlanOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class NetworksLanOneOfNativeVlanOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class NetworksLanData:
    bridge: Optional[Union[NetworksLanOneOfBridgeOptionsDef1, OneOfBridgeOptionsDef2]] = _field(
        default=None
    )
    interface_name: Optional[Union[NetworksLanOneOfPortOptionsDef1, OneOfPortOptionsDef2]] = _field(
        default=None
    )
    ip_address: Optional[Union[NetworksLanOneOfIpAddressOptionsDef1, OneOfIpAddressOptionsDef2]] = (
        _field(default=None)
    )
    mode: Optional[
        Union[
            NetworksLanOneOfModeOptionsDef1, OneOfModeOptionsDef2, NetworksLanOneOfModeOptionsDef3
        ]
    ] = _field(default=None)
    native_vlan: Optional[
        Union[NetworksLanOneOfNativeVlanOptionsDef1, OneOfNativeVlanOptionsDef2]
    ] = _field(default=None)
    netmask: Optional[Union[OneOfNetmaskOptionsDef1, OneOfNetmaskOptionsDef2]] = _field(
        default=None
    )
    network_name: Optional[
        Union[NetworksLanOneOfNetworkNameOptionsDef1, OneOfNetworkNameOptionsDef2]
    ] = _field(default=None)
    vlan: Optional[Union[NetworksLanOneOfVlanOptionsDef1, OneOfVlanOptionsDef2]] = _field(
        default=None
    )


@dataclass
class EditNfvirtualLanParcelPutRequest:
    """
    LAN profile parcel schema for PUT request
    """

    data: NetworksLanData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)
