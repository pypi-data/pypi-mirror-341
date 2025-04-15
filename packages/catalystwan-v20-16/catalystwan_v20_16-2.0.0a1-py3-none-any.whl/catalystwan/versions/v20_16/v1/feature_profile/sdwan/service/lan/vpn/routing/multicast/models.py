# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

VariableOptionTypeDef = Literal["variable"]

GlobalOptionTypeDef = Literal["global"]

DefaultOptionTypeDef = Literal["default"]

OptionType = Literal["default", "global"]

SptThresholdDef = Literal["0", "infinity"]

DefaultSptThresholdDef = Literal["0"]


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
class OneOfThresholdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfThresholdOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfThresholdOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class LocalConfigDef:
    local: Union[
        OneOfOnBooleanDefaultFalseOptionsDef1,
        OneOfOnBooleanDefaultFalseOptionsDef2,
        OneOfOnBooleanDefaultFalseOptionsDef3,
    ]
    threshold: Optional[
        Union[OneOfThresholdOptionsDef1, OneOfThresholdOptionsDef2, OneOfThresholdOptionsDef3]
    ] = _field(default=None)


@dataclass
class Basic:
    """
    multicast basic Attributes
    """

    local_config: LocalConfigDef = _field(metadata={"alias": "localConfig"})
    spt_only: Union[
        OneOfOnBooleanDefaultFalseOptionsDef1,
        OneOfOnBooleanDefaultFalseOptionsDef2,
        OneOfOnBooleanDefaultFalseOptionsDef3,
    ] = _field(metadata={"alias": "sptOnly"})


@dataclass
class OneOfIfNameOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfIfNameOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIgmpVersionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfIgmpVersionOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfMulticastIpV4AddressOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfMulticastIpV4AddressOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfIpV4AddressDefaultOptionsDef1:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfIpV4AddressDefaultOptionsDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfIpV4AddressDefaultOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class JoinGroup:
    group_address: Union[
        OneOfMulticastIpV4AddressOptionsDef1, OneOfMulticastIpV4AddressOptionsDef2
    ] = _field(metadata={"alias": "groupAddress"})
    source_address: Optional[
        Union[
            OneOfIpV4AddressDefaultOptionsDef1,
            OneOfIpV4AddressDefaultOptionsDef2,
            OneOfIpV4AddressDefaultOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "sourceAddress"})


@dataclass
class Interface:
    interface_name: Union[OneOfIfNameOptionsDef1, OneOfIfNameOptionsDef2] = _field(
        metadata={"alias": "interfaceName"}
    )
    version: Union[OneOfIgmpVersionOptionsDef1, OneOfIgmpVersionOptionsDef2]
    # Configure static joins
    join_group: Optional[List[JoinGroup]] = _field(default=None, metadata={"alias": "joinGroup"})


@dataclass
class Igmp:
    """
    set igmp Attributes
    """

    # Set IGMP interface parameters
    interface: List[Interface]


@dataclass
class EnableSsmFlag:
    """
    turn SSM on/off
    """

    option_type: OptionType = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class SsmRangeConfigDef1:
    # turn SSM on/off
    enable_ssm_flag: EnableSsmFlag = _field(metadata={"alias": "enableSSMFlag"})


@dataclass
class BooleanGlobalTrueOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfRangeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfRangeOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfRangeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class SsmRangeConfigDef2:
    enable_ssm_flag: BooleanGlobalTrueOptionsDef = _field(metadata={"alias": "enableSSMFlag"})
    range: Optional[Union[OneOfRangeOptionsDef1, OneOfRangeOptionsDef2, OneOfRangeOptionsDef3]] = (
        _field(default=None)
    )


@dataclass
class OneOfSptThresholdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SptThresholdDef


@dataclass
class OneOfSptThresholdOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfSptThresholdOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultSptThresholdDef  # pytype: disable=annotation-type-mismatch


