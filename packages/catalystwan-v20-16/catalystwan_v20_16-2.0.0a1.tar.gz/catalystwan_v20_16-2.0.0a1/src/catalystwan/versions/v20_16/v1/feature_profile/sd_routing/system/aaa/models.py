# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

VariableOptionTypeDef = Literal["variable"]

DefaultOptionTypeDef = Literal["default"]

UserPrivilegeDef = Literal["1", "15"]

DefaultUserPrivilegeDef = Literal["15"]

UserPubkeyChainKeyTypeDef = Literal["ssh-rsa"]

RadiusServerKeyEnumDef = Literal["6", "7"]

RadiusServerKeyTypeDef = Literal["key", "pac"]

DefaultRadiusServerKeyTypeDef = Literal["key"]

TacacsServerKeyEnumDef = Literal["6", "7"]

AccountingRuleMethodDef = Literal["commands", "exec", "network", "system"]

AccountingRuleLevelDef = Literal["1", "15"]

AuthorizationRuleMethodDef = Literal["commands"]

AuthorizationRuleLevelDef = Literal["1", "15"]


@dataclass
class OneOfAuthenticationGroupOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAuthenticationGroupOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAuthenticationGroupOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAccountingGroupOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAccountingGroupOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAccountingGroupOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfServerAuthOrderOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class OneOfUserNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfUserNameOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfUserPasswordOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfUserPasswordOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfUserPrivilegeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: UserPrivilegeDef


@dataclass
class OneOfUserPrivilegeOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfUserPrivilegeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultUserPrivilegeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfUserPubkeyChainKeyStringOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfUserPubkeyChainKeyStringOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfUserPubkeyChainKeyTypeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: UserPubkeyChainKeyTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class PubkeyChain:
    key_string: Union[
        OneOfUserPubkeyChainKeyStringOptionsDef1, OneOfUserPubkeyChainKeyStringOptionsDef2
    ] = _field(metadata={"alias": "keyString"})
    key_type: Optional[OneOfUserPubkeyChainKeyTypeOptionsDef] = _field(
        default=None, metadata={"alias": "keyType"}
    )


@dataclass
class User:
    name: Union[OneOfUserNameOptionsDef1, OneOfUserNameOptionsDef2]
    password: Union[OneOfUserPasswordOptionsDef1, OneOfUserPasswordOptionsDef2]
    privilege: Optional[
        Union[
            OneOfUserPrivilegeOptionsDef1,
            OneOfUserPrivilegeOptionsDef2,
            OneOfUserPrivilegeOptionsDef3,
        ]
    ] = _field(default=None)
    # List of RSA public-keys per user
    pubkey_chain: Optional[List[PubkeyChain]] = _field(
        default=None, metadata={"alias": "pubkeyChain"}
    )


@dataclass
class OneOfRadiusGroupNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfVrfOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfVrfOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfInterfaceNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfInterfaceNameOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceNameOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfRadiusServerAddressOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfRadiusServerAuthPortOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfRadiusServerAuthPortOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfRadiusServerAuthPortOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfRadiusServerAcctPortOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfRadiusServerAcctPortOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfRadiusServerAcctPortOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfRadiusServerTimeoutOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfRadiusServerTimeoutOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfRadiusServerTimeoutOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfRadiusServerRetransmitOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfRadiusServerRetransmitOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfRadiusServerRetransmitOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfRadiusServerKeyOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfRadiusServerKeyOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfRadiusServerSecretKeyOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfRadiusServerSecretKeyOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfRadiusServerSecretKeyOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfRadiusServerKeyEnumOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: RadiusServerKeyEnumDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfRadiusServerKeyEnumOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfRadiusServerKeyTypeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: RadiusServerKeyTypeDef


