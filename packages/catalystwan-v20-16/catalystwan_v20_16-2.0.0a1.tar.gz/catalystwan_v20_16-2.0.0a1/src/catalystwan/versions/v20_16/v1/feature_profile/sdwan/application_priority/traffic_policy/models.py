# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

SequencesBaseActionDef = Literal["accept", "drop"]

TargetDirectionDef = Literal["all", "service", "tunnel"]

SequencesSequenceIpTypeDef = Literal["all", "ipv4", "ipv6"]

TrafficPolicySequencesBaseActionDef = Literal["accept", "drop"]

TrafficPolicyTargetDirectionDef = Literal["all", "service", "tunnel"]

ApplicationPriorityTrafficPolicyTargetDirectionDef = Literal["all", "service", "tunnel"]

ApplicationPriorityTrafficPolicySequencesBaseActionDef = Literal["accept", "drop"]

SdwanApplicationPriorityTrafficPolicySequencesBaseActionDef = Literal["accept", "drop"]

TrafficPolicySequencesSequenceIpTypeDef = Literal["all", "ipv4", "ipv6"]

FeatureProfileSdwanApplicationPriorityTrafficPolicySequencesBaseActionDef = Literal[
    "accept", "drop"
]

SdwanApplicationPriorityTrafficPolicyTargetDirectionDef = Literal["all", "service", "tunnel"]

FeatureProfileSdwanApplicationPriorityTrafficPolicyTargetDirectionDef = Literal[
    "all", "service", "tunnel"
]

V1FeatureProfileSdwanApplicationPriorityTrafficPolicySequencesBaseActionDef = Literal[
    "accept", "drop"
]

SequencesBaseActionDef1 = Literal["accept", "drop"]

ApplicationPriorityTrafficPolicySequencesSequenceIpTypeDef = Literal["all", "ipv4", "ipv6"]


@dataclass
class CreateTrafficPolicyProfileParcelForapplicationPriorityPostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class OneOfSequencesBaseActionOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SequencesBaseActionDef


@dataclass
class BooleanGlobalOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfTargetVpnOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class OneOfTargetDirectionOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: TargetDirectionDef


@dataclass
class Target1:
    """
    Target vpn and direction
    """

    direction: Optional[OneOfTargetDirectionOptionsDef] = _field(default=None)
    vpn: Optional[OneOfTargetVpnOptionsDef] = _field(default=None)


@dataclass
class CommonRuleDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    rule_id: List[str] = _field(metadata={"alias": "ruleId"})


@dataclass
class Target2:
    """
    rule
    """

    direction: Optional[OneOfTargetDirectionOptionsDef] = _field(default=None)
    vpn_rule: Optional[CommonRuleDef] = _field(default=None, metadata={"alias": "vpnRule"})


@dataclass
class OneOfSequencesSequenceIdOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfSequencesSequenceNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SequenceIpType:
    value: Optional[Any] = _field(default=None)


@dataclass
class Match:
    entries: Optional[Any] = _field(default=None)


@dataclass
class Sequences1:
    actions: Optional[Any] = _field(default=None)
    base_action: Optional[OneOfSequencesBaseActionOptionsDef] = _field(
        default=None, metadata={"alias": "baseAction"}
    )
    match_: Optional[Match] = _field(default=None, metadata={"alias": "match"})
    sequence_id: Optional[OneOfSequencesSequenceIdOptionsDef] = _field(
        default=None, metadata={"alias": "sequenceId"}
    )
    sequence_ip_type: Optional[SequenceIpType] = _field(
        default=None, metadata={"alias": "sequenceIpType"}
    )
    sequence_name: Optional[OneOfSequencesSequenceNameOptionsDef] = _field(
        default=None, metadata={"alias": "sequenceName"}
    )


@dataclass
class OneOfSequencesSequenceIpTypeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SequencesSequenceIpTypeDef


@dataclass
class TrafficPolicyMatch:
    entries: Any