@dataclass
class Ssm:
    """
    ssm Attributes
    """

    ssm_range_config: Union[SsmRangeConfigDef1, SsmRangeConfigDef2] = _field(
        metadata={"alias": "ssmRangeConfig"}
    )
    spt_threshold: Optional[
        Union[
            OneOfSptThresholdOptionsDef1, OneOfSptThresholdOptionsDef2, OneOfSptThresholdOptionsDef3
        ]
    ] = _field(default=None, metadata={"alias": "sptThreshold"})


@dataclass
class OneOfInterfaceQueryIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfInterfaceQueryIntervalOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceQueryIntervalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfInterfaceJoinPruneIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfInterfaceJoinPruneIntervalOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceJoinPruneIntervalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class MulticastInterface:
    interface_name: Union[OneOfIfNameOptionsDef1, OneOfIfNameOptionsDef2] = _field(
        metadata={"alias": "interfaceName"}
    )
    join_prune_interval: Union[
        OneOfInterfaceJoinPruneIntervalOptionsDef1,
        OneOfInterfaceJoinPruneIntervalOptionsDef2,
        OneOfInterfaceJoinPruneIntervalOptionsDef3,
    ] = _field(metadata={"alias": "joinPruneInterval"})
    query_interval: Union[
        OneOfInterfaceQueryIntervalOptionsDef1,
        OneOfInterfaceQueryIntervalOptionsDef2,
        OneOfInterfaceQueryIntervalOptionsDef3,
    ] = _field(metadata={"alias": "queryInterval"})


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
class OneOfAclOptionsNoDefaultDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfAclOptionsNoDefaultDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class RpAddr:
    access_list: Union[OneOfAclOptionsNoDefaultDef1, OneOfAclOptionsNoDefaultDef2] = _field(
        metadata={"alias": "accessList"}
    )
    address: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2]
    override: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class OneOfSendRpAnnounceListScopeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfSendRpAnnounceListScopeOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class SendRpAnnounceList:
    interface_name: Union[OneOfIfNameOptionsDef1, OneOfIfNameOptionsDef2] = _field(
        metadata={"alias": "interfaceName"}
    )
    scope: Union[OneOfSendRpAnnounceListScopeOptionsDef1, OneOfSendRpAnnounceListScopeOptionsDef2]


@dataclass
class OneOfScopeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfScopeOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class SendRpDiscovery:
    interface_name: Union[OneOfIfNameOptionsDef1, OneOfIfNameOptionsDef2] = _field(
        metadata={"alias": "interfaceName"}
    )
    scope: Union[OneOfScopeOptionsDef1, OneOfScopeOptionsDef2]


@dataclass
class AutoRp:
    """
    autoRp Attributes
    """

    enable_auto_rp_flag: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "enableAutoRPFlag"})
    # Enable or disable RP Announce
    send_rp_announce_list: Optional[List[SendRpAnnounceList]] = _field(
        default=None, metadata={"alias": "sendRpAnnounceList"}
    )
    # Enable or disable RP Discovery
    send_rp_discovery: Optional[List[SendRpDiscovery]] = _field(
        default=None, metadata={"alias": "sendRpDiscovery"}
    )


