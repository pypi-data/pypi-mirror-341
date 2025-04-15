# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

GroupSecurityLevelDef = Literal["authNoPriv", "authPriv", "noAuthNoPriv"]

VariableOptionTypeDef = Literal["variable"]

DefaultOptionTypeDef = Literal["default"]

DefaultUserVersionDef = Literal["1"]

UserAuthProtocolDef = Literal["md5", "sha"]

UserPrivProtocolDef = Literal["aes", "des"]

HostHostSecurityLevelDef = Literal["authNoPriv", "authPriv", "noAuthNoPriv"]

SnmpGroupSecurityLevelDef = Literal["authNoPriv", "authPriv", "noAuthNoPriv"]

SnmpDefaultUserVersionDef = Literal["1"]

SnmpUserAuthProtocolDef = Literal["md5", "sha"]

SnmpUserPrivProtocolDef = Literal["aes", "des"]

SnmpHostHostSecurityLevelDef = Literal["authNoPriv", "authPriv", "noAuthNoPriv"]

SystemSnmpGroupSecurityLevelDef = Literal["authNoPriv", "authPriv", "noAuthNoPriv"]

SystemSnmpDefaultUserVersionDef = Literal["1"]

SystemSnmpUserAuthProtocolDef = Literal["md5", "sha"]

SystemSnmpUserPrivProtocolDef = Literal["aes", "des"]

SystemSnmpHostHostSecurityLevelDef = Literal["authNoPriv", "authPriv", "noAuthNoPriv"]


@dataclass
class CreateNfvirtualSnmpParcelPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class OneOfCommunityNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfCommunityCommunityAccessOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class Community:
    community_name: OneOfCommunityNameOptionsDef = _field(metadata={"alias": "communityName"})
    community_access: Optional[OneOfCommunityCommunityAccessOptionsDef] = _field(
        default=None, metadata={"alias": "communityAccess"}
    )


@dataclass
class OneOfGroupNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfGroupContextOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfGroupVersionOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfGroupSecurityLevelOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: GroupSecurityLevelDef


@dataclass
class OneOfGroupNotifyOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfGroupReadOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfGroupWriteOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class Group:
    context: OneOfGroupContextOptionsDef
    name: OneOfGroupNameOptionsDef
    security_level: OneOfGroupSecurityLevelOptionsDef = _field(metadata={"alias": "securityLevel"})
    notify: Optional[OneOfGroupNotifyOptionsDef] = _field(default=None)
    read: Optional[OneOfGroupReadOptionsDef] = _field(default=None)
    version: Optional[OneOfGroupVersionOptionsDef] = _field(default=None)
    write: Optional[OneOfGroupWriteOptionsDef] = _field(default=None)


@dataclass
class OneOfUserUserNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfUserVersionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfUserVersionOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfUserVersionOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Optional[DefaultUserVersionDef] = _field(default=None)


@dataclass
class OneOfUserUserGroupOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfUserAuthProtocolOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: UserAuthProtocolDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfUserAuthProtocolOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfUserPrivProtocolOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: UserPrivProtocolDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfUserPrivProtocolOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfUserPassphraseOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfUserPassphraseOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class User:
    user_group: OneOfUserUserGroupOptionsDef = _field(metadata={"alias": "userGroup"})
    user_name: OneOfUserUserNameOptionsDef = _field(metadata={"alias": "userName"})
    version: Union[
        OneOfUserVersionOptionsDef1, OneOfUserVersionOptionsDef2, OneOfUserVersionOptionsDef3
    ]
    auth_protocol: Optional[
        Union[OneOfUserAuthProtocolOptionsDef1, OneOfUserAuthProtocolOptionsDef2]
    ] = _field(default=None, metadata={"alias": "authProtocol"})
    passphrase: Optional[Union[OneOfUserPassphraseOptionsDef1, OneOfUserPassphraseOptionsDef2]] = (
        _field(default=None)
    )
    priv_protocol: Optional[
        Union[OneOfUserPrivProtocolOptionsDef1, OneOfUserPrivProtocolOptionsDef2]
    ] = _field(default=None, metadata={"alias": "privProtocol"})


