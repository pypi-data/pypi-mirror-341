# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import List


@dataclass
class Devices:
    # Indicates if the device was added by a rule
    added_by_rule: bool = _field(metadata={"alias": "addedByRule"})
    # Timestamp of the last update to the config group
    config_group_last_updated_on: str = _field(metadata={"alias": "configGroupLastUpdatedOn"})
    # Indicates if the config group is up to date
    config_group_up_to_date: str = _field(metadata={"alias": "configGroupUpToDate"})
    # Configuration status message
    config_status_message: str = _field(metadata={"alias": "configStatusMessage"})
    # IP address of the device
    device_ip: str = _field(metadata={"alias": "deviceIP"})
    # Indicates if the device is locked
    device_lock: str = _field(metadata={"alias": "device-lock"})
    # Model of the device
    device_model: str = _field(metadata={"alias": "deviceModel"})
    # Hierarchy name path
    hierarchy_name_path: str = _field(metadata={"alias": "hierarchyNamePath"})
    # Hierarchy type path
    hierarchy_type_path: str = _field(metadata={"alias": "hierarchyTypePath"})
    # Host name of the device
    host_name: str = _field(metadata={"alias": "host-name"})
    # Unique identifier for the device
    id: str
    # Identifier for the site
    site_id: str = _field(metadata={"alias": "site-id"})
    # Name of the site
    site_name: str = _field(metadata={"alias": "site-name"})
    # Tags associated with the device
    tags: List[str]
    # List of unsupported features
    unsupported_features: List[str] = _field(metadata={"alias": "unsupportedFeatures"})


@dataclass
class GetConfigGroupAssociationGetResponse:
    """
    Schema for the response of a GET request to associate a config group
    """

    devices: List[Devices]


@dataclass
class DeviceIdDef:
    id: str


@dataclass
class UpdateConfigGroupAssociationPutRequest:
    """
    Config Group Associate Put Request schema
    """

    # list of device ids that config group need to be associated with
    devices: List[DeviceIdDef]


@dataclass
class AssociateDeviceIdDef:
    id: str


@dataclass
class CreateConfigGroupAssociationPostRequest:
    """
    Config Group Associate Post Request schema
    """

    # list of device ids that config group need to be associated with
    devices: List[AssociateDeviceIdDef]


@dataclass
class DeviceAssociateDeviceIdDef:
    id: str


@dataclass
class DeleteConfigGroupAssociationDeleteRequest:
    """
    Config Group Associate Delete Request schema
    """

    # list of device ids that config group need to be associated with
    devices: List[DeviceAssociateDeviceIdDef]