@dataclass
class Sequences2:
    actions: Optional[Any] = _field(default=None)
    base_action: Optional[OneOfSequencesBaseActionOptionsDef] = _field(
        default=None, metadata={"alias": "baseAction"}
    )
    match_: Optional[TrafficPolicyMatch] = _field(default=None, metadata={"alias": "match"})
    sequence_id: Optional[OneOfSequencesSequenceIdOptionsDef] = _field(
        default=None, metadata={"alias": "sequenceId"}
    )
    sequence_ip_type: Optional[OneOfSequencesSequenceIpTypeOptionsDef] = _field(
        default=None, metadata={"alias": "sequenceIpType"}
    )
    sequence_name: Optional[OneOfSequencesSequenceNameOptionsDef] = _field(
        default=None, metadata={"alias": "sequenceName"}
    )


@dataclass
class Data:
    data_default_action: Optional[OneOfSequencesBaseActionOptionsDef] = _field(
        default=None, metadata={"alias": "dataDefaultAction"}
    )
    has_cor_via_sig: Optional[BooleanGlobalOptionsDef] = _field(
        default=None, metadata={"alias": "hasCorViaSig"}
    )
    # Traffic policy sequence list
    sequences: Optional[List[Union[Sequences1, Sequences2]]] = _field(default=None)
    simple_flow: Optional[BooleanGlobalOptionsDef] = _field(
        default=None, metadata={"alias": "simpleFlow"}
    )
    target: Optional[Union[Target1, Target2]] = _field(default=None)


@dataclass
class CreateTrafficPolicyProfileParcelForapplicationPriorityPostRequest:
    """
    traffic policy profile parcel schema for POST request
    """

    data: Data
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class TrafficPolicyOneOfSequencesBaseActionOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: TrafficPolicySequencesBaseActionDef


@dataclass
class TrafficPolicyOneOfTargetVpnOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class TrafficPolicyOneOfTargetDirectionOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: TrafficPolicyTargetDirectionDef


@dataclass
class TrafficPolicyTarget1:
    """
    Target vpn and direction
    """

    direction: Optional[TrafficPolicyOneOfTargetDirectionOptionsDef] = _field(default=None)
    vpn: Optional[TrafficPolicyOneOfTargetVpnOptionsDef] = _field(default=None)


@dataclass
class ApplicationPriorityTrafficPolicyOneOfTargetDirectionOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ApplicationPriorityTrafficPolicyTargetDirectionDef


@dataclass
class TrafficPolicyTarget2:
    """
    rule
    """

    direction: Optional[ApplicationPriorityTrafficPolicyOneOfTargetDirectionOptionsDef] = _field(
        default=None
    )
    vpn_rule: Optional[CommonRuleDef] = _field(default=None, metadata={"alias": "vpnRule"})


@dataclass
class TrafficPolicyOneOfSequencesSequenceIdOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class TrafficPolicyOneOfSequencesSequenceNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ApplicationPriorityTrafficPolicyOneOfSequencesBaseActionOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ApplicationPriorityTrafficPolicySequencesBaseActionDef


@dataclass
class TrafficPolicySequences1:
    actions: Optional[Any] = _field(default=None)
    base_action: Optional[ApplicationPriorityTrafficPolicyOneOfSequencesBaseActionOptionsDef] = (
        _field(default=None, metadata={"alias": "baseAction"})
    )
    match_: Optional[Match] = _field(default=None, metadata={"alias": "match"})
    sequence_id: Optional[TrafficPolicyOneOfSequencesSequenceIdOptionsDef] = _field(
        default=None, metadata={"alias": "sequenceId"}
    )
    sequence_ip_type: Optional[SequenceIpType] = _field(
        default=None, metadata={"alias": "sequenceIpType"}
    )
    sequence_name: Optional[TrafficPolicyOneOfSequencesSequenceNameOptionsDef] = _field(
        default=None, metadata={"alias": "sequenceName"}
    )


@dataclass
class ApplicationPriorityTrafficPolicyOneOfSequencesSequenceIdOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class ApplicationPriorityTrafficPolicyOneOfSequencesSequenceNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SdwanApplicationPriorityTrafficPolicyOneOfSequencesBaseActionOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SdwanApplicationPriorityTrafficPolicySequencesBaseActionDef


