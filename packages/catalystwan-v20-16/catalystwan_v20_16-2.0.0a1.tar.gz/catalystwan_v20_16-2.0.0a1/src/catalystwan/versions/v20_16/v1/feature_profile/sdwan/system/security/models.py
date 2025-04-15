# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

VariableOptionTypeDef = Literal["variable"]

DefaultOptionTypeDef = Literal["default"]

ReplayWindowDef = Literal["1024", "128", "2048", "256", "4096", "512", "64", "8192"]

DefaultReplayWindowDef = Literal["512"]

IntegrityTypeListDef = Literal["esp", "ip-udp-esp", "ip-udp-esp-no-id", "none"]

KeyTcpDef = Literal["aes-128-cmac", "hmac-sha-1", "hmac-sha-256"]


@dataclass
class OneOfRekeyOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfRekeyOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfRekeyOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfReplayWindowOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ReplayWindowDef


@dataclass
class OneOfReplayWindowOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfReplayWindowOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultReplayWindowDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfExtendedArWindowOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfExtendedArWindowOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfExtendedArWindowOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIntegrityTypeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[IntegrityTypeListDef]


@dataclass
class OneOfIntegrityTypeOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfOnBooleanDefaultFalseOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfOnBooleanDefaultFalseOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfOnBooleanDefaultFalseOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfKeychainNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfKeychainKeyidOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class Keychain:
    id: OneOfKeychainKeyidOptionsDef
    name: OneOfKeychainNameOptionsDef


@dataclass
class OneOfKeyIdOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfKeyChainNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfKeySendIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfKeySendIdOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfKeyRecvIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfKeyRecvIdOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfKeyTcpOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: KeyTcpDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfKeyStringOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfKeyStringOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfKeyStartEpochOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfOnBooleanDefaultTrueOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfOnBooleanDefaultTrueOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfOnBooleanDefaultTrueOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfendChoice1:
    infinite: Union[
        OneOfOnBooleanDefaultTrueOptionsDef1,
        OneOfOnBooleanDefaultTrueOptionsDef2,
        OneOfOnBooleanDefaultTrueOptionsDef3,
    ]


@dataclass
class OneOfKeyDurationOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfKeyDurationOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfendChoice2:
    duration: Union[OneOfKeyDurationOptionsDef1, OneOfKeyDurationOptionsDef2]


@dataclass
class OneOfKeyEndEpochOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfendChoice3:
    exact: OneOfKeyEndEpochOptionsDef


@dataclass
class LifetimeSettings:
    start_epoch: OneOfKeyStartEpochOptionsDef = _field(metadata={"alias": "startEpoch"})
    local: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)
    one_ofend_choice: Optional[Union[OneOfendChoice1, OneOfendChoice2, OneOfendChoice3]] = _field(
        default=None, metadata={"alias": "oneOfendChoice"}
    )


@dataclass
class Key:
    id: OneOfKeyIdOptionsDef
    key_string: Union[OneOfKeyStringOptionsDef1, OneOfKeyStringOptionsDef2] = _field(
        metadata={"alias": "keyString"}
    )
    name: OneOfKeyChainNameOptionsDef
    recv_id: Union[OneOfKeyRecvIdOptionsDef1, OneOfKeyRecvIdOptionsDef2] = _field(
        metadata={"alias": "recvId"}
    )
    send_id: Union[OneOfKeySendIdOptionsDef1, OneOfKeySendIdOptionsDef2] = _field(
        metadata={"alias": "sendId"}
    )
    tcp: OneOfKeyTcpOptionsDef
    accept_ao_mismatch: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "acceptAoMismatch"})
    accept_lifetime: Optional[LifetimeSettings] = _field(
        default=None, metadata={"alias": "acceptLifetime"}
    )
    include_tcp_options: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "includeTcpOptions"})
    send_lifetime: Optional[LifetimeSettings] = _field(
        default=None, metadata={"alias": "sendLifetime"}
    )


