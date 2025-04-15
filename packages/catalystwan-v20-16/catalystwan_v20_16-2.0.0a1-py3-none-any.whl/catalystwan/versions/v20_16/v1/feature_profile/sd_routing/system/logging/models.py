# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

VariableOptionTypeDef = Literal["variable"]

GlobalOptionTypeDef = Literal["global"]

DefaultOptionTypeDef = Literal["default"]

TlsVersionDef = Literal["TLSv1.1", "TLSv1.2"]

Value = Literal["TLSv1.1"]

LoggingValue = Literal["Server"]

CipherSuiteListDef = Literal[
    "aes-128-cbc-sha",
    "aes-256-cbc-sha",
    "dhe-aes-cbc-sha2",
    "dhe-aes-gcm-sha2",
    "ecdhe-ecdsa-aes-gcm-sha2",
    "ecdhe-rsa-aes-cbc-sha2",
    "ecdhe-rsa-aes-gcm-sha2",
    "rsa-aes-cbc-sha2",
    "rsa-aes-gcm-sha2",
]

PrioritytDef = Literal[
    "alert", "critical", "debugging", "emergency", "error", "informational", "notice", "warn"
]

SystemLoggingValue = Literal["informational"]


@dataclass
class OneOfDiskEnableOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfDiskEnableOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfDiskEnableOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfDiskFileSizeOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfDiskFileSizeOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfDiskFileSizeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfDiskFileRotateOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfDiskFileRotateOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfDiskFileRotateOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class File:
    disk_file_rotate: Union[
        OneOfDiskFileRotateOptionsDef1,
        OneOfDiskFileRotateOptionsDef2,
        OneOfDiskFileRotateOptionsDef3,
    ] = _field(metadata={"alias": "diskFileRotate"})
    disk_file_size: Union[
        OneOfDiskFileSizeOptionsDef1, OneOfDiskFileSizeOptionsDef2, OneOfDiskFileSizeOptionsDef3
    ] = _field(metadata={"alias": "diskFileSize"})


@dataclass
class Disk:
    file: File
    disk_enable: Optional[
        Union[OneOfDiskEnableOptionsDef1, OneOfDiskEnableOptionsDef2, OneOfDiskEnableOptionsDef3]
    ] = _field(default=None, metadata={"alias": "diskEnable"})


@dataclass
class OneOfProfileOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfProfileOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfTlsVersionOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTlsVersionOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: TlsVersionDef


@dataclass
class OneOfTlsVersionOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Value  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfAuthTypeOptionsDef:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: LoggingValue  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfCipherSuiteListOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfCipherSuiteListOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[CipherSuiteListDef]  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfCipherSuiteListOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class TlsProfile:
    auth_type: OneOfAuthTypeOptionsDef = _field(metadata={"alias": "authType"})
    profile: Union[OneOfProfileOptionsDef1, OneOfProfileOptionsDef2]
    cipher_suite_list: Optional[
        Union[
            OneOfCipherSuiteListOptionsDef1,
            OneOfCipherSuiteListOptionsDef2,
            OneOfCipherSuiteListOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "cipherSuiteList"})
    tls_version: Optional[
        Union[OneOfTlsVersionOptionsDef1, OneOfTlsVersionOptionsDef2, OneOfTlsVersionOptionsDef3]
    ] = _field(default=None, metadata={"alias": "tlsVersion"})


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
class OneOfVrfOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfVrfOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfVrfOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfSourceInterfaceOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfSourceInterfaceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfSourceInterfaceOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfPriorityOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfPriorityOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: PrioritytDef