@dataclass
class TrafficPolicyOneOfSequencesSequenceIpTypeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: TrafficPolicySequencesSequenceIpTypeDef


@dataclass
class ApplicationPriorityTrafficPolicyMatch:
    entries: Any


@dataclass
class TrafficPolicySequences2:
    actions: Optional[Any] = _field(default=None)
    base_action: Optional[
        SdwanApplicationPriorityTrafficPolicyOneOfSequencesBaseActionOptionsDef
    ] = _field(default=None, metadata={"alias": "baseAction"})
    match_: Optional[ApplicationPriorityTrafficPolicyMatch] = _field(
        default=None, metadata={"alias": "match"}
    )
    sequence_id: Optional[ApplicationPriorityTrafficPolicyOneOfSequencesSequenceIdOptionsDef] = (
        _field(default=None, metadata={"alias": "sequenceId"})
    )
    sequence_ip_type: Optional[TrafficPolicyOneOfSequencesSequenceIpTypeOptionsDef] = _field(
        default=None, metadata={"alias": "sequenceIpType"}
    )
    sequence_name: Optional[
        ApplicationPriorityTrafficPolicyOneOfSequencesSequenceNameOptionsDef
    ] = _field(default=None, metadata={"alias": "sequenceName"})


@dataclass
class TrafficPolicyData:
    data_default_action: Optional[TrafficPolicyOneOfSequencesBaseActionOptionsDef] = _field(
        default=None, metadata={"alias": "dataDefaultAction"}
    )
    has_cor_via_sig: Optional[BooleanGlobalOptionsDef] = _field(
        default=None, metadata={"alias": "hasCorViaSig"}
    )
    # Traffic policy sequence list
    sequences: Optional[List[Union[TrafficPolicySequences1, TrafficPolicySequences2]]] = _field(
        default=None
    )
    simple_flow: Optional[BooleanGlobalOptionsDef] = _field(
        default=None, metadata={"alias": "simpleFlow"}
    )
    target: Optional[Union[TrafficPolicyTarget1, TrafficPolicyTarget2]] = _field(default=None)


@dataclass
class Payload:
    """
    traffic policy profile parcel schema for PUT request
    """

    data: TrafficPolicyData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class GetSingleSdwanApplicationPriorityTrafficPolicyPayload:
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
    # traffic policy profile parcel schema for PUT request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class EditTrafficPolicyProfileParcelForapplicationPriorityPutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class FeatureProfileSdwanApplicationPriorityTrafficPolicyOneOfSequencesBaseActionOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: FeatureProfileSdwanApplicationPriorityTrafficPolicySequencesBaseActionDef


@dataclass
class ApplicationPriorityTrafficPolicyOneOfTargetVpnOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class SdwanApplicationPriorityTrafficPolicyOneOfTargetDirectionOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SdwanApplicationPriorityTrafficPolicyTargetDirectionDef


@dataclass
class ApplicationPriorityTrafficPolicyTarget1:
    """
    Target vpn and direction
    """

    direction: Optional[SdwanApplicationPriorityTrafficPolicyOneOfTargetDirectionOptionsDef] = (
        _field(default=None)
    )
    vpn: Optional[ApplicationPriorityTrafficPolicyOneOfTargetVpnOptionsDef] = _field(default=None)


@dataclass
class FeatureProfileSdwanApplicationPriorityTrafficPolicyOneOfTargetDirectionOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: FeatureProfileSdwanApplicationPriorityTrafficPolicyTargetDirectionDef


@dataclass
class ApplicationPriorityTrafficPolicyTarget2:
    """
    rule
    """

    direction: Optional[
        FeatureProfileSdwanApplicationPriorityTrafficPolicyOneOfTargetDirectionOptionsDef
    ] = _field(default=None)
    vpn_rule: Optional[CommonRuleDef] = _field(default=None, metadata={"alias": "vpnRule"})