@dataclass
class SecurityData:
    extended_ar_window: Optional[
        Union[
            OneOfExtendedArWindowOptionsDef1,
            OneOfExtendedArWindowOptionsDef2,
            OneOfExtendedArWindowOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "extendedArWindow"})
    integrity_type: Optional[
        Union[OneOfIntegrityTypeOptionsDef1, OneOfIntegrityTypeOptionsDef2]
    ] = _field(default=None, metadata={"alias": "integrityType"})
    # Configure a Key
    key: Optional[List[Key]] = _field(default=None)
    # Configure a Keychain
    keychain: Optional[List[Keychain]] = _field(default=None)
    pairwise_keying: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "pairwiseKeying"})
    rekey: Optional[Union[OneOfRekeyOptionsDef1, OneOfRekeyOptionsDef2, OneOfRekeyOptionsDef3]] = (
        _field(default=None)
    )
    replay_window: Optional[
        Union[
            OneOfReplayWindowOptionsDef1, OneOfReplayWindowOptionsDef2, OneOfReplayWindowOptionsDef3
        ]
    ] = _field(default=None, metadata={"alias": "replayWindow"})


@dataclass
class Payload:
    """
    System profile Security feature schema for request
    """

    data: SecurityData
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
    # System profile Security feature schema for request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdwanSystemSecurityPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateSecurityForSystemPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SystemSecurityData:
    extended_ar_window: Optional[
        Union[
            OneOfExtendedArWindowOptionsDef1,
            OneOfExtendedArWindowOptionsDef2,
            OneOfExtendedArWindowOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "extendedArWindow"})
    integrity_type: Optional[
        Union[OneOfIntegrityTypeOptionsDef1, OneOfIntegrityTypeOptionsDef2]
    ] = _field(default=None, metadata={"alias": "integrityType"})
    # Configure a Key
    key: Optional[List[Key]] = _field(default=None)
    # Configure a Keychain
    keychain: Optional[List[Keychain]] = _field(default=None)
    pairwise_keying: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "pairwiseKeying"})
    rekey: Optional[Union[OneOfRekeyOptionsDef1, OneOfRekeyOptionsDef2, OneOfRekeyOptionsDef3]] = (
        _field(default=None)
    )
    replay_window: Optional[
        Union[
            OneOfReplayWindowOptionsDef1, OneOfReplayWindowOptionsDef2, OneOfReplayWindowOptionsDef3
        ]
    ] = _field(default=None, metadata={"alias": "replayWindow"})


@dataclass
class CreateSecurityForSystemPostRequest:
    """
    System profile Security feature schema for request
    """

    data: SystemSecurityData
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetSingleSdwanSystemSecurityPayload:
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
    # System profile Security feature schema for request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class EditSecurityForSystemPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SdwanSystemSecurityData:
    extended_ar_window: Optional[
        Union[
            OneOfExtendedArWindowOptionsDef1,
            OneOfExtendedArWindowOptionsDef2,
            OneOfExtendedArWindowOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "extendedArWindow"})
    integrity_type: Optional[
        Union[OneOfIntegrityTypeOptionsDef1, OneOfIntegrityTypeOptionsDef2]
    ] = _field(default=None, metadata={"alias": "integrityType"})
    # Configure a Key
    key: Optional[List[Key]] = _field(default=None)
    # Configure a Keychain
    keychain: Optional[List[Keychain]] = _field(default=None)
    pairwise_keying: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "pairwiseKeying"})
    rekey: Optional[Union[OneOfRekeyOptionsDef1, OneOfRekeyOptionsDef2, OneOfRekeyOptionsDef3]] = (
        _field(default=None)
    )
    replay_window: Optional[
        Union[
            OneOfReplayWindowOptionsDef1, OneOfReplayWindowOptionsDef2, OneOfReplayWindowOptionsDef3
        ]
    ] = _field(default=None, metadata={"alias": "replayWindow"})


@dataclass
class EditSecurityForSystemPutRequest:
    """
    System profile Security feature schema for request
    """

    data: SdwanSystemSecurityData
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
