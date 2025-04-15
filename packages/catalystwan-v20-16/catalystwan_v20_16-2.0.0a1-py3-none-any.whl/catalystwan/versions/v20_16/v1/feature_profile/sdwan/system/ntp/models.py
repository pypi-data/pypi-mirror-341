# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

VariableOptionTypeDef = Literal["variable"]

GlobalOptionTypeDef = Literal["global"]

DefaultOptionTypeDef = Literal["default"]


@dataclass
class OneOfServerNameOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfServerNameOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfServerKeyOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfServerKeyOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfServerKeyOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfVpnOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfVpnOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfVpnOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfVersionOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfVersionOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfVersionOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


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
class OneOfPreferOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfPreferOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfPreferOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class Server:
    name: Union[OneOfServerNameOptionsDef1, OneOfServerNameOptionsDef2]
    prefer: Union[OneOfPreferOptionsDef1, OneOfPreferOptionsDef2, OneOfPreferOptionsDef3]
    version: Union[OneOfVersionOptionsDef1, OneOfVersionOptionsDef2, OneOfVersionOptionsDef3]
    vpn: Union[OneOfVpnOptionsDef1, OneOfVpnOptionsDef2, OneOfVpnOptionsDef3]
    key: Optional[
        Union[OneOfServerKeyOptionsDef1, OneOfServerKeyOptionsDef2, OneOfServerKeyOptionsDef3]
    ] = _field(default=None)
    source_interface: Optional[
        Union[
            OneOfSourceInterfaceOptionsDef1,
            OneOfSourceInterfaceOptionsDef2,
            OneOfSourceInterfaceOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sourceInterface"})


@dataclass
class OneOfAuthKeyIdOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAuthKeyIdOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfAuthKeyMd5ValueOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAuthKeyMd5ValueOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class AuthenticationKeys:
    key_id: Union[OneOfAuthKeyIdOptionsDef1, OneOfAuthKeyIdOptionsDef2] = _field(
        metadata={"alias": "keyId"}
    )
    md5_value: Union[OneOfAuthKeyMd5ValueOptionsDef1, OneOfAuthKeyMd5ValueOptionsDef2] = _field(
        metadata={"alias": "md5Value"}
    )


@dataclass
class OneOfTrustedKeyIdOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTrustedKeyIdOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[int]


@dataclass
class OneOfTrustedKeyIdOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class Authentication:
    # Set MD5 authentication key
    authentication_keys: List[AuthenticationKeys] = _field(metadata={"alias": "authenticationKeys"})
    trusted_keys: Optional[
        Union[
            OneOfTrustedKeyIdOptionsDef1, OneOfTrustedKeyIdOptionsDef2, OneOfTrustedKeyIdOptionsDef3
        ]
    ] = _field(default=None, metadata={"alias": "trustedKeys"})


@dataclass
class OneOfLeaderEnableOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfLeaderEnableOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfLeaderEnableOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfLeaderStratumOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfLeaderStratumOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfLeaderStratumOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfLeaderSourceOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfLeaderSourceOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfLeaderSourceOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class Leader:
    enable: Optional[
        Union[
            OneOfLeaderEnableOptionsDef1, OneOfLeaderEnableOptionsDef2, OneOfLeaderEnableOptionsDef3
        ]
    ] = _field(default=None)
    source: Optional[
        Union[
            OneOfLeaderSourceOptionsDef1, OneOfLeaderSourceOptionsDef2, OneOfLeaderSourceOptionsDef3
        ]
    ] = _field(default=None)
    stratum: Optional[
        Union[
            OneOfLeaderStratumOptionsDef1,
            OneOfLeaderStratumOptionsDef2,
            OneOfLeaderStratumOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class NtpData:
    # Configure NTP servers
    server: List[Server]
    authentication: Optional[Authentication] = _field(default=None)
    leader: Optional[Leader] = _field(default=None)


@dataclass
class Payload:
    """
    NTP profile parcel schema for POST request
    """

    data: NtpData
    name: str
    # Set the parcel description
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
    # NTP profile parcel schema for POST request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdwanSystemNtpPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateNtpProfileParcelForSystemPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SystemNtpData:
    # Configure NTP servers
    server: List[Server]
    authentication: Optional[Authentication] = _field(default=None)
    leader: Optional[Leader] = _field(default=None)


@dataclass
class CreateNtpProfileParcelForSystemPostRequest:
    """
    NTP profile parcel schema for POST request
    """

    data: SystemNtpData
    name: str
    # Set the parcel description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class NtpOneOfServerNameOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class NtpOneOfServerKeyOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class NtpOneOfVpnOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class NtpOneOfVersionOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class NtpServer:
    name: Union[OneOfServerNameOptionsDef1, NtpOneOfServerNameOptionsDef2]
    prefer: Union[OneOfPreferOptionsDef1, OneOfPreferOptionsDef2, OneOfPreferOptionsDef3]
    version: Union[OneOfVersionOptionsDef1, NtpOneOfVersionOptionsDef2, OneOfVersionOptionsDef3]
    vpn: Union[OneOfVpnOptionsDef1, NtpOneOfVpnOptionsDef2, OneOfVpnOptionsDef3]
    key: Optional[
        Union[OneOfServerKeyOptionsDef1, NtpOneOfServerKeyOptionsDef2, OneOfServerKeyOptionsDef3]
    ] = _field(default=None)
    source_interface: Optional[
        Union[
            OneOfSourceInterfaceOptionsDef1,
            OneOfSourceInterfaceOptionsDef2,
            OneOfSourceInterfaceOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sourceInterface"})


@dataclass
class NtpOneOfAuthKeyIdOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class NtpOneOfAuthKeyMd5ValueOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class NtpAuthenticationKeys:
    key_id: Union[OneOfAuthKeyIdOptionsDef1, NtpOneOfAuthKeyIdOptionsDef2] = _field(
        metadata={"alias": "keyId"}
    )
    md5_value: Union[OneOfAuthKeyMd5ValueOptionsDef1, NtpOneOfAuthKeyMd5ValueOptionsDef2] = _field(
        metadata={"alias": "md5Value"}
    )


@dataclass
class NtpOneOfTrustedKeyIdOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[int]


@dataclass
class NtpAuthentication:
    # Set MD5 authentication key
    authentication_keys: List[NtpAuthenticationKeys] = _field(
        metadata={"alias": "authenticationKeys"}
    )
    trusted_keys: Optional[
        Union[
            OneOfTrustedKeyIdOptionsDef1,
            NtpOneOfTrustedKeyIdOptionsDef2,
            OneOfTrustedKeyIdOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "trustedKeys"})


@dataclass
class NtpOneOfLeaderStratumOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class NtpLeader:
    enable: Optional[
        Union[
            OneOfLeaderEnableOptionsDef1, OneOfLeaderEnableOptionsDef2, OneOfLeaderEnableOptionsDef3
        ]
    ] = _field(default=None)
    source: Optional[
        Union[
            OneOfLeaderSourceOptionsDef1, OneOfLeaderSourceOptionsDef2, OneOfLeaderSourceOptionsDef3
        ]
    ] = _field(default=None)
    stratum: Optional[
        Union[
            OneOfLeaderStratumOptionsDef1,
            NtpOneOfLeaderStratumOptionsDef2,
            OneOfLeaderStratumOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class SdwanSystemNtpData:
    # Configure NTP servers
    server: List[NtpServer]
    authentication: Optional[NtpAuthentication] = _field(default=None)
    leader: Optional[NtpLeader] = _field(default=None)


@dataclass
class NtpPayload:
    """
    NTP profile parcel schema for PUT request
    """

    data: SdwanSystemNtpData
    name: str
    # Set the parcel description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetSingleSdwanSystemNtpPayload:
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
    # NTP profile parcel schema for PUT request
    payload: Optional[NtpPayload] = _field(default=None)


@dataclass
class EditNtpProfileParcelForSystemPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SystemNtpOneOfServerNameOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SystemNtpOneOfServerKeyOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemNtpOneOfVpnOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemNtpOneOfVersionOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemNtpServer:
    name: Union[OneOfServerNameOptionsDef1, SystemNtpOneOfServerNameOptionsDef2]
    prefer: Union[OneOfPreferOptionsDef1, OneOfPreferOptionsDef2, OneOfPreferOptionsDef3]
    version: Union[
        OneOfVersionOptionsDef1, SystemNtpOneOfVersionOptionsDef2, OneOfVersionOptionsDef3
    ]
    vpn: Union[OneOfVpnOptionsDef1, SystemNtpOneOfVpnOptionsDef2, OneOfVpnOptionsDef3]
    key: Optional[
        Union[
            OneOfServerKeyOptionsDef1, SystemNtpOneOfServerKeyOptionsDef2, OneOfServerKeyOptionsDef3
        ]
    ] = _field(default=None)
    source_interface: Optional[
        Union[
            OneOfSourceInterfaceOptionsDef1,
            OneOfSourceInterfaceOptionsDef2,
            OneOfSourceInterfaceOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sourceInterface"})


@dataclass
class SystemNtpOneOfAuthKeyIdOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemNtpOneOfAuthKeyMd5ValueOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SystemNtpAuthenticationKeys:
    key_id: Union[OneOfAuthKeyIdOptionsDef1, SystemNtpOneOfAuthKeyIdOptionsDef2] = _field(
        metadata={"alias": "keyId"}
    )
    md5_value: Union[OneOfAuthKeyMd5ValueOptionsDef1, SystemNtpOneOfAuthKeyMd5ValueOptionsDef2] = (
        _field(metadata={"alias": "md5Value"})
    )


@dataclass
class SystemNtpOneOfTrustedKeyIdOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[int]


@dataclass
class SystemNtpAuthentication:
    # Set MD5 authentication key
    authentication_keys: List[SystemNtpAuthenticationKeys] = _field(
        metadata={"alias": "authenticationKeys"}
    )
    trusted_keys: Optional[
        Union[
            OneOfTrustedKeyIdOptionsDef1,
            SystemNtpOneOfTrustedKeyIdOptionsDef2,
            OneOfTrustedKeyIdOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "trustedKeys"})


@dataclass
class SystemNtpOneOfLeaderStratumOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemNtpLeader:
    enable: Optional[
        Union[
            OneOfLeaderEnableOptionsDef1, OneOfLeaderEnableOptionsDef2, OneOfLeaderEnableOptionsDef3
        ]
    ] = _field(default=None)
    source: Optional[
        Union[
            OneOfLeaderSourceOptionsDef1, OneOfLeaderSourceOptionsDef2, OneOfLeaderSourceOptionsDef3
        ]
    ] = _field(default=None)
    stratum: Optional[
        Union[
            OneOfLeaderStratumOptionsDef1,
            SystemNtpOneOfLeaderStratumOptionsDef2,
            OneOfLeaderStratumOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class FeatureProfileSdwanSystemNtpData:
    # Configure NTP servers
    server: List[SystemNtpServer]
    authentication: Optional[SystemNtpAuthentication] = _field(default=None)
    leader: Optional[SystemNtpLeader] = _field(default=None)


@dataclass
class EditNtpProfileParcelForSystemPutRequest:
    """
    NTP profile parcel schema for PUT request
    """

    data: FeatureProfileSdwanSystemNtpData
    name: str
    # Set the parcel description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
