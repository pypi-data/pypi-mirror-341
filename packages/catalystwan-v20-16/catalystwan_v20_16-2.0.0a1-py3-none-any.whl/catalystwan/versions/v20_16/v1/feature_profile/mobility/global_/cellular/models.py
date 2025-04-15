# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List, Literal, Optional

Type = Literal[
    "cellular", "ethernet", "globalSettings", "networkProtocol", "securityPolicy", "wifi"
]


@dataclass
class CellularProfile:
    apn: Optional[str] = _field(default=None)
    auth_method: Optional[str] = _field(default=None, metadata={"alias": "authMethod"})
    id: Optional[int] = _field(default=None)
    password: Optional[str] = _field(default=None)
    pdn_type: Optional[str] = _field(default=None, metadata={"alias": "pdnType"})
    user_name: Optional[str] = _field(default=None, metadata={"alias": "userName"})


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
    payload: Optional[CellularProfile] = _field(default=None)


@dataclass
class GetListMobilityGlobalCellularPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class Variable:
    json_path: str = _field(metadata={"alias": "jsonPath"})
    var_name: str = _field(metadata={"alias": "varName"})


@dataclass
class SimSlotConfig:
    attach_profile_id: int = _field(metadata={"alias": "attachProfileId"})
    profile_list: List[CellularProfile] = _field(metadata={"alias": "profileList"})
    slot_number: int = _field(metadata={"alias": "slotNumber"})
    carrier_name: Optional[str] = _field(default=None, metadata={"alias": "carrierName"})
    data_profile_id_list: Optional[List[int]] = _field(
        default=None, metadata={"alias": "dataProfileIdList"}
    )


@dataclass
class Cellular:
    # Name of the Profile Parcel. Must be unique.
    name: str
    primary_slot: int = _field(metadata={"alias": "primarySlot"})
    type_: Type = _field(metadata={"alias": "type"})  # pytype: disable=annotation-type-mismatch
    # User who last created this.
    created_by: Optional[str] = _field(default=None, metadata={"alias": "createdBy"})
    # Timestamp of creation
    created_on: Optional[int] = _field(default=None, metadata={"alias": "createdOn"})
    # Description of the Profile Parcel.
    description: Optional[str] = _field(default=None)
    # System generated unique identifier of the Profile Parcel in UUID format.
    id: Optional[str] = _field(default=None)
    # User who last updated this.
    last_updated_by: Optional[str] = _field(default=None, metadata={"alias": "lastUpdatedBy"})
    # Timestamp of last update
    last_updated_on: Optional[int] = _field(default=None, metadata={"alias": "lastUpdatedOn"})
    sim_slot0: Optional[SimSlotConfig] = _field(default=None, metadata={"alias": "simSlot0"})
    sim_slot1: Optional[SimSlotConfig] = _field(default=None, metadata={"alias": "simSlot1"})
    variables: Optional[List[Variable]] = _field(default=None)
    wan_config: Optional[str] = _field(default=None, metadata={"alias": "wanConfig"})


@dataclass
class GetSingleMobilityGlobalCellularPayload:
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
    payload: Optional[Cellular] = _field(default=None)


@dataclass
class EditCellularProfileParcelForMobilityPutRequest:
    # Name of the Profile Parcel. Must be unique.
    name: str
    primary_slot: int = _field(metadata={"alias": "primarySlot"})
    type_: Type = _field(metadata={"alias": "type"})  # pytype: disable=annotation-type-mismatch
    # User who last created this.
    created_by: Optional[str] = _field(default=None, metadata={"alias": "createdBy"})
    # Timestamp of creation
    created_on: Optional[int] = _field(default=None, metadata={"alias": "createdOn"})
    # Description of the Profile Parcel.
    description: Optional[str] = _field(default=None)
    # System generated unique identifier of the Profile Parcel in UUID format.
    id: Optional[str] = _field(default=None)
    # User who last updated this.
    last_updated_by: Optional[str] = _field(default=None, metadata={"alias": "lastUpdatedBy"})
    # Timestamp of last update
    last_updated_on: Optional[int] = _field(default=None, metadata={"alias": "lastUpdatedOn"})
    sim_slot0: Optional[SimSlotConfig] = _field(default=None, metadata={"alias": "simSlot0"})
    sim_slot1: Optional[SimSlotConfig] = _field(default=None, metadata={"alias": "simSlot1"})
    variables: Optional[List[Variable]] = _field(default=None)
    wan_config: Optional[str] = _field(default=None, metadata={"alias": "wanConfig"})
