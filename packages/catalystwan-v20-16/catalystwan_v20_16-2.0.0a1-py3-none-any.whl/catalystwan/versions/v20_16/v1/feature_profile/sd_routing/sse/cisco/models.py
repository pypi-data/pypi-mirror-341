# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

SseInstanceDef = Literal["Cisco-Secure-Access"]

DefaultOptionTypeDef = Literal["default"]

CiscoGlobalOptionTypeDef = Literal["global"]

VariableOptionTypeDef = Literal["variable"]

SseCiscoGlobalOptionTypeDef = Literal["global"]

CiscoVariableOptionTypeDef = Literal["variable"]

SdRoutingSseCiscoGlobalOptionTypeDef = Literal["global"]

SseCiscoVariableOptionTypeDef = Literal["variable"]

CiscoDefaultOptionTypeDef = Literal["default"]

FeatureProfileSdRoutingSseCiscoGlobalOptionTypeDef = Literal["global"]

InterfaceTunnelDcPreferenceDef = Literal["primary-dc", "secondary-dc"]

V1FeatureProfileSdRoutingSseCiscoGlobalOptionTypeDef = Literal["global"]

SdRoutingSseCiscoVariableOptionTypeDef = Literal["variable"]

SseCiscoDefaultOptionTypeDef = Literal["default"]

GlobalOptionTypeDef1 = Literal["global"]

FeatureProfileSdRoutingSseCiscoVariableOptionTypeDef = Literal["variable"]

GlobalOptionTypeDef2 = Literal["global"]

V1FeatureProfileSdRoutingSseCiscoVariableOptionTypeDef = Literal["variable"]

SdRoutingSseCiscoDefaultOptionTypeDef = Literal["default"]

GlobalOptionTypeDef3 = Literal["global"]

VariableOptionTypeDef1 = Literal["variable"]

FeatureProfileSdRoutingSseCiscoDefaultOptionTypeDef = Literal["default"]

GlobalOptionTypeDef4 = Literal["global"]

VariableOptionTypeDef2 = Literal["variable"]

V1FeatureProfileSdRoutingSseCiscoDefaultOptionTypeDef = Literal["default"]

GlobalOptionTypeDef5 = Literal["global"]

VariableOptionTypeDef3 = Literal["variable"]

DefaultOptionTypeDef1 = Literal["default"]

GlobalOptionTypeDef6 = Literal["global"]

InterfaceIkeCiphersuiteDef = Literal[
    "aes128-cbc-sha1", "aes128-cbc-sha2", "aes256-cbc-sha1", "aes256-cbc-sha2"
]

VariableOptionTypeDef4 = Literal["variable"]

DefaultOptionTypeDef2 = Literal["default"]

DefaultInterfaceIkeCiphersuiteDef = Literal["aes256-cbc-sha1"]

GlobalOptionTypeDef7 = Literal["global"]

InterfaceIkeGroupDef = Literal["14", "15", "16", "19", "2", "20", "21", "5"]

VariableOptionTypeDef5 = Literal["variable"]

DefaultOptionTypeDef3 = Literal["default"]

GlobalOptionTypeDef8 = Literal["global"]

VariableOptionTypeDef6 = Literal["variable"]

DefaultOptionTypeDef4 = Literal["default"]

GlobalOptionTypeDef9 = Literal["global"]

VariableOptionTypeDef7 = Literal["variable"]

DefaultOptionTypeDef5 = Literal["default"]

GlobalOptionTypeDef10 = Literal["global"]

InterfaceIpsecCiphersuiteDef = Literal[
    "aes256-cbc-sha1", "aes256-cbc-sha256", "aes256-cbc-sha384", "aes256-cbc-sha512", "aes256-gcm"
]

VariableOptionTypeDef8 = Literal["variable"]

DefaultOptionTypeDef6 = Literal["default"]

GlobalOptionTypeDef11 = Literal["global"]

InterfacePerfectForwardSecrecyDef = Literal[
    "group-14",
    "group-15",
    "group-16",
    "group-19",
    "group-2",
    "group-20",
    "group-21",
    "group-5",
    "none",
]

VariableOptionTypeDef9 = Literal["variable"]

DefaultOptionTypeDef7 = Literal["default"]

GlobalOptionTypeDef12 = Literal["global"]

DefaultOptionTypeDef8 = Literal["default"]

DefaultInterfaceTrackerDef = Literal["DefaultTracker"]

GlobalOptionTypeDef13 = Literal["global"]