@dataclass
class OneOfRpCandidateIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfRpCandidateIntervalOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfRpCandidateIntervalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfRpCandidatePriorityOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfRpCandidatePriorityOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfRpCandidatePriorityOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class RpCandidate:
    interface_name: Union[OneOfIfNameOptionsDef1, OneOfIfNameOptionsDef2] = _field(
        metadata={"alias": "interfaceName"}
    )
    group_list: Optional[
        Union[OneOfRangeOptionsDef1, OneOfRangeOptionsDef2, OneOfRangeOptionsDef3]
    ] = _field(default=None, metadata={"alias": "groupList"})
    interval: Optional[
        Union[
            OneOfRpCandidateIntervalOptionsDef1,
            OneOfRpCandidateIntervalOptionsDef2,
            OneOfRpCandidateIntervalOptionsDef3,
        ]
    ] = _field(default=None)
    priority: Optional[
        Union[
            OneOfRpCandidatePriorityOptionsDef1,
            OneOfRpCandidatePriorityOptionsDef2,
            OneOfRpCandidatePriorityOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class OneOfMaskOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfMaskOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfMaskOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfPriorityOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfPriorityOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfPriorityOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfAcceptRpCandidateOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfAcceptRpCandidateOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfAcceptRpCandidateOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class BsrCandidate:
    interface_name: Union[OneOfIfNameOptionsDef1, OneOfIfNameOptionsDef2] = _field(
        metadata={"alias": "interfaceName"}
    )
    accept_rp_candidate: Optional[
        Union[
            OneOfAcceptRpCandidateOptionsDef1,
            OneOfAcceptRpCandidateOptionsDef2,
            OneOfAcceptRpCandidateOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "acceptRpCandidate"})
    mask: Optional[Union[OneOfMaskOptionsDef1, OneOfMaskOptionsDef2, OneOfMaskOptionsDef3]] = (
        _field(default=None)
    )
    priority: Optional[
        Union[OneOfPriorityOptionsDef1, OneOfPriorityOptionsDef2, OneOfPriorityOptionsDef3]
    ] = _field(default=None)


@dataclass
class PimBsr:
    """
    pimBSR Attributes
    """

    # bsr candidate Attributes
    bsr_candidate: Optional[List[BsrCandidate]] = _field(
        default=None, metadata={"alias": "bsrCandidate"}
    )
    # Set RP Discovery Scope
    rp_candidate: Optional[List[RpCandidate]] = _field(
        default=None, metadata={"alias": "rpCandidate"}
    )


@dataclass
class Pim:
    """
    multicast pim Attributes
    """

    # ssm Attributes
    ssm: Ssm
    # autoRp Attributes
    auto_rp: Optional[AutoRp] = _field(default=None, metadata={"alias": "autoRp"})
    # Set PIM interface parameters
    interface: Optional[List[MulticastInterface]] = _field(default=None)
    # pimBSR Attributes
    pim_bsr: Optional[PimBsr] = _field(default=None, metadata={"alias": "pimBsr"})
    # Set Static RP Address(es)
    rp_addr: Optional[List[RpAddr]] = _field(default=None, metadata={"alias": "rpAddr"})


@dataclass
class OneOfMeshGroupOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfMeshGroupOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfMeshGroupOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfPeerIpOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfPeerIpOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfPeerConnectSourceIntfOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfPeerConnectSourceIntfOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfPeerConnectSourceIntfOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfPeerRemoteAsOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfPeerRemoteAsOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfPeerRemoteAsOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfPeerPasswordOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfPeerPasswordOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfPeerPasswordOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfPeerKeepaliveIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfPeerKeepaliveIntervalOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfPeerKeepaliveIntervalOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfPeerKeepaliveHoldTimeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfPeerKeepaliveHoldTimeOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfPeerKeepaliveHoldTimeOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfSaLimitOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfSaLimitOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfSaLimitOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class DefaultPeer:
    """
    Set MSDP default peer
    """

    option_type: OptionType = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfPeerDefaultDef1:
    # Set MSDP default peer
    default_peer: DefaultPeer = _field(metadata={"alias": "defaultPeer"})


@dataclass
class RefId:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ParcelReferenceDef:
    ref_id: RefId = _field(metadata={"alias": "refId"})


@dataclass
class OneOfPeerDefaultDef2:
    default_peer: BooleanGlobalTrueOptionsDef = _field(metadata={"alias": "defaultPeer"})
    prefix_list: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "prefixList"}
    )