@dataclass
class SdwanApplicationPriorityTrafficPolicyOneOfSequencesSequenceIdOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SdwanApplicationPriorityTrafficPolicyOneOfSequencesSequenceNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class V1FeatureProfileSdwanApplicationPriorityTrafficPolicyOneOfSequencesBaseActionOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: V1FeatureProfileSdwanApplicationPriorityTrafficPolicySequencesBaseActionDef


@dataclass
class ApplicationPriorityTrafficPolicySequences1:
    actions: Optional[Any] = _field(default=None)
    base_action: Optional[
        V1FeatureProfileSdwanApplicationPriorityTrafficPolicyOneOfSequencesBaseActionOptionsDef
    ] = _field(default=None, metadata={"alias": "baseAction"})
    match_: Optional[Match] = _field(default=None, metadata={"alias": "match"})
    sequence_id: Optional[
        SdwanApplicationPriorityTrafficPolicyOneOfSequencesSequenceIdOptionsDef
    ] = _field(default=None, metadata={"alias": "sequenceId"})
    sequence_ip_type: Optional[SequenceIpType] = _field(
        default=None, metadata={"alias": "sequenceIpType"}
    )
    sequence_name: Optional[
        SdwanApplicationPriorityTrafficPolicyOneOfSequencesSequenceNameOptionsDef
    ] = _field(default=None, metadata={"alias": "sequenceName"})


@dataclass
class FeatureProfileSdwanApplicationPriorityTrafficPolicyOneOfSequencesSequenceIdOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class FeatureProfileSdwanApplicationPriorityTrafficPolicyOneOfSequencesSequenceNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfSequencesBaseActionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SequencesBaseActionDef1


@dataclass
class ApplicationPriorityTrafficPolicyOneOfSequencesSequenceIpTypeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ApplicationPriorityTrafficPolicySequencesSequenceIpTypeDef


@dataclass
class SdwanApplicationPriorityTrafficPolicyMatch:
    entries: Any


@dataclass
class ApplicationPriorityTrafficPolicySequences2:
    actions: Optional[Any] = _field(default=None)
    base_action: Optional[OneOfSequencesBaseActionOptionsDef1] = _field(
        default=None, metadata={"alias": "baseAction"}
    )
    match_: Optional[SdwanApplicationPriorityTrafficPolicyMatch] = _field(
        default=None, metadata={"alias": "match"}
    )
    sequence_id: Optional[
        FeatureProfileSdwanApplicationPriorityTrafficPolicyOneOfSequencesSequenceIdOptionsDef
    ] = _field(default=None, metadata={"alias": "sequenceId"})
    sequence_ip_type: Optional[
        ApplicationPriorityTrafficPolicyOneOfSequencesSequenceIpTypeOptionsDef
    ] = _field(default=None, metadata={"alias": "sequenceIpType"})
    sequence_name: Optional[
        FeatureProfileSdwanApplicationPriorityTrafficPolicyOneOfSequencesSequenceNameOptionsDef
    ] = _field(default=None, metadata={"alias": "sequenceName"})


@dataclass
class ApplicationPriorityTrafficPolicyData:
    data_default_action: Optional[
        FeatureProfileSdwanApplicationPriorityTrafficPolicyOneOfSequencesBaseActionOptionsDef
    ] = _field(default=None, metadata={"alias": "dataDefaultAction"})
    has_cor_via_sig: Optional[BooleanGlobalOptionsDef] = _field(
        default=None, metadata={"alias": "hasCorViaSig"}
    )
    # Traffic policy sequence list
    sequences: Optional[
        List[
            Union[
                ApplicationPriorityTrafficPolicySequences1,
                ApplicationPriorityTrafficPolicySequences2,
            ]
        ]
    ] = _field(default=None)
    simple_flow: Optional[BooleanGlobalOptionsDef] = _field(
        default=None, metadata={"alias": "simpleFlow"}
    )
    target: Optional[
        Union[ApplicationPriorityTrafficPolicyTarget1, ApplicationPriorityTrafficPolicyTarget2]
    ] = _field(default=None)


@dataclass
class EditTrafficPolicyProfileParcelForapplicationPriorityPutRequest:
    """
    traffic policy profile parcel schema for PUT request
    """

    data: ApplicationPriorityTrafficPolicyData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)