GlobalOptionTypeDef14 = Literal["global"]

GlobalOptionTypeDef15 = Literal["global"]

GlobalOptionTypeDef16 = Literal["global"]

DefaultRegionDef = Literal["auto"]

GlobalOptionTypeDef17 = Literal["global"]

GlobalOptionTypeDef18 = Literal["global"]

VariableOptionTypeDef10 = Literal["variable"]

GlobalOptionTypeDef19 = Literal["global"]

VariableOptionTypeDef11 = Literal["variable"]

DefaultOptionTypeDef9 = Literal["default"]

GlobalOptionTypeDef20 = Literal["global"]

VariableOptionTypeDef12 = Literal["variable"]

DefaultOptionTypeDef10 = Literal["default"]

GlobalOptionTypeDef21 = Literal["global"]

VariableOptionTypeDef13 = Literal["variable"]

DefaultOptionTypeDef11 = Literal["default"]

TrackerTrackerTypeDef = Literal["cisco-sse"]

CiscoSseInstanceDef = Literal["Cisco-Secure-Access"]

CiscoDefaultRegionDef = Literal["auto"]

CiscoTrackerTrackerTypeDef = Literal["cisco-sse"]

SseCiscoSseInstanceDef = Literal["Cisco-Secure-Access"]

SseCiscoDefaultRegionDef = Literal["auto"]

SseCiscoTrackerTrackerTypeDef = Literal["cisco-sse"]


@dataclass
class OneOfSseInstanceOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SseInstanceDef


@dataclass
class OneOfOnBooleanDefaultFalseNoVariableOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfOnBooleanDefaultFalseNoVariableOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfInterfaceIfNameOptionsDef:
    option_type: CiscoGlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


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
class OneOfInterfaceTunnelSourceInterfaceOptionsDef1:
    option_type: SseCiscoGlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfInterfaceTunnelSourceInterfaceOptionsDef2:
    option_type: CiscoVariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceTunnelRouteViaOptionsDef1:
    option_type: SdRoutingSseCiscoGlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfInterfaceTunnelRouteViaOptionsDef2:
    option_type: SseCiscoVariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceTunnelRouteViaOptionsDef3:
    option_type: Optional[CiscoDefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[str] = _field(default="")


@dataclass
class OneOfInterfaceTunnelDcPreferenceOptionsDef:
    option_type: FeatureProfileSdRoutingSseCiscoGlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceTunnelDcPreferenceDef


@dataclass
class OneOfInterfaceTcpMssAdjustOptionsDef1:
    option_type: V1FeatureProfileSdRoutingSseCiscoGlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfInterfaceTcpMssAdjustOptionsDef2:
    option_type: SdRoutingSseCiscoVariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceTcpMssAdjustOptionsDef3:
    option_type: SseCiscoDefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfInterfaceMtuOptionsDef1:
    option_type: GlobalOptionTypeDef1 = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfInterfaceMtuOptionsDef2:
    option_type: FeatureProfileSdRoutingSseCiscoVariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceDpdIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef2 = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfInterfaceDpdIntervalOptionsDef2:
    option_type: V1FeatureProfileSdRoutingSseCiscoVariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceDpdIntervalOptionsDef3:
    option_type: Optional[SdRoutingSseCiscoDefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class OneOfInterfaceDpdRetriesOptionsDef1:
    option_type: GlobalOptionTypeDef3 = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfInterfaceDpdRetriesOptionsDef2:
    option_type: VariableOptionTypeDef1 = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceDpdRetriesOptionsDef3:
    option_type: Optional[FeatureProfileSdRoutingSseCiscoDefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class OneOfInterfaceIkeVersionOptionsDef1:
    option_type: GlobalOptionTypeDef4 = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfInterfaceIkeVersionOptionsDef2:
    option_type: VariableOptionTypeDef2 = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceIkeVersionOptionsDef3:
    option_type: Optional[V1FeatureProfileSdRoutingSseCiscoDefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class OneOfInterfaceIkeRekeyIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef5 = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfInterfaceIkeRekeyIntervalOptionsDef2:
    option_type: VariableOptionTypeDef3 = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceIkeRekeyIntervalOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef1] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class OneOfInterfaceIkeCiphersuiteOptionsDef1:
    option_type: GlobalOptionTypeDef6 = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceIkeCiphersuiteDef


@dataclass
class OneOfInterfaceIkeCiphersuiteOptionsDef2:
    option_type: VariableOptionTypeDef4 = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceIkeCiphersuiteOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef2] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[DefaultInterfaceIkeCiphersuiteDef] = _field(default=None)


@dataclass
class OneOfInterfaceIkeGroupOptionsDef1:
    option_type: GlobalOptionTypeDef7 = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceIkeGroupDef


@dataclass
class OneOfInterfaceIkeGroupOptionsDef2:
    option_type: VariableOptionTypeDef5 = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceIkeGroupOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef3] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[InterfaceIkeGroupDef] = _field(default="16")


@dataclass
class OneOfInterfaceIpsecRekeyIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef8 = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfInterfaceIpsecRekeyIntervalOptionsDef2:
    option_type: VariableOptionTypeDef6 = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceIpsecRekeyIntervalOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef4] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class OneOfInterfaceIpsecReplayWindowOptionsDef1:
    option_type: GlobalOptionTypeDef9 = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfInterfaceIpsecReplayWindowOptionsDef2:
    option_type: VariableOptionTypeDef7 = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceIpsecReplayWindowOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef5] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class OneOfInterfaceIpsecCiphersuiteOptionsDef1:
    option_type: GlobalOptionTypeDef10 = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceIpsecCiphersuiteDef


