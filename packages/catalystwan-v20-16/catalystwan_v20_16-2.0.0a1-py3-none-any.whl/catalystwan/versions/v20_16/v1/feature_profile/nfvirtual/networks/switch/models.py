# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

InterfacesInterfaceNameDef = Literal[
    "gigabitEthernet1/0",
    "gigabitEthernet1/1",
    "gigabitEthernet1/2",
    "gigabitEthernet1/3",
    "gigabitEthernet1/4",
    "gigabitEthernet1/5",
    "gigabitEthernet1/6",
    "gigabitEthernet1/7",
]

VariableOptionTypeDef = Literal["variable"]

InterfacesModeDef = Literal["access", "trunk"]

SwitchInterfacesInterfaceNameDef = Literal[
    "gigabitEthernet1/0",
    "gigabitEthernet1/1",
    "gigabitEthernet1/2",
    "gigabitEthernet1/3",
    "gigabitEthernet1/4",
    "gigabitEthernet1/5",
    "gigabitEthernet1/6",
    "gigabitEthernet1/7",
]

SwitchInterfacesModeDef = Literal["access", "trunk"]

NetworksSwitchInterfacesInterfaceNameDef = Literal[
    "gigabitEthernet1/0",
    "gigabitEthernet1/1",
    "gigabitEthernet1/2",
    "gigabitEthernet1/3",
    "gigabitEthernet1/4",
    "gigabitEthernet1/5",
    "gigabitEthernet1/6",
    "gigabitEthernet1/7",
]

NetworksSwitchInterfacesModeDef = Literal["access", "trunk"]


@dataclass
class CreateNfvirtualSwitchParcelPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class OneOfInterfacesInterfaceNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfacesInterfaceNameDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfInterfacesInterfaceNameOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfacesVlanOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfInterfacesVlanOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfacesModeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfacesModeDef


@dataclass
class OneOfInterfacesNativeVlanOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class Interfaces:
    interface_name: Union[
        OneOfInterfacesInterfaceNameOptionsDef1, OneOfInterfacesInterfaceNameOptionsDef2
    ]
    mode: Optional[OneOfInterfacesModeOptionsDef] = _field(default=None)
    native_vlan: Optional[OneOfInterfacesNativeVlanOptionsDef] = _field(default=None)
    vlan: Optional[Union[OneOfInterfacesVlanOptionsDef1, OneOfInterfacesVlanOptionsDef2]] = _field(
        default=None
    )


@dataclass
class Data:
    # List of Interfaces
    interfaces: Optional[List[Interfaces]] = _field(default=None)


@dataclass
class CreateNfvirtualSwitchParcelPostRequest:
    """
    Switch profile parcel schema for POST request
    """

    data: Data
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class SwitchOneOfInterfacesInterfaceNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SwitchInterfacesInterfaceNameDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SwitchOneOfInterfacesVlanOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SwitchOneOfInterfacesModeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SwitchInterfacesModeDef


@dataclass
class SwitchOneOfInterfacesNativeVlanOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SwitchInterfaces:
    interface_name: Union[
        SwitchOneOfInterfacesInterfaceNameOptionsDef1, OneOfInterfacesInterfaceNameOptionsDef2
    ]
    mode: Optional[SwitchOneOfInterfacesModeOptionsDef] = _field(default=None)
    native_vlan: Optional[SwitchOneOfInterfacesNativeVlanOptionsDef] = _field(default=None)
    vlan: Optional[Union[SwitchOneOfInterfacesVlanOptionsDef1, OneOfInterfacesVlanOptionsDef2]] = (
        _field(default=None)
    )


@dataclass
class SwitchData:
    # List of Interfaces
    interfaces: Optional[List[SwitchInterfaces]] = _field(default=None)


@dataclass
class Payload:
    """
    Switch profile parcel schema for PUT request
    """

    data: SwitchData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class GetSingleNfvirtualNetworksSwitchPayload:
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
    # Switch profile parcel schema for PUT request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class EditNfvirtualSwitchParcelPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class NetworksSwitchOneOfInterfacesInterfaceNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: NetworksSwitchInterfacesInterfaceNameDef  # pytype: disable=annotation-type-mismatch


@dataclass
class NetworksSwitchOneOfInterfacesVlanOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class NetworksSwitchOneOfInterfacesModeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: NetworksSwitchInterfacesModeDef


@dataclass
class NetworksSwitchOneOfInterfacesNativeVlanOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class NetworksSwitchInterfaces:
    interface_name: Union[
        NetworksSwitchOneOfInterfacesInterfaceNameOptionsDef1,
        OneOfInterfacesInterfaceNameOptionsDef2,
    ]
    mode: Optional[NetworksSwitchOneOfInterfacesModeOptionsDef] = _field(default=None)
    native_vlan: Optional[NetworksSwitchOneOfInterfacesNativeVlanOptionsDef] = _field(default=None)
    vlan: Optional[
        Union[NetworksSwitchOneOfInterfacesVlanOptionsDef1, OneOfInterfacesVlanOptionsDef2]
    ] = _field(default=None)


@dataclass
class NetworksSwitchData:
    # List of Interfaces
    interfaces: Optional[List[NetworksSwitchInterfaces]] = _field(default=None)


@dataclass
class EditNfvirtualSwitchParcelPutRequest:
    """
    Switch profile parcel schema for PUT request
    """

    data: NetworksSwitchData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)
