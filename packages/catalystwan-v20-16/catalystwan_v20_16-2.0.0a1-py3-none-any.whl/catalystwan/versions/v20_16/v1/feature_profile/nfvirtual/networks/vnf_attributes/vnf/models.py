# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

DeploymentDatastoreDef = Literal["datastore1", "datastore2", "datastore3"]

VariableOptionTypeDef = Literal["variable"]

ModeDef = Literal["access", "trunk"]

VnfDeploymentDatastoreDef = Literal["datastore1", "datastore2", "datastore3"]

VnfModeDef = Literal["access", "trunk"]

VnfAttributesVnfDeploymentDatastoreDef = Literal["datastore1", "datastore2", "datastore3"]

VnfAttributesVnfModeDef = Literal["access", "trunk"]


@dataclass
class CreateNfvirtualVnfParcelPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class OneOfNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfImageOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfBootupTimeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfDeploymentDatastoreOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DeploymentDatastoreDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfVcpusOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfVcpusOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfMemoryMbOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfMemoryMbOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfRootDiskMbOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfRootDiskMbOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfDayZeroMountPointOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfDayZeroDayZeroFileContentOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfDayZeroCustomPropertyNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfDayZeroCustomPropertyValOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfDayZeroCustomPropertyValOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfDayZeroCustomPropertyEncryptedValOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfDayZeroCustomPropertyEncryptedValOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class CustomProperty:
    encrypted_val: Optional[
        Union[
            OneOfDayZeroCustomPropertyEncryptedValOptionsDef1,
            OneOfDayZeroCustomPropertyEncryptedValOptionsDef2,
        ]
    ] = _field(default=None)
    name: Optional[OneOfDayZeroCustomPropertyNameOptionsDef] = _field(default=None)
    val: Optional[
        Union[OneOfDayZeroCustomPropertyValOptionsDef1, OneOfDayZeroCustomPropertyValOptionsDef2]
    ] = _field(default=None)


@dataclass
class DayZero:
    day_zero_file_content: OneOfDayZeroDayZeroFileContentOptionsDef = _field(
        metadata={"alias": "dayZeroFileContent"}
    )
    mount_point: OneOfDayZeroMountPointOptionsDef
    # custom property
    custom_property: Optional[List[CustomProperty]] = _field(
        default=None, metadata={"alias": "customProperty"}
    )


@dataclass
class OneOfInterfacesNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfInterfacesNameOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfacesNicidOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfInterfacesNicidOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfacesSriovOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfInterfacesSriovOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfModeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ModeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfModeOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfVlanOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfVlanOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class Interfaces:
    mode: Optional[Union[OneOfModeOptionsDef1, OneOfModeOptionsDef2]] = _field(default=None)
    name: Optional[Union[OneOfInterfacesNameOptionsDef1, OneOfInterfacesNameOptionsDef2]] = _field(
        default=None
    )
    nicid: Optional[Union[OneOfInterfacesNicidOptionsDef1, OneOfInterfacesNicidOptionsDef2]] = (
        _field(default=None)
    )
    sriov: Optional[Union[OneOfInterfacesSriovOptionsDef1, OneOfInterfacesSriovOptionsDef2]] = (
        _field(default=None)
    )
    vlan: Optional[Union[OneOfVlanOptionsDef1, OneOfVlanOptionsDef2]] = _field(default=None)


@dataclass
class OneOfAdditionalDisksDiskSizeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfAdditionalDisksMountPathOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfAdditionalDisksMountPathOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class AdditionalDisks:
    disk_size: OneOfAdditionalDisksDiskSizeOptionsDef
    mount_path: Optional[
        Union[OneOfAdditionalDisksMountPathOptionsDef1, OneOfAdditionalDisksMountPathOptionsDef2]
    ] = _field(default=None)


@dataclass
class Data:
    image: OneOfImageOptionsDef
    memory_mb: Union[OneOfMemoryMbOptionsDef1, OneOfMemoryMbOptionsDef2]
    name: OneOfNameOptionsDef
    vcpus: Union[OneOfVcpusOptionsDef1, OneOfVcpusOptionsDef2]
    # Additional disks
    additional_disks: Optional[List[AdditionalDisks]] = _field(
        default=None, metadata={"alias": "additionalDisks"}
    )
    bootup_time: Optional[OneOfBootupTimeOptionsDef] = _field(default=None)
    # DayZero file
    day_zero: Optional[List[DayZero]] = _field(default=None, metadata={"alias": "dayZero"})
    deployment_datastore: Optional[OneOfDeploymentDatastoreOptionsDef] = _field(default=None)
    # Interface name
    interfaces: Optional[List[Interfaces]] = _field(default=None)
    root_disk_mb: Optional[Union[OneOfRootDiskMbOptionsDef1, OneOfRootDiskMbOptionsDef2]] = _field(
        default=None
    )


@dataclass
class CreateNfvirtualVnfParcelPostRequest:
    """
    VNF profile parcel schema for POST request
    """

    data: Data
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class VnfOneOfNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VnfOneOfImageOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VnfOneOfBootupTimeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VnfOneOfDeploymentDatastoreOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: VnfDeploymentDatastoreDef  # pytype: disable=annotation-type-mismatch