@dataclass
class Peer:
    peer_ip: Union[OneOfPeerIpOptionsDef1, OneOfPeerIpOptionsDef2] = _field(
        metadata={"alias": "peerIp"}
    )
    connect_source_intf: Optional[
        Union[
            OneOfPeerConnectSourceIntfOptionsDef1,
            OneOfPeerConnectSourceIntfOptionsDef2,
            OneOfPeerConnectSourceIntfOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "connectSourceIntf"})
    default: Optional[Union[OneOfPeerDefaultDef1, OneOfPeerDefaultDef2]] = _field(default=None)
    keepalive_hold_time: Optional[
        Union[
            OneOfPeerKeepaliveHoldTimeOptionsDef1,
            OneOfPeerKeepaliveHoldTimeOptionsDef2,
            OneOfPeerKeepaliveHoldTimeOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "keepaliveHoldTime"})
    keepalive_interval: Optional[
        Union[
            OneOfPeerKeepaliveIntervalOptionsDef1,
            OneOfPeerKeepaliveIntervalOptionsDef2,
            OneOfPeerKeepaliveIntervalOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "keepaliveInterval"})
    password: Optional[
        Union[
            OneOfPeerPasswordOptionsDef1, OneOfPeerPasswordOptionsDef2, OneOfPeerPasswordOptionsDef3
        ]
    ] = _field(default=None)
    remote_as: Optional[
        Union[
            OneOfPeerRemoteAsOptionsDef1, OneOfPeerRemoteAsOptionsDef2, OneOfPeerRemoteAsOptionsDef3
        ]
    ] = _field(default=None, metadata={"alias": "remoteAs"})
    sa_limit: Optional[
        Union[OneOfSaLimitOptionsDef1, OneOfSaLimitOptionsDef2, OneOfSaLimitOptionsDef3]
    ] = _field(default=None, metadata={"alias": "saLimit"})


@dataclass
class MsdpList:
    # Configure peer
    peer: List[Peer]
    mesh_group: Optional[
        Union[OneOfMeshGroupOptionsDef1, OneOfMeshGroupOptionsDef2, OneOfMeshGroupOptionsDef3]
    ] = _field(default=None, metadata={"alias": "meshGroup"})


@dataclass
class OneOfPeerOriginatorIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfPeerOriginatorIdOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfPeerOriginatorIdOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfRefreshTimerOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfRefreshTimerOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfRefreshTimerOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class Msdp:
    """
    multicast MSDP
    """

    # multicast MSDP peer
    msdp_list: Optional[List[MsdpList]] = _field(default=None, metadata={"alias": "msdpList"})
    originator_id: Optional[
        Union[
            OneOfPeerOriginatorIdOptionsDef1,
            OneOfPeerOriginatorIdOptionsDef2,
            OneOfPeerOriginatorIdOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "originatorId"})
    refresh_timer: Optional[
        Union[
            OneOfRefreshTimerOptionsDef1, OneOfRefreshTimerOptionsDef2, OneOfRefreshTimerOptionsDef3
        ]
    ] = _field(default=None, metadata={"alias": "refreshTimer"})


@dataclass
class Data:
    # multicast basic Attributes
    basic: Basic
    # set igmp Attributes
    igmp: Optional[Igmp] = _field(default=None)
    # multicast MSDP
    msdp: Optional[Msdp] = _field(default=None)
    # multicast pim Attributes
    pim: Optional[Pim] = _field(default=None)


@dataclass
class Payload:
    """
    routing/multicast profile parcel schema for request
    """

    data: Data
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class GetLanVpnAssociatedRoutingMulticastParcelsForServiceGetResponse:
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
    # routing/multicast profile parcel schema for request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class CreateLanVpnAndRoutingMulticastParcelAssociationForServicePostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class CreateLanVpnAndRoutingMulticastParcelAssociationForServicePostRequest:
    """
    Profile Parcel POST Request schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetSingleSdwanServiceLanVpnRoutingMulticastPayload:
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
    # routing/multicast profile parcel schema for request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class EditLanVpnAndRoutingMulticastParcelAssociationForServicePutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class EditLanVpnAndRoutingMulticastParcelAssociationForServicePutRequest:
    """
    Profile Parcel POST Request schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)