@dataclass
class OneOfRadiusServerKeyTypeOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfRadiusServerKeyTypeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultRadiusServerKeyTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class Server:
    address: OneOfRadiusServerAddressOptionsDef
    key: Union[OneOfRadiusServerKeyOptionsDef1, OneOfRadiusServerKeyOptionsDef2]
    acct_port: Optional[
        Union[
            OneOfRadiusServerAcctPortOptionsDef1,
            OneOfRadiusServerAcctPortOptionsDef2,
            OneOfRadiusServerAcctPortOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "acctPort"})
    auth_port: Optional[
        Union[
            OneOfRadiusServerAuthPortOptionsDef1,
            OneOfRadiusServerAuthPortOptionsDef2,
            OneOfRadiusServerAuthPortOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "authPort"})
    key_enum: Optional[
        Union[OneOfRadiusServerKeyEnumOptionsDef1, OneOfRadiusServerKeyEnumOptionsDef2]
    ] = _field(default=None, metadata={"alias": "keyEnum"})
    key_type: Optional[
        Union[
            OneOfRadiusServerKeyTypeOptionsDef1,
            OneOfRadiusServerKeyTypeOptionsDef2,
            OneOfRadiusServerKeyTypeOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "keyType"})
    retransmit: Optional[
        Union[
            OneOfRadiusServerRetransmitOptionsDef1,
            OneOfRadiusServerRetransmitOptionsDef2,
            OneOfRadiusServerRetransmitOptionsDef3,
        ]
    ] = _field(default=None)
    secret_key: Optional[
        Union[
            OneOfRadiusServerSecretKeyOptionsDef1,
            OneOfRadiusServerSecretKeyOptionsDef2,
            OneOfRadiusServerSecretKeyOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "secretKey"})
    timeout: Optional[
        Union[
            OneOfRadiusServerTimeoutOptionsDef1,
            OneOfRadiusServerTimeoutOptionsDef2,
            OneOfRadiusServerTimeoutOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class Radius:
    group_name: OneOfRadiusGroupNameOptionsDef = _field(metadata={"alias": "groupName"})
    # Configure the Radius server
    server: List[Server]
    source_interface: Optional[
        Union[
            OneOfInterfaceNameOptionsDef1,
            OneOfInterfaceNameOptionsDef2,
            OneOfInterfaceNameOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sourceInterface"})
    vrf: Optional[Union[OneOfVrfOptionsDef1, OneOfVrfOptionsDef2]] = _field(default=None)


@dataclass
class OneOfTacacsGroupNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfTacacsServerAddressOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfTacacsServerPortOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfTacacsServerPortOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTacacsServerPortOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfTacacsServerTimeoutOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfTacacsServerTimeoutOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTacacsServerTimeoutOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfTacacsServerKeyOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfTacacsServerKeyOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTacacsServerSecretKeyOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfTacacsServerSecretKeyOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTacacsServerKeyEnumOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: TacacsServerKeyEnumDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfTacacsServerKeyEnumOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class AaaServer:
    address: OneOfTacacsServerAddressOptionsDef
    key: Union[OneOfTacacsServerKeyOptionsDef1, OneOfTacacsServerKeyOptionsDef2]
    key_enum: Optional[
        Union[OneOfTacacsServerKeyEnumOptionsDef1, OneOfTacacsServerKeyEnumOptionsDef2]
    ] = _field(default=None, metadata={"alias": "keyEnum"})
    port: Optional[
        Union[
            OneOfTacacsServerPortOptionsDef1,
            OneOfTacacsServerPortOptionsDef2,
            OneOfTacacsServerPortOptionsDef3,
        ]
    ] = _field(default=None)
    secret_key: Optional[
        Union[OneOfTacacsServerSecretKeyOptionsDef1, OneOfTacacsServerSecretKeyOptionsDef2]
    ] = _field(default=None, metadata={"alias": "secretKey"})
    timeout: Optional[
        Union[
            OneOfTacacsServerTimeoutOptionsDef1,
            OneOfTacacsServerTimeoutOptionsDef2,
            OneOfTacacsServerTimeoutOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class Tacacs:
    group_name: OneOfTacacsGroupNameOptionsDef = _field(metadata={"alias": "groupName"})
    # Configure the TACACS server
    server: List[AaaServer]
    source_interface: Optional[
        Union[
            OneOfInterfaceNameOptionsDef1,
            OneOfInterfaceNameOptionsDef2,
            OneOfInterfaceNameOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sourceInterface"})
    vrf: Optional[Union[OneOfVrfOptionsDef1, OneOfVrfOptionsDef2]] = _field(default=None)


@dataclass
class OneOfAccountingRuleRuleIdOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfAccountingRuleMethodOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: AccountingRuleMethodDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfAccountingRuleLevelOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: AccountingRuleLevelDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfAccountingRuleLevelOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfAccountingRuleStartStopOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAccountingRuleStartStopOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAccountingRuleStartStopOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAccountingRuleGroupOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class AccountingRule:
    group: OneOfAccountingRuleGroupOptionsDef
    method: OneOfAccountingRuleMethodOptionsDef
    rule_id: OneOfAccountingRuleRuleIdOptionsDef = _field(metadata={"alias": "ruleId"})
    level: Optional[
        Union[OneOfAccountingRuleLevelOptionsDef1, OneOfAccountingRuleLevelOptionsDef2]
    ] = _field(default=None)
    start_stop: Optional[
        Union[
            OneOfAccountingRuleStartStopOptionsDef1,
            OneOfAccountingRuleStartStopOptionsDef2,
            OneOfAccountingRuleStartStopOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "startStop"})


@dataclass
class OneOfAuthorizationConsoleOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAuthorizationConsoleOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAuthorizationConsoleOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAuthorizationConfigCommandsOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAuthorizationConfigCommandsOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAuthorizationConfigCommandsOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAuthorizationRuleRuleIdOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfAuthorizationRuleMethodOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: AuthorizationRuleMethodDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfAuthorizationRuleLevelOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: AuthorizationRuleLevelDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfAuthorizationRuleGroupOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class OneOfAuthorizationRuleIfAuthenticatedOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAuthorizationRuleIfAuthenticatedOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class AuthorizationRule:
    group: OneOfAuthorizationRuleGroupOptionsDef
    level: OneOfAuthorizationRuleLevelOptionsDef
    method: OneOfAuthorizationRuleMethodOptionsDef
    rule_id: OneOfAuthorizationRuleRuleIdOptionsDef = _field(metadata={"alias": "ruleId"})
    if_authenticated: Optional[
        Union[
            OneOfAuthorizationRuleIfAuthenticatedOptionsDef1,
            OneOfAuthorizationRuleIfAuthenticatedOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "ifAuthenticated"})


@dataclass
class AaaData:
    accounting_group: Union[
        OneOfAccountingGroupOptionsDef1,
        OneOfAccountingGroupOptionsDef2,
        OneOfAccountingGroupOptionsDef3,
    ] = _field(metadata={"alias": "accountingGroup"})
    authentication_group: Union[
        OneOfAuthenticationGroupOptionsDef1,
        OneOfAuthenticationGroupOptionsDef2,
        OneOfAuthenticationGroupOptionsDef3,
    ] = _field(metadata={"alias": "authenticationGroup"})
    authorization_config_commands: Union[
        OneOfAuthorizationConfigCommandsOptionsDef1,
        OneOfAuthorizationConfigCommandsOptionsDef2,
        OneOfAuthorizationConfigCommandsOptionsDef3,
    ] = _field(metadata={"alias": "authorizationConfigCommands"})
    authorization_console: Union[
        OneOfAuthorizationConsoleOptionsDef1,
        OneOfAuthorizationConsoleOptionsDef2,
        OneOfAuthorizationConsoleOptionsDef3,
    ] = _field(metadata={"alias": "authorizationConsole"})
    server_auth_order: OneOfServerAuthOrderOptionsDef = _field(
        metadata={"alias": "serverAuthOrder"}
    )
    # Configure the accounting rules
    accounting_rule: Optional[List[AccountingRule]] = _field(
        default=None, metadata={"alias": "accountingRule"}
    )
    # Configure the Authorization Rules
    authorization_rule: Optional[List[AuthorizationRule]] = _field(
        default=None, metadata={"alias": "authorizationRule"}
    )
    # Configure the Radius serverGroup
    radius: Optional[List[Radius]] = _field(default=None)
    # Configure the TACACS serverGroup
    tacacs: Optional[List[Tacacs]] = _field(default=None)
    # Create local login account
    user: Optional[List[User]] = _field(default=None)


@dataclass
class Payload:
    """
    SD-Routing AAA feature schema
    """

    data: AaaData
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
    # SD-Routing AAA feature schema
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdRoutingSystemAaaSdRoutingPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateSdroutingAaaFeaturePostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SystemAaaData:
    accounting_group: Union[
        OneOfAccountingGroupOptionsDef1,
        OneOfAccountingGroupOptionsDef2,
        OneOfAccountingGroupOptionsDef3,
    ] = _field(metadata={"alias": "accountingGroup"})
    authentication_group: Union[
        OneOfAuthenticationGroupOptionsDef1,
        OneOfAuthenticationGroupOptionsDef2,
        OneOfAuthenticationGroupOptionsDef3,
    ] = _field(metadata={"alias": "authenticationGroup"})
    authorization_config_commands: Union[
        OneOfAuthorizationConfigCommandsOptionsDef1,
        OneOfAuthorizationConfigCommandsOptionsDef2,
        OneOfAuthorizationConfigCommandsOptionsDef3,
    ] = _field(metadata={"alias": "authorizationConfigCommands"})
    authorization_console: Union[
        OneOfAuthorizationConsoleOptionsDef1,
        OneOfAuthorizationConsoleOptionsDef2,
        OneOfAuthorizationConsoleOptionsDef3,
    ] = _field(metadata={"alias": "authorizationConsole"})
    server_auth_order: OneOfServerAuthOrderOptionsDef = _field(
        metadata={"alias": "serverAuthOrder"}
    )
    # Configure the accounting rules
    accounting_rule: Optional[List[AccountingRule]] = _field(
        default=None, metadata={"alias": "accountingRule"}
    )
    # Configure the Authorization Rules
    authorization_rule: Optional[List[AuthorizationRule]] = _field(
        default=None, metadata={"alias": "authorizationRule"}
    )
    # Configure the Radius serverGroup
    radius: Optional[List[Radius]] = _field(default=None)
    # Configure the TACACS serverGroup
    tacacs: Optional[List[Tacacs]] = _field(default=None)
    # Create local login account
    user: Optional[List[User]] = _field(default=None)


@dataclass
class CreateSdroutingAaaFeaturePostRequest:
    """
    SD-Routing AAA feature schema
    """

    data: SystemAaaData
    name: str
    # Set the feature description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetSingleSdRoutingSystemAaaSdRoutingPayload:
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
    # SD-Routing AAA feature schema
    payload: Optional[Payload] = _field(default=None)


@dataclass
class EditSdroutingAaaFeaturePutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SdRoutingSystemAaaData:
    accounting_group: Union[
        OneOfAccountingGroupOptionsDef1,
        OneOfAccountingGroupOptionsDef2,
        OneOfAccountingGroupOptionsDef3,
    ] = _field(metadata={"alias": "accountingGroup"})
    authentication_group: Union[
        OneOfAuthenticationGroupOptionsDef1,
        OneOfAuthenticationGroupOptionsDef2,
        OneOfAuthenticationGroupOptionsDef3,
    ] = _field(metadata={"alias": "authenticationGroup"})
    authorization_config_commands: Union[
        OneOfAuthorizationConfigCommandsOptionsDef1,
        OneOfAuthorizationConfigCommandsOptionsDef2,
        OneOfAuthorizationConfigCommandsOptionsDef3,
    ] = _field(metadata={"alias": "authorizationConfigCommands"})
    authorization_console: Union[
        OneOfAuthorizationConsoleOptionsDef1,
        OneOfAuthorizationConsoleOptionsDef2,
        OneOfAuthorizationConsoleOptionsDef3,
    ] = _field(metadata={"alias": "authorizationConsole"})
    server_auth_order: OneOfServerAuthOrderOptionsDef = _field(
        metadata={"alias": "serverAuthOrder"}
    )
    # Configure the accounting rules
    accounting_rule: Optional[List[AccountingRule]] = _field(
        default=None, metadata={"alias": "accountingRule"}
    )
    # Configure the Authorization Rules
    authorization_rule: Optional[List[AuthorizationRule]] = _field(
        default=None, metadata={"alias": "authorizationRule"}
    )
    # Configure the Radius serverGroup
    radius: Optional[List[Radius]] = _field(default=None)
    # Configure the TACACS serverGroup
    tacacs: Optional[List[Tacacs]] = _field(default=None)
    # Create local login account
    user: Optional[List[User]] = _field(default=None)


@dataclass
class EditSdroutingAaaFeaturePutRequest:
    """
    SD-Routing AAA feature schema
    """

    data: SdRoutingSystemAaaData
    name: str
    # Set the feature description
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
