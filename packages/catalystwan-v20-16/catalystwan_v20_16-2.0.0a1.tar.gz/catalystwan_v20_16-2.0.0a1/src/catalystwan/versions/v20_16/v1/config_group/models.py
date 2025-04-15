# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Dict, List, Literal, Optional

Solution = Literal[
    "cellulargateway", "common", "mobility", "nfvirtual", "sd-routing", "sdwan", "service-insertion"
]

Attribute = Literal["tag"]

ParcelType = Literal[
    "global-vrf",
    "global-vrf/routing/bgp",
    "global-vrf/wan/interface/ipsec",
    "lan/multicloud-connection",
    "lan/vpn",
    "lan/vpn/interface/ethernet",
    "lan/vpn/interface/gre",
    "lan/vpn/interface/ipsec",
    "lan/vpn/interface/svi",
    "route-policy",
    "routing/bgp",
    "routing/ospf",
    "service-insertion-attachment",
    "vrf",
    "vrf/lan/interface/ethernet",
    "vrf/lan/interface/gre",
    "vrf/lan/interface/ipsec",
    "vrf/lan/multicloud-connection",
    "vrf/routing/bgp",
    "vrf/wan/interface/ethernet",
    "vrf/wan/interface/gre",
    "vrf/wan/interface/ipsec",
    "vrf/wan/multicloud-connection",
    "wan/multicloud-connection",
    "wan/vpn/interface/cellular",
    "wan/vpn/interface/dsl-ipoe",
    "wan/vpn/interface/dsl-pppoa",
    "wan/vpn/interface/dsl-pppoe",
    "wan/vpn/interface/ethernet",
    "wan/vpn/interface/gre",
    "wan/vpn/interface/ipsec",
    "wan/vpn/interface/serial",
]

ProfileType = Literal["global"]

Source = Literal["custom_workflow", "equinix_workflow", "nfvirtual_workflow", "retail_workflow"]

SolutionDef = Literal[
    "cellulargateway", "mobility", "nfvirtual", "sd-routing", "sdwan", "service-insertion"
]

UnsupportedFeaturesEnumDef = Literal[
    "lan/multicloud-connection",
    "lan/vpn",
    "lan/vpn/interface/ethernet",
    "lan/vpn/interface/ipsec",
    "lan/vpn/interface/svi",
    "route-policy",
    "routing/bgp",
    "routing/ospf",
    "vrf",
    "vrf/lan/interface/ethernet",
    "vrf/lan/interface/ipsec",
    "vrf/lan/multicloud-connection",
    "vrf/routing/bgp",
    "vrf/wan/interface/ethernet",
    "vrf/wan/interface/gre",
    "vrf/wan/interface/ipsec",
    "vrf/wan/multicloud-connection",
    "wan/multicloud-connection",
    "wan/vpn/interface/cellular",
    "wan/vpn/interface/dsl-ipoe",
    "wan/vpn/interface/dsl-pppoa",
    "wan/vpn/interface/dsl-pppoe",
    "wan/vpn/interface/ethernet",
    "wan/vpn/interface/gre",
    "wan/vpn/interface/ipsec",
    "wan/vpn/interface/serial",
]


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
class Criteria:
    attribute: Optional[Attribute] = _field(default=None)
    value: Optional[str] = _field(default=None)


@dataclass
class UnsupportedFeature:
    parcel_id: Optional[str] = _field(default=None, metadata={"alias": "parcelId"})
    parcel_type: Optional[ParcelType] = _field(default=None, metadata={"alias": "parcelType"})


@dataclass
class ConfigGroupDevice:
    criteria: Optional[Criteria] = _field(default=None)
    unsupported_features: Optional[List[UnsupportedFeature]] = _field(
        default=None, metadata={"alias": "unsupportedFeatures"}
    )


@dataclass
class Topology:
    devices: Optional[List[ConfigGroupDevice]] = _field(default=None)
    site_devices: Optional[int] = _field(default=None, metadata={"alias": "siteDevices"})