@dataclass
class OneOfPriorityOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SystemLoggingValue  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfTlsEnableOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTlsEnableOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfTlsEnableOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfTlsPropCustomProfileOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTlsPropCustomProfileOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfTlsPropCustomProfileOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfTlsPropProfileOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTlsPropProfileOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfTlsPropProfileOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class Server:
    name: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2]
    priority: Union[OneOfPriorityOptionsDef1, OneOfPriorityOptionsDef2, OneOfPriorityOptionsDef3]
    tls_enable: Union[
        OneOfTlsEnableOptionsDef1, OneOfTlsEnableOptionsDef2, OneOfTlsEnableOptionsDef3
    ] = _field(metadata={"alias": "tlsEnable"})
    vrf: Union[OneOfVrfOptionsDef1, OneOfVrfOptionsDef2, OneOfVrfOptionsDef3]
    source_interface: Optional[
        Union[
            OneOfSourceInterfaceOptionsDef1,
            OneOfSourceInterfaceOptionsDef2,
            OneOfSourceInterfaceOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sourceInterface"})
    tls_properties_custom_profile: Optional[
        Union[
            OneOfTlsPropCustomProfileOptionsDef1,
            OneOfTlsPropCustomProfileOptionsDef2,
            OneOfTlsPropCustomProfileOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tlsPropertiesCustomProfile"})
    tls_properties_profile: Optional[
        Union[
            OneOfTlsPropProfileOptionsDef1,
            OneOfTlsPropProfileOptionsDef2,
            OneOfTlsPropProfileOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tlsPropertiesProfile"})


@dataclass
class OneOfIpv6AddrGlobalVariableOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfIpv6AddrGlobalVariableOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class Ipv6Server:
    name: Union[OneOfIpv6AddrGlobalVariableOptionsDef1, OneOfIpv6AddrGlobalVariableOptionsDef2]
    priority: Union[OneOfPriorityOptionsDef1, OneOfPriorityOptionsDef2, OneOfPriorityOptionsDef3]
    tls_enable: Union[
        OneOfTlsEnableOptionsDef1, OneOfTlsEnableOptionsDef2, OneOfTlsEnableOptionsDef3
    ] = _field(metadata={"alias": "tlsEnable"})
    vrf: Union[OneOfVrfOptionsDef1, OneOfVrfOptionsDef2, OneOfVrfOptionsDef3]
    source_interface: Optional[
        Union[
            OneOfSourceInterfaceOptionsDef1,
            OneOfSourceInterfaceOptionsDef2,
            OneOfSourceInterfaceOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sourceInterface"})
    tls_properties_custom_profile: Optional[
        Union[
            OneOfTlsPropCustomProfileOptionsDef1,
            OneOfTlsPropCustomProfileOptionsDef2,
            OneOfTlsPropCustomProfileOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tlsPropertiesCustomProfile"})
    tls_properties_profile: Optional[
        Union[
            OneOfTlsPropProfileOptionsDef1,
            OneOfTlsPropProfileOptionsDef2,
            OneOfTlsPropProfileOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tlsPropertiesProfile"})


@dataclass
class LoggingData:
    disk: Disk
    # Enable logging to remote ipv6 server
    ipv6_server: Optional[List[Ipv6Server]] = _field(default=None, metadata={"alias": "ipv6Server"})
    # Enable logging to remote server
    server: Optional[List[Server]] = _field(default=None)
    # Configure a TLS profile
    tls_profile: Optional[List[TlsProfile]] = _field(default=None, metadata={"alias": "tlsProfile"})


@dataclass
class Payload:
    """
    SD-Routing logging feature schema
    """

    data: LoggingData
    name: str
    # Set the feature description
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
    # SD-Routing logging feature schema
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdRoutingSystemLoggingSdRoutingPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateSdroutingLoggingFeaturePostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SystemLoggingData:
    disk: Disk
    # Enable logging to remote ipv6 server
    ipv6_server: Optional[List[Ipv6Server]] = _field(default=None, metadata={"alias": "ipv6Server"})
    # Enable logging to remote server
    server: Optional[List[Server]] = _field(default=None)
    # Configure a TLS profile
    tls_profile: Optional[List[TlsProfile]] = _field(default=None, metadata={"alias": "tlsProfile"})


@dataclass
class CreateSdroutingLoggingFeaturePostRequest:
    """
    SD-Routing logging feature schema
    """

    data: SystemLoggingData
    name: str
    # Set the feature description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetSingleSdRoutingSystemLoggingSdRoutingPayload:
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
    # SD-Routing logging feature schema
    payload: Optional[Payload] = _field(default=None)


@dataclass
class EditSdroutingLoggingFeaturePutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SdRoutingSystemLoggingData:
    disk: Disk
    # Enable logging to remote ipv6 server
    ipv6_server: Optional[List[Ipv6Server]] = _field(default=None, metadata={"alias": "ipv6Server"})
    # Enable logging to remote server
    server: Optional[List[Server]] = _field(default=None)
    # Configure a TLS profile
    tls_profile: Optional[List[TlsProfile]] = _field(default=None, metadata={"alias": "tlsProfile"})


@dataclass
class EditSdroutingLoggingFeaturePutRequest:
    """
    SD-Routing logging feature schema
    """

    data: SdRoutingSystemLoggingData
    name: str
    # Set the feature description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