@dataclass
class OneOfHostHostNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfHostHostNameOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfHostIpOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfHostIpOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfHostPortOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfHostHostUserNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfHostHostVersionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfHostHostVersionOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfHostHostSecurityLevelOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: HostHostSecurityLevelDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfHostHostSecurityLevelOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class Host:
    host_name: Union[OneOfHostHostNameOptionsDef1, OneOfHostHostNameOptionsDef2] = _field(
        metadata={"alias": "hostName"}
    )
    host_security_level: Union[
        OneOfHostHostSecurityLevelOptionsDef1, OneOfHostHostSecurityLevelOptionsDef2
    ] = _field(metadata={"alias": "hostSecurityLevel"})
    host_user_name: OneOfHostHostUserNameOptionsDef = _field(metadata={"alias": "hostUserName"})
    host_version: Union[OneOfHostHostVersionOptionsDef1, OneOfHostHostVersionOptionsDef2] = _field(
        metadata={"alias": "hostVersion"}
    )
    ip: Union[OneOfHostIpOptionsDef1, OneOfHostIpOptionsDef2]
    port: OneOfHostPortOptionsDef


@dataclass
class OneOfLinkUpOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfLinkUpOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfLinkDownOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfLinkDownOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class Data:
    # Configure SNMP community
    community: Optional[List[Community]] = _field(default=None)
    # Configure an SNMP group
    group: Optional[List[Group]] = _field(default=None)
    # Configure SNMP server to receive SNMP traps
    host: Optional[List[Host]] = _field(default=None)
    link_down: Optional[Union[OneOfLinkDownOptionsDef1, OneOfLinkDownOptionsDef2]] = _field(
        default=None, metadata={"alias": "linkDown"}
    )
    link_up: Optional[Union[OneOfLinkUpOptionsDef1, OneOfLinkUpOptionsDef2]] = _field(
        default=None, metadata={"alias": "linkUp"}
    )
    # Configure an SNMP user
    user: Optional[List[User]] = _field(default=None)


@dataclass
class CreateNfvirtualSnmpParcelPostRequest:
    """
    SNMP profile parcel schema for POST request
    """

    data: Data
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class SnmpOneOfCommunityNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SnmpOneOfCommunityCommunityAccessOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SnmpCommunity:
    community_name: SnmpOneOfCommunityNameOptionsDef = _field(metadata={"alias": "communityName"})
    community_access: Optional[SnmpOneOfCommunityCommunityAccessOptionsDef] = _field(
        default=None, metadata={"alias": "communityAccess"}
    )


@dataclass
class SnmpOneOfGroupNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SnmpOneOfGroupContextOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SnmpOneOfGroupVersionOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SnmpOneOfGroupSecurityLevelOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SnmpGroupSecurityLevelDef


@dataclass
class SnmpOneOfGroupNotifyOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SnmpOneOfGroupReadOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SnmpOneOfGroupWriteOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SnmpGroup:
    context: SnmpOneOfGroupContextOptionsDef
    name: SnmpOneOfGroupNameOptionsDef
    security_level: SnmpOneOfGroupSecurityLevelOptionsDef = _field(
        metadata={"alias": "securityLevel"}
    )
    notify: Optional[SnmpOneOfGroupNotifyOptionsDef] = _field(default=None)
    read: Optional[SnmpOneOfGroupReadOptionsDef] = _field(default=None)
    version: Optional[SnmpOneOfGroupVersionOptionsDef] = _field(default=None)
    write: Optional[SnmpOneOfGroupWriteOptionsDef] = _field(default=None)


@dataclass
class SnmpOneOfUserUserNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SnmpOneOfUserVersionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SnmpOneOfUserVersionOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Optional[SnmpDefaultUserVersionDef] = _field(default=None)


@dataclass
class SnmpOneOfUserUserGroupOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SnmpOneOfUserAuthProtocolOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SnmpUserAuthProtocolDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SnmpOneOfUserPrivProtocolOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SnmpUserPrivProtocolDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SnmpOneOfUserPassphraseOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SnmpUser:
    user_group: SnmpOneOfUserUserGroupOptionsDef = _field(metadata={"alias": "userGroup"})
    user_name: SnmpOneOfUserUserNameOptionsDef = _field(metadata={"alias": "userName"})
    version: Union[
        SnmpOneOfUserVersionOptionsDef1,
        OneOfUserVersionOptionsDef2,
        SnmpOneOfUserVersionOptionsDef3,
    ]
    auth_protocol: Optional[
        Union[SnmpOneOfUserAuthProtocolOptionsDef1, OneOfUserAuthProtocolOptionsDef2]
    ] = _field(default=None, metadata={"alias": "authProtocol"})
    passphrase: Optional[
        Union[SnmpOneOfUserPassphraseOptionsDef1, OneOfUserPassphraseOptionsDef2]
    ] = _field(default=None)
    priv_protocol: Optional[
        Union[SnmpOneOfUserPrivProtocolOptionsDef1, OneOfUserPrivProtocolOptionsDef2]
    ] = _field(default=None, metadata={"alias": "privProtocol"})


