# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Dict, List, Literal, Optional

Solution = Literal[
    "cellulargateway", "common", "mobility", "nfvirtual", "sd-routing", "sdwan", "service-insertion"
]

TopologyGroupSolution = Literal["sdwan"]

V1TopologyGroupSolution = Literal["sdwan"]


@dataclass
class FeatureProfile:
    """
    List of devices UUIDs associated with this group
    """

    # Name of the feature Profile. Must be unique.
    name: str
    # Solution of the feature Profile.
    solution: str
    # Type of the feature Profile.
    type_: str = _field(metadata={"alias": "type"})
    # User who last created this.
    created_by: Optional[str] = _field(default=None, metadata={"alias": "createdBy"})
    # Timestamp of creation
    created_on: Optional[int] = _field(default=None, metadata={"alias": "createdOn"})
    # Description of the feature Profile.
    description: Optional[str] = _field(default=None)
    # System generated unique identifier of the feature profile in UUID format.
    id: Optional[str] = _field(default=None)
    # User who last updated this.
    last_updated_by: Optional[str] = _field(default=None, metadata={"alias": "lastUpdatedBy"})
    # Timestamp of last update
    last_updated_on: Optional[int] = _field(default=None, metadata={"alias": "lastUpdatedOn"})
    # Number of Parcels attached with Feature Profile
    profile_parcel_count: Optional[int] = _field(
        default=None, metadata={"alias": "profileParcelCount"}
    )


@dataclass
class TopologyGroup:
    # Name of the  Group. Must be unique.
    name: str
    # Specify one of the device platform solution
    solution: Solution  # pytype: disable=annotation-type-mismatch
    #  Group Deployment state
    state: str
    #  Group Version Flag
    version: int
    active_status: Optional[bool] = _field(default=None, metadata={"alias": "activeStatus"})
    copy_info: Optional[str] = _field(default=None, metadata={"alias": "copyInfo"})
    # User who last created this.
    created_by: Optional[str] = _field(default=None, metadata={"alias": "createdBy"})
    # Timestamp of creation
    created_on: Optional[int] = _field(default=None, metadata={"alias": "createdOn"})
    # Description of the  Group.
    description: Optional[str] = _field(default=None)
    devices: Optional[List[str]] = _field(default=None)
    # System generated unique identifier of the  Group in UUID format.
    id: Optional[str] = _field(default=None)
    # User who last updated this.
    last_updated_by: Optional[str] = _field(default=None, metadata={"alias": "lastUpdatedBy"})
    # Timestamp of last update
    last_updated_on: Optional[int] = _field(default=None, metadata={"alias": "lastUpdatedOn"})
    number_of_devices: Optional[int] = _field(default=None, metadata={"alias": "numberOfDevices"})
    number_of_devices_up_to_date: Optional[int] = _field(
        default=None, metadata={"alias": "numberOfDevicesUpToDate"}
    )
    origin: Optional[str] = _field(default=None)
    origin_info: Optional[Dict[str, str]] = _field(default=None, metadata={"alias": "originInfo"})
    # List of devices UUIDs associated with this group
    profiles: Optional[List[FeatureProfile]] = _field(default=None)
    # Source of group
    source: Optional[str] = _field(default=None)


@dataclass
class ProfileIdObjDef:
    id: str


@dataclass
class FromTopologyGroupDef:
    copy: str


@dataclass
class CreateTopologyGroupPostRequest:
    """
    Topology Group POST Request schema
    """

    description: str
    name: str
    solution: TopologyGroupSolution  # pytype: disable=annotation-type-mismatch
    from_topology_group: Optional[FromTopologyGroupDef] = _field(
        default=None, metadata={"alias": "fromTopologyGroup"}
    )
    # list of profile ids that belongs to the topology group
    profiles: Optional[List[ProfileIdObjDef]] = _field(default=None)


@dataclass
class TopologyGroupProfileIdObjDef:
    id: str


@dataclass
class EditTopologyGroupPutRequest:
    """
    Topology Group PUT Request schema
    """

    description: str
    name: str
    solution: V1TopologyGroupSolution  # pytype: disable=annotation-type-mismatch
    # list of profile ids that belongs to the topology group
    profiles: Optional[List[TopologyGroupProfileIdObjDef]] = _field(default=None)
