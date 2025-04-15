# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

VariableOptionTypeDef = Literal["variable"]

ModeDef = Literal["access", "trunk"]

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

OvsnetworkModeDef = Literal["access", "trunk"]


@dataclass
class OneOfNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfNameOptionsDef2:
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
class OneOfNativeLanOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfNativeLanOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAddressOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfAddressOptionsDef2:
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
class OneOfDhcpOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfDhcpOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfGatewayOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfGatewayOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class Data:
    network_name: Union[OneOfNameOptionsDef1, OneOfNameOptionsDef2]
    bridge: Optional[Union[OneOfBridgeOptionsDef1, OneOfBridgeOptionsDef2]] = _field(default=None)
    dhcp: Optional[Union[OneOfDhcpOptionsDef1, OneOfDhcpOptionsDef2]] = _field(default=None)
    gateway: Optional[Union[OneOfGatewayOptionsDef1, OneOfGatewayOptionsDef2]] = _field(
        default=None
    )
    interface_name: Optional[
        Union[OneOfInterfaceNameOptionsDef1, OneOfInterfaceNameOptionsDef2]
    ] = _field(default=None)
    ip_address: Optional[Union[OneOfAddressOptionsDef1, OneOfAddressOptionsDef2]] = _field(
        default=None
    )
    mode: Optional[Union[OneOfModeOptionsDef1, OneOfModeOptionsDef2]] = _field(default=None)
    native_vlan: Optional[Union[OneOfNativeLanOptionsDef1, OneOfNativeLanOptionsDef2]] = _field(
        default=None
    )
    netmask: Optional[Union[OneOfNetmaskOptionsDef1, OneOfNetmaskOptionsDef2]] = _field(
        default=None
    )
    vlan: Optional[Union[OneOfVlanOptionsDef1, OneOfVlanOptionsDef2]] = _field(default=None)


@dataclass
class Payload:
    """
    Network profile parcel schema for PUT request
    """

    data: Data
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class GetSingleNfvirtualNetworksOvsnetworkPayload:
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
    # Network profile parcel schema for PUT request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class CreateNfvirtualOvsNetworkParcelPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class OvsnetworkOneOfNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OvsnetworkOneOfInterfaceNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OvsnetworkOneOfBridgeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OvsnetworkOneOfModeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: OvsnetworkModeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OvsnetworkOneOfVlanOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OvsnetworkOneOfNativeLanOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OvsnetworkOneOfAddressOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OvsnetworkOneOfGatewayOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OvsnetworkData:
    network_name: Union[OvsnetworkOneOfNameOptionsDef1, OneOfNameOptionsDef2]
    bridge: Optional[Union[OvsnetworkOneOfBridgeOptionsDef1, OneOfBridgeOptionsDef2]] = _field(
        default=None
    )
    dhcp: Optional[Union[OneOfDhcpOptionsDef1, OneOfDhcpOptionsDef2]] = _field(default=None)
    gateway: Optional[Union[OvsnetworkOneOfGatewayOptionsDef1, OneOfGatewayOptionsDef2]] = _field(
        default=None
    )
    interface_name: Optional[
        Union[OvsnetworkOneOfInterfaceNameOptionsDef1, OneOfInterfaceNameOptionsDef2]
    ] = _field(default=None)
    ip_address: Optional[Union[OvsnetworkOneOfAddressOptionsDef1, OneOfAddressOptionsDef2]] = (
        _field(default=None)
    )
    mode: Optional[Union[OvsnetworkOneOfModeOptionsDef1, OneOfModeOptionsDef2]] = _field(
        default=None
    )
    native_vlan: Optional[Union[OvsnetworkOneOfNativeLanOptionsDef1, OneOfNativeLanOptionsDef2]] = (
        _field(default=None)
    )
    netmask: Optional[Union[OneOfNetmaskOptionsDef1, OneOfNetmaskOptionsDef2]] = _field(
        default=None
    )
    vlan: Optional[Union[OvsnetworkOneOfVlanOptionsDef1, OneOfVlanOptionsDef2]] = _field(
        default=None
    )


@dataclass
class CreateNfvirtualOvsNetworkParcelPostRequest:
    """
    Network profile parcel schema for POST request
    """

    data: OvsnetworkData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class EditNfvirtualOvsNetworkParcelPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class EditNfvirtualOvsNetworkParcelPutRequest:
    """
    Network profile parcel schema for PUT request
    """

    data: Data
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)