@dataclass
class VnfOneOfVcpusOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VnfOneOfMemoryMbOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VnfOneOfRootDiskMbOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VnfOneOfDayZeroMountPointOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VnfOneOfDayZeroDayZeroFileContentOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VnfOneOfDayZeroCustomPropertyNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VnfOneOfDayZeroCustomPropertyValOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VnfOneOfDayZeroCustomPropertyValOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VnfOneOfDayZeroCustomPropertyEncryptedValOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VnfOneOfDayZeroCustomPropertyEncryptedValOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VnfCustomProperty:
    encrypted_val: Optional[
        Union[
            VnfOneOfDayZeroCustomPropertyEncryptedValOptionsDef1,
            VnfOneOfDayZeroCustomPropertyEncryptedValOptionsDef2,
        ]
    ] = _field(default=None)
    name: Optional[VnfOneOfDayZeroCustomPropertyNameOptionsDef] = _field(default=None)
    val: Optional[
        Union[
            VnfOneOfDayZeroCustomPropertyValOptionsDef1, VnfOneOfDayZeroCustomPropertyValOptionsDef2
        ]
    ] = _field(default=None)


@dataclass
class VnfDayZero:
    day_zero_file_content: VnfOneOfDayZeroDayZeroFileContentOptionsDef = _field(
        metadata={"alias": "dayZeroFileContent"}
    )
    mount_point: VnfOneOfDayZeroMountPointOptionsDef
    # custom property
    custom_property: Optional[List[VnfCustomProperty]] = _field(
        default=None, metadata={"alias": "customProperty"}
    )


@dataclass
class VnfOneOfInterfacesNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VnfOneOfInterfacesNicidOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VnfOneOfModeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: VnfModeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class VnfOneOfVlanOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VnfInterfaces:
    mode: Optional[Union[VnfOneOfModeOptionsDef1, OneOfModeOptionsDef2]] = _field(default=None)
    name: Optional[Union[VnfOneOfInterfacesNameOptionsDef1, OneOfInterfacesNameOptionsDef2]] = (
        _field(default=None)
    )
    nicid: Optional[Union[VnfOneOfInterfacesNicidOptionsDef1, OneOfInterfacesNicidOptionsDef2]] = (
        _field(default=None)
    )
    sriov: Optional[Union[OneOfInterfacesSriovOptionsDef1, OneOfInterfacesSriovOptionsDef2]] = (
        _field(default=None)
    )
    vlan: Optional[Union[VnfOneOfVlanOptionsDef1, OneOfVlanOptionsDef2]] = _field(default=None)


@dataclass
class VnfOneOfAdditionalDisksDiskSizeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VnfOneOfAdditionalDisksMountPathOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VnfAdditionalDisks:
    disk_size: VnfOneOfAdditionalDisksDiskSizeOptionsDef
    mount_path: Optional[
        Union[VnfOneOfAdditionalDisksMountPathOptionsDef1, OneOfAdditionalDisksMountPathOptionsDef2]
    ] = _field(default=None)


@dataclass
class VnfData:
    image: VnfOneOfImageOptionsDef
    memory_mb: Union[VnfOneOfMemoryMbOptionsDef1, OneOfMemoryMbOptionsDef2]
    name: VnfOneOfNameOptionsDef
    vcpus: Union[VnfOneOfVcpusOptionsDef1, OneOfVcpusOptionsDef2]
    # Additional disks
    additional_disks: Optional[List[VnfAdditionalDisks]] = _field(
        default=None, metadata={"alias": "additionalDisks"}
    )
    bootup_time: Optional[VnfOneOfBootupTimeOptionsDef] = _field(default=None)
    # DayZero file
    day_zero: Optional[List[VnfDayZero]] = _field(default=None, metadata={"alias": "dayZero"})
    deployment_datastore: Optional[VnfOneOfDeploymentDatastoreOptionsDef] = _field(default=None)
    # Interface name
    interfaces: Optional[List[VnfInterfaces]] = _field(default=None)
    root_disk_mb: Optional[Union[VnfOneOfRootDiskMbOptionsDef1, OneOfRootDiskMbOptionsDef2]] = (
        _field(default=None)
    )


@dataclass
class Payload:
    """
    VNF profile parcel schema for PUT request
    """

    data: VnfData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class GetSingleNfvirtualNetworksVnfAttributesVnfPayload:
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
    # VNF profile parcel schema for PUT request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class EditNfvirtualVnfParcelPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class VnfAttributesVnfOneOfNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VnfAttributesVnfOneOfImageOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VnfAttributesVnfOneOfBootupTimeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VnfAttributesVnfOneOfDeploymentDatastoreOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: VnfAttributesVnfDeploymentDatastoreDef  # pytype: disable=annotation-type-mismatch


