# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

VariableOptionTypeDef = Literal["variable"]

GlobalOptionTypeDef = Literal["global"]

TrackGroupBooleanDef = Literal["and", "or"]

DefaultOptionTypeDef = Literal["default"]

DefaultTrackGroupBooleanDef = Literal["or"]


@dataclass
class OneOfTrackerObjectIdDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTrackerObjectIdDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


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
class TrackGroupRefDef:
    tracker_ref: ParcelReferenceDef = _field(metadata={"alias": "trackerRef"})


@dataclass
class OneOfTrackerBooleanOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTrackerBooleanOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: TrackGroupBooleanDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfTrackerBooleanOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultTrackGroupBooleanDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfDelayUpTimeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfDelayUpTimeOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfDelayUpTimeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfDelayDownTimeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfDelayDownTimeOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfDelayDownTimeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class ObjecttrackergroupData:
    criteria: Union[
        OneOfTrackerBooleanOptionsDef1,
        OneOfTrackerBooleanOptionsDef2,
        OneOfTrackerBooleanOptionsDef3,
    ]
    delay_down_time: Union[
        OneOfDelayDownTimeOptionsDef1, OneOfDelayDownTimeOptionsDef2, OneOfDelayDownTimeOptionsDef3
    ] = _field(metadata={"alias": "delayDownTime"})
    delay_up_time: Union[
        OneOfDelayUpTimeOptionsDef1, OneOfDelayUpTimeOptionsDef2, OneOfDelayUpTimeOptionsDef3
    ] = _field(metadata={"alias": "delayUpTime"})
    object_id: Union[OneOfTrackerObjectIdDef1, OneOfTrackerObjectIdDef2] = _field(
        metadata={"alias": "objectId"}
    )
    # Group Tracks ID Refs
    tracker_refs: List[TrackGroupRefDef] = _field(metadata={"alias": "trackerRefs"})


@dataclass
class Payload:
    """
    SD-Routing object tracker group feature schema
    """

    data: ObjecttrackergroupData
    name: str
    # Feature description
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
    # SD-Routing object tracker group feature schema
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdRoutingServiceObjecttrackergroupPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateSdroutingServiceObjectTrackerGroupFeaturePostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class ServiceObjecttrackergroupData:
    criteria: Union[
        OneOfTrackerBooleanOptionsDef1,
        OneOfTrackerBooleanOptionsDef2,
        OneOfTrackerBooleanOptionsDef3,
    ]
    delay_down_time: Union[
        OneOfDelayDownTimeOptionsDef1, OneOfDelayDownTimeOptionsDef2, OneOfDelayDownTimeOptionsDef3
    ] = _field(metadata={"alias": "delayDownTime"})
    delay_up_time: Union[
        OneOfDelayUpTimeOptionsDef1, OneOfDelayUpTimeOptionsDef2, OneOfDelayUpTimeOptionsDef3
    ] = _field(metadata={"alias": "delayUpTime"})
    object_id: Union[OneOfTrackerObjectIdDef1, OneOfTrackerObjectIdDef2] = _field(
        metadata={"alias": "objectId"}
    )
    # Group Tracks ID Refs
    tracker_refs: List[TrackGroupRefDef] = _field(metadata={"alias": "trackerRefs"})


@dataclass
class CreateSdroutingServiceObjectTrackerGroupFeaturePostRequest:
    """
    SD-Routing object tracker group feature schema
    """

    data: ServiceObjecttrackergroupData
    name: str
    # Feature description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetSingleSdRoutingServiceObjecttrackergroupPayload:
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
    # SD-Routing object tracker group feature schema
    payload: Optional[Payload] = _field(default=None)


@dataclass
class EditSdroutingServiceObjectTrackerGroupFeaturePutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SdRoutingServiceObjecttrackergroupData:
    criteria: Union[
        OneOfTrackerBooleanOptionsDef1,
        OneOfTrackerBooleanOptionsDef2,
        OneOfTrackerBooleanOptionsDef3,
    ]
    delay_down_time: Union[
        OneOfDelayDownTimeOptionsDef1, OneOfDelayDownTimeOptionsDef2, OneOfDelayDownTimeOptionsDef3
    ] = _field(metadata={"alias": "delayDownTime"})
    delay_up_time: Union[
        OneOfDelayUpTimeOptionsDef1, OneOfDelayUpTimeOptionsDef2, OneOfDelayUpTimeOptionsDef3
    ] = _field(metadata={"alias": "delayUpTime"})
    object_id: Union[OneOfTrackerObjectIdDef1, OneOfTrackerObjectIdDef2] = _field(
        metadata={"alias": "objectId"}
    )
    # Group Tracks ID Refs
    tracker_refs: List[TrackGroupRefDef] = _field(metadata={"alias": "trackerRefs"})


@dataclass
class EditSdroutingServiceObjectTrackerGroupFeaturePutRequest:
    """
    SD-Routing object tracker group feature schema
    """

    data: SdRoutingServiceObjecttrackergroupData
    name: str
    # Feature description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
