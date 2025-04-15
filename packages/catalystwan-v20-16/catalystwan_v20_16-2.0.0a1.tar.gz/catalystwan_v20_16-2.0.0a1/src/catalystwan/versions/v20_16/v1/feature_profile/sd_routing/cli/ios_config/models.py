# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Optional


@dataclass
class IosConfigData:
    iosconfig: str


@dataclass
class Payload:
    """
    Ios Classic CLI config feature schema for POST/PUT request
    """

    data: IosConfigData
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
    # Ios Classic CLI config feature schema for POST/PUT request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdRoutingCliIosConfigPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateSdroutingIosClassicCliAddOnFeaturePostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class CliIosConfigData:
    iosconfig: str


@dataclass
class CreateSdroutingIosClassicCliAddOnFeaturePostRequest:
    """
    Ios Classic CLI config feature schema for POST/PUT request
    """

    data: CliIosConfigData
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetSingleSdRoutingCliIosConfigPayload:
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
    # Ios Classic CLI config feature schema for POST/PUT request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class EditSdroutingIosClassicCliAddOnFeaturePutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SdRoutingCliIosConfigData:
    iosconfig: str


@dataclass
class EditSdroutingIosClassicCliAddOnFeaturePutRequest:
    """
    Ios Classic CLI config feature schema for POST/PUT request
    """

    data: SdRoutingCliIosConfigData
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