@dataclass
class SnmpOneOfHostHostNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SnmpOneOfHostIpOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class SnmpOneOfHostPortOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SnmpOneOfHostHostUserNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SnmpOneOfHostHostVersionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SnmpOneOfHostHostSecurityLevelOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SnmpHostHostSecurityLevelDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SnmpHost:
    host_name: Union[SnmpOneOfHostHostNameOptionsDef1, OneOfHostHostNameOptionsDef2] = _field(
        metadata={"alias": "hostName"}
    )
    host_security_level: Union[
        SnmpOneOfHostHostSecurityLevelOptionsDef1, OneOfHostHostSecurityLevelOptionsDef2
    ] = _field(metadata={"alias": "hostSecurityLevel"})
    host_user_name: SnmpOneOfHostHostUserNameOptionsDef = _field(metadata={"alias": "hostUserName"})
    host_version: Union[SnmpOneOfHostHostVersionOptionsDef1, OneOfHostHostVersionOptionsDef2] = (
        _field(metadata={"alias": "hostVersion"})
    )
    ip: Union[SnmpOneOfHostIpOptionsDef1, OneOfHostIpOptionsDef2]
    port: SnmpOneOfHostPortOptionsDef


@dataclass
class SnmpData:
    # Configure SNMP community
    community: Optional[List[SnmpCommunity]] = _field(default=None)
    # Configure an SNMP group
    group: Optional[List[SnmpGroup]] = _field(default=None)
    # Configure SNMP server to receive SNMP traps
    host: Optional[List[SnmpHost]] = _field(default=None)
    link_down: Optional[Union[OneOfLinkDownOptionsDef1, OneOfLinkDownOptionsDef2]] = _field(
        default=None, metadata={"alias": "linkDown"}
    )
    link_up: Optional[Union[OneOfLinkUpOptionsDef1, OneOfLinkUpOptionsDef2]] = _field(
        default=None, metadata={"alias": "linkUp"}
    )
    # Configure an SNMP user
    user: Optional[List[SnmpUser]] = _field(default=None)


@dataclass
class Payload:
    """
    SNMP profile parcel schema for PUT request
    """

    data: SnmpData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class GetSingleNfvirtualSystemSnmpPayload:
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
    # SNMP profile parcel schema for PUT request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class EditNfvirtualSnmpParcelPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SystemSnmpOneOfCommunityNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SystemSnmpOneOfCommunityCommunityAccessOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SystemSnmpCommunity:
    community_name: SystemSnmpOneOfCommunityNameOptionsDef = _field(
        metadata={"alias": "communityName"}
    )
    community_access: Optional[SystemSnmpOneOfCommunityCommunityAccessOptionsDef] = _field(
        default=None, metadata={"alias": "communityAccess"}
    )


@dataclass
class SystemSnmpOneOfGroupNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SystemSnmpOneOfGroupContextOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SystemSnmpOneOfGroupVersionOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SystemSnmpOneOfGroupSecurityLevelOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SystemSnmpGroupSecurityLevelDef


@dataclass
class SystemSnmpOneOfGroupNotifyOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SystemSnmpOneOfGroupReadOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SystemSnmpOneOfGroupWriteOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SystemSnmpGroup:
    context: SystemSnmpOneOfGroupContextOptionsDef
    name: SystemSnmpOneOfGroupNameOptionsDef
    security_level: SystemSnmpOneOfGroupSecurityLevelOptionsDef = _field(
        metadata={"alias": "securityLevel"}
    )
    notify: Optional[SystemSnmpOneOfGroupNotifyOptionsDef] = _field(default=None)
    read: Optional[SystemSnmpOneOfGroupReadOptionsDef] = _field(default=None)
    version: Optional[SystemSnmpOneOfGroupVersionOptionsDef] = _field(default=None)
    write: Optional[SystemSnmpOneOfGroupWriteOptionsDef] = _field(default=None)