@dataclass
class VnfAttributesVnfOneOfVcpusOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VnfAttributesVnfOneOfMemoryMbOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VnfAttributesVnfOneOfRootDiskMbOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VnfAttributesVnfOneOfDayZeroMountPointOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VnfAttributesVnfOneOfDayZeroDayZeroFileContentOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VnfAttributesVnfOneOfDayZeroCustomPropertyNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VnfAttributesVnfOneOfDayZeroCustomPropertyValOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VnfAttributesVnfOneOfDayZeroCustomPropertyValOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VnfAttributesVnfOneOfDayZeroCustomPropertyEncryptedValOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VnfAttributesVnfOneOfDayZeroCustomPropertyEncryptedValOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VnfAttributesVnfCustomProperty:
    encrypted_val: Optional[
        Union[
            VnfAttributesVnfOneOfDayZeroCustomPropertyEncryptedValOptionsDef1,
            VnfAttributesVnfOneOfDayZeroCustomPropertyEncryptedValOptionsDef2,
        ]
    ] = _field(default=None)
    name: Optional[VnfAttributesVnfOneOfDayZeroCustomPropertyNameOptionsDef] = _field(default=None)
    val: Optional[
        Union[
            VnfAttributesVnfOneOfDayZeroCustomPropertyValOptionsDef1,
            VnfAttributesVnfOneOfDayZeroCustomPropertyValOptionsDef2,
        ]
    ] = _field(default=None)


@dataclass
class VnfAttributesVnfDayZero:
    day_zero_file_content: VnfAttributesVnfOneOfDayZeroDayZeroFileContentOptionsDef = _field(
        metadata={"alias": "dayZeroFileContent"}
    )
    mount_point: VnfAttributesVnfOneOfDayZeroMountPointOptionsDef
    # custom property
    custom_property: Optional[List[VnfAttributesVnfCustomProperty]] = _field(
        default=None, metadata={"alias": "customProperty"}
    )


@dataclass
class VnfAttributesVnfOneOfInterfacesNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VnfAttributesVnfOneOfInterfacesNicidOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VnfAttributesVnfOneOfModeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: VnfAttributesVnfModeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class VnfAttributesVnfOneOfVlanOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VnfAttributesVnfInterfaces:
    mode: Optional[Union[VnfAttributesVnfOneOfModeOptionsDef1, OneOfModeOptionsDef2]] = _field(
        default=None
    )
    name: Optional[
        Union[VnfAttributesVnfOneOfInterfacesNameOptionsDef1, OneOfInterfacesNameOptionsDef2]
    ] = _field(default=None)
    nicid: Optional[
        Union[VnfAttributesVnfOneOfInterfacesNicidOptionsDef1, OneOfInterfacesNicidOptionsDef2]
    ] = _field(default=None)
    sriov: Optional[Union[OneOfInterfacesSriovOptionsDef1, OneOfInterfacesSriovOptionsDef2]] = (
        _field(default=None)
    )
    vlan: Optional[Union[VnfAttributesVnfOneOfVlanOptionsDef1, OneOfVlanOptionsDef2]] = _field(
        default=None
    )


@dataclass
class VnfAttributesVnfOneOfAdditionalDisksDiskSizeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class VnfAttributesVnfOneOfAdditionalDisksMountPathOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class VnfAttributesVnfAdditionalDisks:
    disk_size: VnfAttributesVnfOneOfAdditionalDisksDiskSizeOptionsDef
    mount_path: Optional[
        Union[
            VnfAttributesVnfOneOfAdditionalDisksMountPathOptionsDef1,
            OneOfAdditionalDisksMountPathOptionsDef2,
        ]
    ] = _field(default=None)


@dataclass
class VnfAttributesVnfData:
    image: VnfAttributesVnfOneOfImageOptionsDef
    memory_mb: Union[VnfAttributesVnfOneOfMemoryMbOptionsDef1, OneOfMemoryMbOptionsDef2]
    name: VnfAttributesVnfOneOfNameOptionsDef
    vcpus: Union[VnfAttributesVnfOneOfVcpusOptionsDef1, OneOfVcpusOptionsDef2]
    # Additional disks
    additional_disks: Optional[List[VnfAttributesVnfAdditionalDisks]] = _field(
        default=None, metadata={"alias": "additionalDisks"}
    )
    bootup_time: Optional[VnfAttributesVnfOneOfBootupTimeOptionsDef] = _field(default=None)
    # DayZero file
    day_zero: Optional[List[VnfAttributesVnfDayZero]] = _field(
        default=None, metadata={"alias": "dayZero"}
    )
    deployment_datastore: Optional[VnfAttributesVnfOneOfDeploymentDatastoreOptionsDef] = _field(
        default=None
    )
    # Interface name
    interfaces: Optional[List[VnfAttributesVnfInterfaces]] = _field(default=None)
    root_disk_mb: Optional[
        Union[VnfAttributesVnfOneOfRootDiskMbOptionsDef1, OneOfRootDiskMbOptionsDef2]
    ] = _field(default=None)


@dataclass
class EditNfvirtualVnfParcelPutRequest:
    """
    VNF profile parcel schema for PUT request
    """

    data: VnfAttributesVnfData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)
