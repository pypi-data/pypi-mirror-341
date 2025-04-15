# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

VariableOptionTypeDef = Literal["variable"]

DefaultOptionTypeDef = Literal["default"]

RoleDef = Literal["border-router", "edge-router"]

EnableMrfMigrationDef = Literal["enabled", "enabled-from-bgp-core"]


@dataclass
class OneOfSecondaryRegionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfSecondaryRegionOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfSecondaryRegionOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfRoleOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: RoleDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfRoleOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfRoleOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfEnableMrfMigrationOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EnableMrfMigrationDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfEnableMrfMigrationOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfMigrationBgpCommunityOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfMigrationBgpCommunityOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfEnableManagemantRegionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfEnableManagemantRegionOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfEnableManagemantRegionOptionsDef3:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfVrfIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfVrfIdOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfVrfIdOptionsDef3:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfGatewayPreferenceOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[int]


@dataclass
class OneOfGatewayPreferenceOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfGatewayPreferenceOptionsDef3:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfManagementGatewayOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfManagementGatewayOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfManagementGatewayOptionsDef3:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class ManagementRegion:
    """
    Management Region
    """

    gateway_preference: Optional[
        Union[
            OneOfGatewayPreferenceOptionsDef1,
            OneOfGatewayPreferenceOptionsDef2,
            OneOfGatewayPreferenceOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "gatewayPreference"})
    management_gateway: Optional[
        Union[
            OneOfManagementGatewayOptionsDef1,
            OneOfManagementGatewayOptionsDef2,
            OneOfManagementGatewayOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "managementGateway"})
    vrf_id: Optional[Union[OneOfVrfIdOptionsDef1, OneOfVrfIdOptionsDef2, OneOfVrfIdOptionsDef3]] = (
        _field(default=None, metadata={"alias": "vrfId"})
    )


@dataclass
class MrfData:
    enable_management_region: Optional[
        Union[
            OneOfEnableManagemantRegionOptionsDef1,
            OneOfEnableManagemantRegionOptionsDef2,
            OneOfEnableManagemantRegionOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "enableManagementRegion"})
    enable_mrf_migration: Optional[
        Union[OneOfEnableMrfMigrationOptionsDef1, OneOfEnableMrfMigrationOptionsDef2]
    ] = _field(default=None, metadata={"alias": "enableMrfMigration"})
    # Management Region
    management_region: Optional[ManagementRegion] = _field(
        default=None, metadata={"alias": "managementRegion"}
    )
    migration_bgp_community: Optional[
        Union[OneOfMigrationBgpCommunityOptionsDef1, OneOfMigrationBgpCommunityOptionsDef2]
    ] = _field(default=None, metadata={"alias": "migrationBgpCommunity"})
    role: Optional[Union[OneOfRoleOptionsDef1, OneOfRoleOptionsDef2, OneOfRoleOptionsDef3]] = (
        _field(default=None)
    )
    secondary_region: Optional[
        Union[
            OneOfSecondaryRegionOptionsDef1,
            OneOfSecondaryRegionOptionsDef2,
            OneOfSecondaryRegionOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "secondaryRegion"})


@dataclass
class Payload:
    """
    mrf profile parcel schema for POST request
    """

    data: MrfData
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
    # mrf profile parcel schema for POST request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdwanSystemMrfPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateMrfProfileParcelForSystemPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SystemMrfData:
    enable_management_region: Optional[
        Union[
            OneOfEnableManagemantRegionOptionsDef1,
            OneOfEnableManagemantRegionOptionsDef2,
            OneOfEnableManagemantRegionOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "enableManagementRegion"})
    enable_mrf_migration: Optional[
        Union[OneOfEnableMrfMigrationOptionsDef1, OneOfEnableMrfMigrationOptionsDef2]
    ] = _field(default=None, metadata={"alias": "enableMrfMigration"})
    # Management Region
    management_region: Optional[ManagementRegion] = _field(
        default=None, metadata={"alias": "managementRegion"}
    )
    migration_bgp_community: Optional[
        Union[OneOfMigrationBgpCommunityOptionsDef1, OneOfMigrationBgpCommunityOptionsDef2]
    ] = _field(default=None, metadata={"alias": "migrationBgpCommunity"})
    role: Optional[Union[OneOfRoleOptionsDef1, OneOfRoleOptionsDef2, OneOfRoleOptionsDef3]] = (
        _field(default=None)
    )
    secondary_region: Optional[
        Union[
            OneOfSecondaryRegionOptionsDef1,
            OneOfSecondaryRegionOptionsDef2,
            OneOfSecondaryRegionOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "secondaryRegion"})


@dataclass
class CreateMrfProfileParcelForSystemPostRequest:
    """
    mrf profile parcel schema for POST request
    """

    data: SystemMrfData
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetSingleSdwanSystemMrfPayload:
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
    # mrf profile parcel schema for POST request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class EditMrfProfileParcelForSystemPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SdwanSystemMrfData:
    enable_management_region: Optional[
        Union[
            OneOfEnableManagemantRegionOptionsDef1,
            OneOfEnableManagemantRegionOptionsDef2,
            OneOfEnableManagemantRegionOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "enableManagementRegion"})
    enable_mrf_migration: Optional[
        Union[OneOfEnableMrfMigrationOptionsDef1, OneOfEnableMrfMigrationOptionsDef2]
    ] = _field(default=None, metadata={"alias": "enableMrfMigration"})
    # Management Region
    management_region: Optional[ManagementRegion] = _field(
        default=None, metadata={"alias": "managementRegion"}
    )
    migration_bgp_community: Optional[
        Union[OneOfMigrationBgpCommunityOptionsDef1, OneOfMigrationBgpCommunityOptionsDef2]
    ] = _field(default=None, metadata={"alias": "migrationBgpCommunity"})
    role: Optional[Union[OneOfRoleOptionsDef1, OneOfRoleOptionsDef2, OneOfRoleOptionsDef3]] = (
        _field(default=None)
    )
    secondary_region: Optional[
        Union[
            OneOfSecondaryRegionOptionsDef1,
            OneOfSecondaryRegionOptionsDef2,
            OneOfSecondaryRegionOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "secondaryRegion"})


@dataclass
class EditMrfProfileParcelForSystemPutRequest:
    """
    mrf profile parcel schema for POST request
    """

    data: SdwanSystemMrfData
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
