# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Optional


@dataclass
class ConfigData:
    config: str


@dataclass
class Payload:
    """
    Config profile parcel schema for POST request
    """

    data: ConfigData
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
    # Config profile parcel schema for POST request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListMobilityCliConfigPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateConfigFeatureForMobilityPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class CliConfigData:
    config: str


@dataclass
class CreateConfigFeatureForMobilityPostRequest:
    """
    Config profile parcel schema for POST request
    """

    data: CliConfigData
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class MobilityCliConfigData:
    config: str


@dataclass
class ConfigPayload:
    """
    Config profile parcel schema for PUT request
    """

    data: MobilityCliConfigData
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetSingleMobilityCliConfigPayload:
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
    # Config profile parcel schema for PUT request
    payload: Optional[ConfigPayload] = _field(default=None)


@dataclass
class EditConfigFeatureForMobilityPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class FeatureProfileMobilityCliConfigData:
    config: str


@dataclass
class EditConfigFeatureForMobilityPutRequest:
    """
    Config profile parcel schema for PUT request
    """

    data: FeatureProfileMobilityCliConfigData
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