@dataclass
class ConfigGroup:
    # Name of the  Group. Must be unique.
    name: str
    # Specify one of the device platform solution
    solution: Solution  # pytype: disable=annotation-type-mismatch
    #  Group Deployment state
    state: str
    #  Group Version Flag
    version: int
    copy_info: Optional[str] = _field(default=None, metadata={"alias": "copyInfo"})
    # User who last created this.
    created_by: Optional[str] = _field(default=None, metadata={"alias": "createdBy"})
    # Timestamp of creation
    created_on: Optional[int] = _field(default=None, metadata={"alias": "createdOn"})
    # Description of the  Group.
    description: Optional[str] = _field(default=None)
    devices: Optional[List[str]] = _field(default=None)
    full_config_cli: Optional[bool] = _field(default=None, metadata={"alias": "fullConfigCli"})
    # System generated unique identifier of the  Group in UUID format.
    id: Optional[str] = _field(default=None)
    ios_config_cli: Optional[bool] = _field(default=None, metadata={"alias": "iosConfigCli"})
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
    topology: Optional[Topology] = _field(default=None)
    version_increment_reason: Optional[str] = _field(
        default=None, metadata={"alias": "versionIncrementReason"}
    )


@dataclass
class ProfileObjDef:
    id: str
    profile_type: ProfileType = _field(
        metadata={"alias": "profileType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class CreateConfigGroupPostResponse:
    """
    Config Group POST Response schema
    """

    id: str
    # (Optional - only applicable for AON) List of profile ids that belongs to the config group
    profiles: Optional[List[ProfileObjDef]] = _field(default=None)


@dataclass
class Criteria_1:
    attribute: Attribute  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class UnsupportedFeatures:
    parcel_id: str = _field(metadata={"alias": "parcelId"})
    parcel_type: UnsupportedFeaturesEnumDef = _field(
        metadata={"alias": "parcelType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class TopologyDevicePropertiesDef:
    criteria: Criteria_1
    unsupported_features: Optional[List[UnsupportedFeatures]] = _field(
        default=None, metadata={"alias": "unsupportedFeatures"}
    )


@dataclass
class TopologyDef:
    # list of devices in a site
    devices: List[TopologyDevicePropertiesDef]
    site_devices: Optional[int] = _field(default=None, metadata={"alias": "siteDevices"})


@dataclass
class ProfileIdObjDef:
    id: str


@dataclass
class FromConfigGroupDef:
    copy: str


@dataclass
class CreateConfigGroupPostRequest:
    """
    Config Group POST Request schema
    """

    description: str
    name: str
    solution: SolutionDef  # pytype: disable=annotation-type-mismatch
    from_config_group: Optional[FromConfigGroupDef] = _field(
        default=None, metadata={"alias": "fromConfigGroup"}
    )
    # list of profile ids that belongs to the config group
    profiles: Optional[List[ProfileIdObjDef]] = _field(default=None)
    source: Optional[Source] = _field(default=None)
    topology: Optional[TopologyDef] = _field(default=None)


@dataclass
class ConfigGroupProfileObjDef:
    id: str
    profile_type: ProfileType = _field(
        metadata={"alias": "profileType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class EditConfigGroupPutResponse:
    """
    Config Group PUT Response schema
    """

    id: str
    # (Optional - only applicable for AON) List of profile ids that belongs to the config group
    profiles: Optional[List[ConfigGroupProfileObjDef]] = _field(default=None)


@dataclass
class ConfigGroupTopologyDevicePropertiesDef:
    criteria: Criteria_1
    unsupported_features: Optional[List[UnsupportedFeatures]] = _field(
        default=None, metadata={"alias": "unsupportedFeatures"}
    )


@dataclass
class ConfigGroupTopologyDef:
    # list of devices in a site
    devices: List[ConfigGroupTopologyDevicePropertiesDef]
    site_devices: Optional[int] = _field(default=None, metadata={"alias": "siteDevices"})


@dataclass
class ConfigGroupProfileIdObjDef:
    id: str


@dataclass
class EditConfigGroupPutRequest:
    """
    Config Group PUT Request schema
    """

    description: str
    name: str
    solution: SolutionDef  # pytype: disable=annotation-type-mismatch
    # list of profile ids that belongs to the config group
    profiles: Optional[List[ConfigGroupProfileIdObjDef]] = _field(default=None)
    topology: Optional[ConfigGroupTopologyDef] = _field(default=None)
