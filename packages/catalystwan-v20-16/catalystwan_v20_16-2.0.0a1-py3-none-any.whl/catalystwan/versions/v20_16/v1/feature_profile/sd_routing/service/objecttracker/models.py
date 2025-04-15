# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

VariableOptionTypeDef = Literal["variable"]

GlobalOptionTypeDef = Literal["global"]

InterfaceTrackTypeDef = Literal["ip-routing", "ipv6-routing", "line-protocol"]

DefaultOptionTypeDef = Literal["default"]

DefaultInterfaceTrackTypeDef = Literal["line-protocol"]

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
class OneOfInterfaceNameV2OptionsNoDefaultDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfInterfaceNameV2OptionsNoDefaultDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceTrackTypeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceTrackTypeDef


@dataclass
class OneOfInterfaceTrackTypeOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultInterfaceTrackTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfInterfaceTrackTypeOptionsDef3:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceObjectTrackerConfigDef:
    if_name: Union[
        OneOfInterfaceNameV2OptionsNoDefaultDef1, OneOfInterfaceNameV2OptionsNoDefaultDef2
    ] = _field(metadata={"alias": "ifName"})
    interface_track_type: Union[
        OneOfInterfaceTrackTypeOptionsDef1,
        OneOfInterfaceTrackTypeOptionsDef2,
        OneOfInterfaceTrackTypeOptionsDef3,
    ] = _field(metadata={"alias": "interfaceTrackType"})


@dataclass
class OneOfObjectTrackerConfigOptionsDef1:
    interface: OneOfInterfaceObjectTrackerConfigDef


@dataclass
class OneOfIpV4AddressOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpV4AddressOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfIpV4SubnetMaskOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpV4SubnetMaskOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Ipv4SubnetMaskDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfVrfOptionsWithDefault1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfVrfOptionsWithDefault2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfVrfOptionsWithDefault3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfRouteObjectTrackerConfigDef:
    address: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2]
    mask: Union[OneOfIpV4SubnetMaskOptionsDef1, OneOfIpV4SubnetMaskOptionsDef2]
    vrf_name: Union[
        OneOfVrfOptionsWithDefault1, OneOfVrfOptionsWithDefault2, OneOfVrfOptionsWithDefault3
    ] = _field(metadata={"alias": "vrfName"})


@dataclass
class OneOfObjectTrackerConfigOptionsDef2:
    route: OneOfRouteObjectTrackerConfigDef


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
class ObjecttrackerData:
    delay_down_time: Union[
        OneOfDelayDownTimeOptionsDef1, OneOfDelayDownTimeOptionsDef2, OneOfDelayDownTimeOptionsDef3
    ] = _field(metadata={"alias": "delayDownTime"})
    delay_up_time: Union[
        OneOfDelayUpTimeOptionsDef1, OneOfDelayUpTimeOptionsDef2, OneOfDelayUpTimeOptionsDef3
    ] = _field(metadata={"alias": "delayUpTime"})
    tracker_config: Union[
        OneOfObjectTrackerConfigOptionsDef1, OneOfObjectTrackerConfigOptionsDef2
    ] = _field(metadata={"alias": "trackerConfig"})
    tracker_id: Union[OneOfTrackerObjectIdDef1, OneOfTrackerObjectIdDef2] = _field(
        metadata={"alias": "trackerId"}
    )


@dataclass
class Payload:
    """
    SD-Routing object tracker feature schema
    """

    data: ObjecttrackerData
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
    # SD-Routing object tracker feature schema
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdRoutingServiceObjecttrackerPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateSdroutingServiceObjectTrackerFeaturePostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class ServiceObjecttrackerData:
    delay_down_time: Union[
        OneOfDelayDownTimeOptionsDef1, OneOfDelayDownTimeOptionsDef2, OneOfDelayDownTimeOptionsDef3
    ] = _field(metadata={"alias": "delayDownTime"})
    delay_up_time: Union[
        OneOfDelayUpTimeOptionsDef1, OneOfDelayUpTimeOptionsDef2, OneOfDelayUpTimeOptionsDef3
    ] = _field(metadata={"alias": "delayUpTime"})
    tracker_config: Union[
        OneOfObjectTrackerConfigOptionsDef1, OneOfObjectTrackerConfigOptionsDef2
    ] = _field(metadata={"alias": "trackerConfig"})
    tracker_id: Union[OneOfTrackerObjectIdDef1, OneOfTrackerObjectIdDef2] = _field(
        metadata={"alias": "trackerId"}
    )


@dataclass
class CreateSdroutingServiceObjectTrackerFeaturePostRequest:
    """
    SD-Routing object tracker feature schema
    """

    data: ServiceObjecttrackerData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class GetSingleSdRoutingServiceObjecttrackerPayload:
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
    # SD-Routing object tracker feature schema
    payload: Optional[Payload] = _field(default=None)


@dataclass
class EditSdroutingServiceObjectTrackerFeaturePutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SdRoutingServiceObjecttrackerData:
    delay_down_time: Union[
        OneOfDelayDownTimeOptionsDef1, OneOfDelayDownTimeOptionsDef2, OneOfDelayDownTimeOptionsDef3
    ] = _field(metadata={"alias": "delayDownTime"})
    delay_up_time: Union[
        OneOfDelayUpTimeOptionsDef1, OneOfDelayUpTimeOptionsDef2, OneOfDelayUpTimeOptionsDef3
    ] = _field(metadata={"alias": "delayUpTime"})
    tracker_config: Union[
        OneOfObjectTrackerConfigOptionsDef1, OneOfObjectTrackerConfigOptionsDef2
    ] = _field(metadata={"alias": "trackerConfig"})
    tracker_id: Union[OneOfTrackerObjectIdDef1, OneOfTrackerObjectIdDef2] = _field(
        metadata={"alias": "trackerId"}
    )


@dataclass
class EditSdroutingServiceObjectTrackerFeaturePutRequest:
    """
    SD-Routing object tracker feature schema
    """

    data: SdRoutingServiceObjecttrackerData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)
