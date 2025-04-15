# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional

GlobalOptionTypeDef = Literal["global"]


@dataclass
class OneOfRadiusServerNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfRadiusServerIpAddressOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfRadiusServerPortOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfRadiusServerSecretOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class RadiusServers:
    ip_address: OneOfRadiusServerIpAddressOptionsDef = _field(metadata={"alias": "ipAddress"})
    name: OneOfRadiusServerNameOptionsDef
    port: OneOfRadiusServerPortOptionsDef
    secret: OneOfRadiusServerSecretOptionsDef


@dataclass
class AaaserversData:
    # Radius Server Configuration
    radius_servers: List[RadiusServers] = _field(metadata={"alias": "radiusServers"})


@dataclass
class Payload:
    """
    AON AAA Servers profile parcel schema for POST request
    """

    data: AaaserversData
    name: str
    # Set the parcel description
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
    # AON AAA Servers profile parcel schema for POST request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListMobilityGlobalAaaserversPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateAaaServersProfileParcelForMobilityPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GlobalAaaserversData:
    # Radius Server Configuration
    radius_servers: List[RadiusServers] = _field(metadata={"alias": "radiusServers"})


@dataclass
class CreateAaaServersProfileParcelForMobilityPostRequest:
    """
    AON AAA Servers profile parcel schema for POST request
    """

    data: GlobalAaaserversData
    name: str
    # Set the parcel description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class AaaserversOneOfRadiusServerNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class AaaserversOneOfRadiusServerPortOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class AaaserversOneOfRadiusServerSecretOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class AaaserversRadiusServers:
    ip_address: OneOfRadiusServerIpAddressOptionsDef = _field(metadata={"alias": "ipAddress"})
    name: AaaserversOneOfRadiusServerNameOptionsDef
    port: AaaserversOneOfRadiusServerPortOptionsDef
    secret: AaaserversOneOfRadiusServerSecretOptionsDef


@dataclass
class MobilityGlobalAaaserversData:
    # Radius Server Configuration
    radius_servers: List[AaaserversRadiusServers] = _field(metadata={"alias": "radiusServers"})


@dataclass
class AaaserversPayload:
    """
    AON AAA Servers profile parcel schema for PUT request
    """

    data: MobilityGlobalAaaserversData
    name: str
    # Set the parcel description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetSingleMobilityGlobalAaaserversPayload:
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
    # AON AAA Servers profile parcel schema for PUT request
    payload: Optional[AaaserversPayload] = _field(default=None)


@dataclass
class EditAaaServersProfileParcelForMobilityPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GlobalAaaserversOneOfRadiusServerNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class GlobalAaaserversOneOfRadiusServerPortOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class GlobalAaaserversOneOfRadiusServerSecretOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class GlobalAaaserversRadiusServers:
    ip_address: OneOfRadiusServerIpAddressOptionsDef = _field(metadata={"alias": "ipAddress"})
    name: GlobalAaaserversOneOfRadiusServerNameOptionsDef
    port: GlobalAaaserversOneOfRadiusServerPortOptionsDef
    secret: GlobalAaaserversOneOfRadiusServerSecretOptionsDef


@dataclass
class FeatureProfileMobilityGlobalAaaserversData:
    # Radius Server Configuration
    radius_servers: List[GlobalAaaserversRadiusServers] = _field(
        metadata={"alias": "radiusServers"}
    )


@dataclass
class EditAaaServersProfileParcelForMobilityPutRequest:
    """
    AON AAA Servers profile parcel schema for PUT request
    """

    data: FeatureProfileMobilityGlobalAaaserversData
    name: str
    # Set the parcel description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
