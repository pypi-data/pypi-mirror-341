# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, Literal, Optional, Union

VariableOptionTypeDef = Literal["variable"]

GlobalOptionTypeDef = Literal["global"]

DefaultOptionTypeDef = Literal["default"]

ModeDef = Literal["ms-based", "standalone"]

DefaultModeDef = Literal["ms-based"]

GpsModeDef = Literal["ms-based", "standalone"]

GpsDefaultModeDef = Literal["ms-based"]


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
    value: DefaultModeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfNmeaOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfNmeaOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfNmeaOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfSourceAddressOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfSourceAddressOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfSourceAddressOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfDestinationAddressOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfDestinationAddressOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfDestinationAddressOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfDestinationPortOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfDestinationPortOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfDestinationPortOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class Data:
    destination_address: Optional[
        Union[
            OneOfDestinationAddressOptionsDef1,
            OneOfDestinationAddressOptionsDef2,
            OneOfDestinationAddressOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "destinationAddress"})
    destination_port: Optional[
        Union[
            OneOfDestinationPortOptionsDef1,
            OneOfDestinationPortOptionsDef2,
            OneOfDestinationPortOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "destinationPort"})
    enable: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)
    mode: Optional[Union[OneOfModeOptionsDef1, OneOfModeOptionsDef2, OneOfModeOptionsDef3]] = (
        _field(default=None)
    )
    nmea: Optional[Union[OneOfNmeaOptionsDef1, OneOfNmeaOptionsDef2, OneOfNmeaOptionsDef3]] = (
        _field(default=None)
    )
    source_address: Optional[
        Union[
            OneOfSourceAddressOptionsDef1,
            OneOfSourceAddressOptionsDef2,
            OneOfSourceAddressOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sourceAddress"})


@dataclass
class Payload:
    """
    Gps profile parcel schema for POST request
    """

    data: Data
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class GetCellularControllerAssociatedGpsParcelsForTransport1GetResponse:
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
    # Gps profile parcel schema for POST request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class CreateCellularControllerAndGpsParcelAssociationForTransport1PostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class CreateCellularControllerAndGpsParcelAssociationForTransport1PostRequest:
    """
    Profile Parcel POST Request schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GpsOneOfModeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: GpsModeDef


@dataclass
class GpsOneOfModeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: GpsDefaultModeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class GpsData:
    destination_address: Optional[
        Union[
            OneOfDestinationAddressOptionsDef1,
            OneOfDestinationAddressOptionsDef2,
            OneOfDestinationAddressOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "destinationAddress"})
    destination_port: Optional[
        Union[
            OneOfDestinationPortOptionsDef1,
            OneOfDestinationPortOptionsDef2,
            OneOfDestinationPortOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "destinationPort"})
    enable: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)
    mode: Optional[
        Union[GpsOneOfModeOptionsDef1, OneOfModeOptionsDef2, GpsOneOfModeOptionsDef3]
    ] = _field(default=None)
    nmea: Optional[Union[OneOfNmeaOptionsDef1, OneOfNmeaOptionsDef2, OneOfNmeaOptionsDef3]] = (
        _field(default=None)
    )
    source_address: Optional[
        Union[
            OneOfSourceAddressOptionsDef1,
            OneOfSourceAddressOptionsDef2,
            OneOfSourceAddressOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sourceAddress"})


@dataclass
class GpsPayload:
    """
    Gps profile parcel schema for PUT request
    """

    data: GpsData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class GetSingleSdRoutingTransportCellularControllerGpsPayload:
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
    # Gps profile parcel schema for PUT request
    payload: Optional[GpsPayload] = _field(default=None)