@dataclass
class OneOfInterfaceIpsecCiphersuiteOptionsDef2:
    option_type: VariableOptionTypeDef8 = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceIpsecCiphersuiteOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef6] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[InterfaceIpsecCiphersuiteDef] = _field(default="aes256-cbc-sha512")


@dataclass
class OneOfInterfacePerfectForwardSecrecyOptionsDef1:
    option_type: GlobalOptionTypeDef11 = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfacePerfectForwardSecrecyDef


@dataclass
class OneOfInterfacePerfectForwardSecrecyOptionsDef2:
    option_type: VariableOptionTypeDef9 = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfacePerfectForwardSecrecyOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef7] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[InterfacePerfectForwardSecrecyDef] = _field(default="group-16")


@dataclass
class OneOfInterfaceTrackerOptionsDef1:
    option_type: GlobalOptionTypeDef12 = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfInterfaceTrackerOptionsDef2:
    option_type: DefaultOptionTypeDef8 = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DefaultInterfaceTrackerDef  # pytype: disable=annotation-type-mismatch


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
class Interface:
    if_name: OneOfInterfaceIfNameOptionsDef = _field(metadata={"alias": "ifName"})
    dpd_interval: Optional[
        Union[
            OneOfInterfaceDpdIntervalOptionsDef1,
            OneOfInterfaceDpdIntervalOptionsDef2,
            OneOfInterfaceDpdIntervalOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "dpdInterval"})
    dpd_retries: Optional[
        Union[
            OneOfInterfaceDpdRetriesOptionsDef1,
            OneOfInterfaceDpdRetriesOptionsDef2,
            OneOfInterfaceDpdRetriesOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "dpdRetries"})
    ike_ciphersuite: Optional[
        Union[
            OneOfInterfaceIkeCiphersuiteOptionsDef1,
            OneOfInterfaceIkeCiphersuiteOptionsDef2,
            OneOfInterfaceIkeCiphersuiteOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ikeCiphersuite"})
    ike_group: Optional[
        Union[
            OneOfInterfaceIkeGroupOptionsDef1,
            OneOfInterfaceIkeGroupOptionsDef2,
            OneOfInterfaceIkeGroupOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ikeGroup"})
    ike_rekey_interval: Optional[
        Union[
            OneOfInterfaceIkeRekeyIntervalOptionsDef1,
            OneOfInterfaceIkeRekeyIntervalOptionsDef2,
            OneOfInterfaceIkeRekeyIntervalOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ikeRekeyInterval"})
    ike_version: Optional[
        Union[
            OneOfInterfaceIkeVersionOptionsDef1,
            OneOfInterfaceIkeVersionOptionsDef2,
            OneOfInterfaceIkeVersionOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ikeVersion"})
    ipsec_ciphersuite: Optional[
        Union[
            OneOfInterfaceIpsecCiphersuiteOptionsDef1,
            OneOfInterfaceIpsecCiphersuiteOptionsDef2,
            OneOfInterfaceIpsecCiphersuiteOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ipsecCiphersuite"})
    ipsec_rekey_interval: Optional[
        Union[
            OneOfInterfaceIpsecRekeyIntervalOptionsDef1,
            OneOfInterfaceIpsecRekeyIntervalOptionsDef2,
            OneOfInterfaceIpsecRekeyIntervalOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ipsecRekeyInterval"})
    ipsec_replay_window: Optional[
        Union[
            OneOfInterfaceIpsecReplayWindowOptionsDef1,
            OneOfInterfaceIpsecReplayWindowOptionsDef2,
            OneOfInterfaceIpsecReplayWindowOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ipsecReplayWindow"})
    mtu: Optional[Union[OneOfInterfaceMtuOptionsDef1, OneOfInterfaceMtuOptionsDef2]] = _field(
        default=None
    )
    perfect_forward_secrecy: Optional[
        Union[
            OneOfInterfacePerfectForwardSecrecyOptionsDef1,
            OneOfInterfacePerfectForwardSecrecyOptionsDef2,
            OneOfInterfacePerfectForwardSecrecyOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "perfectForwardSecrecy"})
    shutdown: Optional[
        Union[
            OneOfOnBooleanDefaultFalseOptionsDef1,
            OneOfOnBooleanDefaultFalseOptionsDef2,
            OneOfOnBooleanDefaultFalseOptionsDef3,
        ]
    ] = _field(default=None)
    tcp_mss_adjust: Optional[
        Union[
            OneOfInterfaceTcpMssAdjustOptionsDef1,
            OneOfInterfaceTcpMssAdjustOptionsDef2,
            OneOfInterfaceTcpMssAdjustOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tcpMssAdjust"})
    track_enable: Optional[
        Union[
            OneOfOnBooleanDefaultTrueOptionsDef1,
            OneOfOnBooleanDefaultTrueOptionsDef2,
            OneOfOnBooleanDefaultTrueOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "trackEnable"})
    tracker: Optional[Union[OneOfInterfaceTrackerOptionsDef1, OneOfInterfaceTrackerOptionsDef2]] = (
        _field(default=None)
    )
    tunnel_dc_preference: Optional[OneOfInterfaceTunnelDcPreferenceOptionsDef] = _field(
        default=None, metadata={"alias": "tunnelDcPreference"}
    )
    tunnel_route_via: Optional[
        Union[
            OneOfInterfaceTunnelRouteViaOptionsDef1,
            OneOfInterfaceTunnelRouteViaOptionsDef2,
            OneOfInterfaceTunnelRouteViaOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tunnelRouteVia"})
    tunnel_source_interface: Optional[
        Union[
            OneOfInterfaceTunnelSourceInterfaceOptionsDef1,
            OneOfInterfaceTunnelSourceInterfaceOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "tunnelSourceInterface"})


@dataclass
class OneOfServiceInterfacePairActiveInterfaceOptionsDef:
    option_type: GlobalOptionTypeDef13 = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfServiceInterfacePairActiveInterfaceWeightOptionsDef:
    option_type: GlobalOptionTypeDef14 = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfServiceInterfacePairBackupInterfaceOptionsDef:
    option_type: GlobalOptionTypeDef15 = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfServiceInterfacePairBackupInterfaceWeightOptionsDef:
    option_type: GlobalOptionTypeDef16 = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class InterfacePair:
    active_interface: OneOfServiceInterfacePairActiveInterfaceOptionsDef = _field(
        metadata={"alias": "activeInterface"}
    )
    backup_interface: OneOfServiceInterfacePairBackupInterfaceOptionsDef = _field(
        metadata={"alias": "backupInterface"}
    )
    active_interface_weight: Optional[OneOfServiceInterfacePairActiveInterfaceWeightOptionsDef] = (
        _field(default=None, metadata={"alias": "activeInterfaceWeight"})
    )
    backup_interface_weight: Optional[OneOfServiceInterfacePairBackupInterfaceWeightOptionsDef] = (
        _field(default=None, metadata={"alias": "backupInterfaceWeight"})
    )


@dataclass
class OneOfRegionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfRegionOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfRegionOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[DefaultRegionDef] = _field(default=None)


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
class OneOfTrackerNameOptionsDef:
    option_type: GlobalOptionTypeDef17 = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfTrackerEndpointApiUrlOptionsDef1:
    option_type: GlobalOptionTypeDef18 = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfTrackerEndpointApiUrlOptionsDef2:
    option_type: VariableOptionTypeDef10 = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTrackerThresholdOptionsDef1:
    option_type: GlobalOptionTypeDef19 = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfTrackerThresholdOptionsDef2:
    option_type: VariableOptionTypeDef11 = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTrackerThresholdOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef9] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class OneOfTrackerIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef20 = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfTrackerIntervalOptionsDef2:
    option_type: VariableOptionTypeDef12 = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTrackerIntervalOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef10] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class OneOfTrackerMultiplierOptionsDef1:
    option_type: GlobalOptionTypeDef21 = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfTrackerMultiplierOptionsDef2:
    option_type: VariableOptionTypeDef13 = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTrackerMultiplierOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef11] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class OneOfTrackerTrackerTypeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: TrackerTrackerTypeDef


@dataclass
class Tracker:
    endpoint_api_url: Union[
        OneOfTrackerEndpointApiUrlOptionsDef1, OneOfTrackerEndpointApiUrlOptionsDef2
    ] = _field(metadata={"alias": "endpointApiUrl"})
    name: OneOfTrackerNameOptionsDef
    tracker_type: OneOfTrackerTrackerTypeOptionsDef = _field(metadata={"alias": "trackerType"})
    interval: Optional[
        Union[
            OneOfTrackerIntervalOptionsDef1,
            OneOfTrackerIntervalOptionsDef2,
            OneOfTrackerIntervalOptionsDef3,
        ]
    ] = _field(default=None)
    multiplier: Optional[
        Union[
            OneOfTrackerMultiplierOptionsDef1,
            OneOfTrackerMultiplierOptionsDef2,
            OneOfTrackerMultiplierOptionsDef3,
        ]
    ] = _field(default=None)
    threshold: Optional[
        Union[
            OneOfTrackerThresholdOptionsDef1,
            OneOfTrackerThresholdOptionsDef2,
            OneOfTrackerThresholdOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class CiscoData:
    # Interface name: IPsec when present
    interface: List[Interface]
    # Interface Pair for active and backup
    interface_pair: List[InterfacePair] = _field(metadata={"alias": "interfacePair"})
    region: Union[OneOfRegionOptionsDef1, OneOfRegionOptionsDef2, OneOfRegionOptionsDef3]
    sse_instance: OneOfSseInstanceOptionsDef
    tracker_src_ip: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2] = _field(
        metadata={"alias": "trackerSrcIp"}
    )
    context_sharing_for_sgt: Optional[
        Union[
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef1,
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "contextSharingForSgt"})
    context_sharing_for_vpn: Optional[
        Union[
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef1,
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "contextSharingForVpn"})
    # Tracker configuration
    tracker: Optional[List[Tracker]] = _field(default=None)


@dataclass
class Payload:
    """
    Cisco-SSE schema for POST request
    """

    data: CiscoData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


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
    # Cisco-SSE schema for POST request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdRoutingSseCiscoSsePayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateCiscoSseFeatureForSsePostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SseCiscoData:
    # Interface name: IPsec when present
    interface: List[Interface]
    # Interface Pair for active and backup
    interface_pair: List[InterfacePair] = _field(metadata={"alias": "interfacePair"})
    region: Union[OneOfRegionOptionsDef1, OneOfRegionOptionsDef2, OneOfRegionOptionsDef3]
    sse_instance: OneOfSseInstanceOptionsDef
    tracker_src_ip: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2] = _field(
        metadata={"alias": "trackerSrcIp"}
    )
    context_sharing_for_sgt: Optional[
        Union[
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef1,
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "contextSharingForSgt"})
    context_sharing_for_vpn: Optional[
        Union[
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef1,
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "contextSharingForVpn"})
    # Tracker configuration
    tracker: Optional[List[Tracker]] = _field(default=None)


@dataclass
class CreateCiscoSseFeatureForSsePostRequest:
    """
    Cisco-SSE schema for POST request
    """

    data: SseCiscoData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class CiscoOneOfSseInstanceOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: CiscoSseInstanceDef


@dataclass
class CiscoOneOfRegionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class CiscoOneOfRegionOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[CiscoDefaultRegionDef] = _field(default=None)


@dataclass
class CiscoOneOfTrackerTrackerTypeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: CiscoTrackerTrackerTypeDef


@dataclass
class CiscoTracker:
    endpoint_api_url: Union[
        OneOfTrackerEndpointApiUrlOptionsDef1, OneOfTrackerEndpointApiUrlOptionsDef2
    ] = _field(metadata={"alias": "endpointApiUrl"})
    name: OneOfTrackerNameOptionsDef
    tracker_type: CiscoOneOfTrackerTrackerTypeOptionsDef = _field(metadata={"alias": "trackerType"})
    interval: Optional[
        Union[
            OneOfTrackerIntervalOptionsDef1,
            OneOfTrackerIntervalOptionsDef2,
            OneOfTrackerIntervalOptionsDef3,
        ]
    ] = _field(default=None)
    multiplier: Optional[
        Union[
            OneOfTrackerMultiplierOptionsDef1,
            OneOfTrackerMultiplierOptionsDef2,
            OneOfTrackerMultiplierOptionsDef3,
        ]
    ] = _field(default=None)
    threshold: Optional[
        Union[
            OneOfTrackerThresholdOptionsDef1,
            OneOfTrackerThresholdOptionsDef2,
            OneOfTrackerThresholdOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class SdRoutingSseCiscoData:
    # Interface name: IPsec when present
    interface: List[Interface]
    # Interface Pair for active and backup
    interface_pair: List[InterfacePair] = _field(metadata={"alias": "interfacePair"})
    region: Union[CiscoOneOfRegionOptionsDef1, OneOfRegionOptionsDef2, CiscoOneOfRegionOptionsDef3]
    sse_instance: CiscoOneOfSseInstanceOptionsDef
    tracker_src_ip: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2] = _field(
        metadata={"alias": "trackerSrcIp"}
    )
    context_sharing_for_sgt: Optional[
        Union[
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef1,
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "contextSharingForSgt"})
    context_sharing_for_vpn: Optional[
        Union[
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef1,
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "contextSharingForVpn"})
    # Tracker configuration
    tracker: Optional[List[CiscoTracker]] = _field(default=None)


@dataclass
class CiscoPayload:
    """
    Cisco-SSE schema for PUT request
    """

    data: SdRoutingSseCiscoData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class GetSingleSdRoutingSseCiscoSsePayload:
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
    # Cisco-SSE schema for PUT request
    payload: Optional[CiscoPayload] = _field(default=None)


@dataclass
class EditCiscoSseFeaturePutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SseCiscoOneOfSseInstanceOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SseCiscoSseInstanceDef


@dataclass
class SseCiscoOneOfRegionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SseCiscoOneOfRegionOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[SseCiscoDefaultRegionDef] = _field(default=None)


@dataclass
class SseCiscoOneOfTrackerTrackerTypeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SseCiscoTrackerTrackerTypeDef


@dataclass
class SseCiscoTracker:
    endpoint_api_url: Union[
        OneOfTrackerEndpointApiUrlOptionsDef1, OneOfTrackerEndpointApiUrlOptionsDef2
    ] = _field(metadata={"alias": "endpointApiUrl"})
    name: OneOfTrackerNameOptionsDef
    tracker_type: SseCiscoOneOfTrackerTrackerTypeOptionsDef = _field(
        metadata={"alias": "trackerType"}
    )
    interval: Optional[
        Union[
            OneOfTrackerIntervalOptionsDef1,
            OneOfTrackerIntervalOptionsDef2,
            OneOfTrackerIntervalOptionsDef3,
        ]
    ] = _field(default=None)
    multiplier: Optional[
        Union[
            OneOfTrackerMultiplierOptionsDef1,
            OneOfTrackerMultiplierOptionsDef2,
            OneOfTrackerMultiplierOptionsDef3,
        ]
    ] = _field(default=None)
    threshold: Optional[
        Union[
            OneOfTrackerThresholdOptionsDef1,
            OneOfTrackerThresholdOptionsDef2,
            OneOfTrackerThresholdOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class FeatureProfileSdRoutingSseCiscoData:
    # Interface name: IPsec when present
    interface: List[Interface]
    # Interface Pair for active and backup
    interface_pair: List[InterfacePair] = _field(metadata={"alias": "interfacePair"})
    region: Union[
        SseCiscoOneOfRegionOptionsDef1, OneOfRegionOptionsDef2, SseCiscoOneOfRegionOptionsDef3
    ]
    sse_instance: SseCiscoOneOfSseInstanceOptionsDef
    tracker_src_ip: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2] = _field(
        metadata={"alias": "trackerSrcIp"}
    )
    context_sharing_for_sgt: Optional[
        Union[
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef1,
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "contextSharingForSgt"})
    context_sharing_for_vpn: Optional[
        Union[
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef1,
            OneOfOnBooleanDefaultFalseNoVariableOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "contextSharingForVpn"})
    # Tracker configuration
    tracker: Optional[List[SseCiscoTracker]] = _field(default=None)


@dataclass
class EditCiscoSseFeaturePutRequest:
    """
    Cisco-SSE schema for PUT request
    """

    data: FeatureProfileSdRoutingSseCiscoData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)
