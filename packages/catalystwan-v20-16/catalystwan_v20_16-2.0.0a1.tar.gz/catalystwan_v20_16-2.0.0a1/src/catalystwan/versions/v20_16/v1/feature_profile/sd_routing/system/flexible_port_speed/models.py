# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

PortConfigModeDef = Literal[
    "12 ports of 1/10GE + 1 port of 100GE",
    "12 ports of 1/10GE + 3 ports 40GE",
    "2 ports of 100 GE",
    "3 ports of 40GE + 1port of 100GE",
    "8 ports of 1/10GE + 1 port of 40GE + 1 port of 100GE",
    "8 ports of 1/10GE + 4 ports of 40GE",
]

VariableOptionTypeDef = Literal["variable"]

DefaultOptionTypeDef = Literal["default"]

DefaultPortConfigModeDef = Literal["12 ports of 1/10GE + 3 ports 40GE"]


@dataclass
class OneOfPortOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: PortConfigModeDef


@dataclass
class OneOfPortOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfPortOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultPortConfigModeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class FlexiblePortSpeedData:
    port_type: Optional[Union[OneOfPortOptionsDef1, OneOfPortOptionsDef2, OneOfPortOptionsDef3]] = (
        _field(default=None, metadata={"alias": "portType"})
    )


@dataclass
class Payload:
    """
    Flexible Port Speed profile feature schema for request
    """

    data: FlexiblePortSpeedData
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
    # Flexible Port Speed profile feature schema for request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdRoutingSystemFlexiblePortSpeedPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateSdroutingFlexiblePortSpeedFeaturePostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SystemFlexiblePortSpeedData:
    port_type: Optional[Union[OneOfPortOptionsDef1, OneOfPortOptionsDef2, OneOfPortOptionsDef3]] = (
        _field(default=None, metadata={"alias": "portType"})
    )


@dataclass
class CreateSdroutingFlexiblePortSpeedFeaturePostRequest:
    """
    Flexible Port Speed profile feature schema for request
    """

    data: SystemFlexiblePortSpeedData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class GetSingleSdRoutingSystemFlexiblePortSpeedPayload:
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
    # Flexible Port Speed profile feature schema for request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class EditSdroutingFlexiblePortSpeedFeaturePutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SdRoutingSystemFlexiblePortSpeedData:
    port_type: Optional[Union[OneOfPortOptionsDef1, OneOfPortOptionsDef2, OneOfPortOptionsDef3]] = (
        _field(default=None, metadata={"alias": "portType"})
    )


@dataclass
class EditSdroutingFlexiblePortSpeedFeaturePutRequest:
    """
    Flexible Port Speed profile feature schema for request
    """

    data: SdRoutingSystemFlexiblePortSpeedData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)