@dataclass
class SystemSnmpOneOfUserUserNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SystemSnmpOneOfUserVersionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SystemSnmpOneOfUserVersionOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Optional[SystemSnmpDefaultUserVersionDef] = _field(default=None)


@dataclass
class SystemSnmpOneOfUserUserGroupOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SystemSnmpOneOfUserAuthProtocolOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SystemSnmpUserAuthProtocolDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SystemSnmpOneOfUserPrivProtocolOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SystemSnmpUserPrivProtocolDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SystemSnmpOneOfUserPassphraseOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SystemSnmpUser:
    user_group: SystemSnmpOneOfUserUserGroupOptionsDef = _field(metadata={"alias": "userGroup"})
    user_name: SystemSnmpOneOfUserUserNameOptionsDef = _field(metadata={"alias": "userName"})
    version: Union[
        SystemSnmpOneOfUserVersionOptionsDef1,
        OneOfUserVersionOptionsDef2,
        SystemSnmpOneOfUserVersionOptionsDef3,
    ]
    auth_protocol: Optional[
        Union[SystemSnmpOneOfUserAuthProtocolOptionsDef1, OneOfUserAuthProtocolOptionsDef2]
    ] = _field(default=None, metadata={"alias": "authProtocol"})
    passphrase: Optional[
        Union[SystemSnmpOneOfUserPassphraseOptionsDef1, OneOfUserPassphraseOptionsDef2]
    ] = _field(default=None)
    priv_protocol: Optional[
        Union[SystemSnmpOneOfUserPrivProtocolOptionsDef1, OneOfUserPrivProtocolOptionsDef2]
    ] = _field(default=None, metadata={"alias": "privProtocol"})


@dataclass
class SystemSnmpOneOfHostHostNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SystemSnmpOneOfHostIpOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class SystemSnmpOneOfHostPortOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SystemSnmpOneOfHostHostUserNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SystemSnmpOneOfHostHostVersionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SystemSnmpOneOfHostHostSecurityLevelOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SystemSnmpHostHostSecurityLevelDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SystemSnmpHost:
    host_name: Union[SystemSnmpOneOfHostHostNameOptionsDef1, OneOfHostHostNameOptionsDef2] = _field(
        metadata={"alias": "hostName"}
    )
    host_security_level: Union[
        SystemSnmpOneOfHostHostSecurityLevelOptionsDef1, OneOfHostHostSecurityLevelOptionsDef2
    ] = _field(metadata={"alias": "hostSecurityLevel"})
    host_user_name: SystemSnmpOneOfHostHostUserNameOptionsDef = _field(
        metadata={"alias": "hostUserName"}
    )
    host_version: Union[
        SystemSnmpOneOfHostHostVersionOptionsDef1, OneOfHostHostVersionOptionsDef2
    ] = _field(metadata={"alias": "hostVersion"})
    ip: Union[SystemSnmpOneOfHostIpOptionsDef1, OneOfHostIpOptionsDef2]
    port: SystemSnmpOneOfHostPortOptionsDef


@dataclass
class SystemSnmpData:
    # Configure SNMP community
    community: Optional[List[SystemSnmpCommunity]] = _field(default=None)
    # Configure an SNMP group
    group: Optional[List[SystemSnmpGroup]] = _field(default=None)
    # Configure SNMP server to receive SNMP traps
    host: Optional[List[SystemSnmpHost]] = _field(default=None)
    link_down: Optional[Union[OneOfLinkDownOptionsDef1, OneOfLinkDownOptionsDef2]] = _field(
        default=None, metadata={"alias": "linkDown"}
    )
    link_up: Optional[Union[OneOfLinkUpOptionsDef1, OneOfLinkUpOptionsDef2]] = _field(
        default=None, metadata={"alias": "linkUp"}
    )
    # Configure an SNMP user
    user: Optional[List[SystemSnmpUser]] = _field(default=None)


@dataclass
class EditNfvirtualSnmpParcelPutRequest:
    """
    SNMP profile parcel schema for PUT request
    """

    data: SystemSnmpData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)
