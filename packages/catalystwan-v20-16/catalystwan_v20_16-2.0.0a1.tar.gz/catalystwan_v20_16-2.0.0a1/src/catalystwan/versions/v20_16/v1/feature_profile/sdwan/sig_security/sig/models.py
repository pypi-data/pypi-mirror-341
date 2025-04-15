# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

SigProviderDef = Literal["Generic", "Umbrella", "Zscaler"]

DefaultOptionTypeDef = Literal["default"]

VariableOptionTypeDef = Literal["variable"]

InterfaceApplicationDef = Literal["sig"]

InterfaceTunnelSetDef = Literal[
    "secure-internet-gateway-other",
    "secure-internet-gateway-umbrella",
    "secure-internet-gateway-zscaler",
]

InterfaceTunnelDcPreferenceDef = Literal["primary-dc", "secondary-dc"]

InterfaceIkeCiphersuiteDef = Literal[
    "aes128-cbc-sha1", "aes128-cbc-sha2", "aes256-cbc-sha1", "aes256-cbc-sha2"
]

DefaultInterfaceIkeCiphersuiteDef = Literal["aes256-cbc-sha1"]

InterfaceIkeGroupDef = Literal["14", "15", "16", "19", "2", "20", "21", "5"]

InterfaceIpsecCiphersuiteDef = Literal[
    "aes256-cbc-sha1", "aes256-cbc-sha256", "aes256-cbc-sha384", "aes256-cbc-sha512", "aes256-gcm"
]

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

ServiceDisplayTimeUnitDef = Literal["DAY", "HOUR", "MINUTE"]

DefaultServiceDisplayTimeUnitDef = Literal["MINUTE"]

ServiceRefreshTimeUnitDef = Literal["DAY", "HOUR", "MINUTE"]

DefaultServiceRefreshTimeUnitDef = Literal["MINUTE"]

TrackerTrackerTypeDef = Literal["SIG"]

SigSigProviderDef = Literal["Generic", "Umbrella", "Zscaler"]

SigInterfaceApplicationDef = Literal["sig"]

SigInterfaceTunnelSetDef = Literal[
    "secure-internet-gateway-other",
    "secure-internet-gateway-umbrella",
    "secure-internet-gateway-zscaler",
]

SigInterfaceTunnelDcPreferenceDef = Literal["primary-dc", "secondary-dc"]

SigInterfaceIkeCiphersuiteDef = Literal[
    "aes128-cbc-sha1", "aes128-cbc-sha2", "aes256-cbc-sha1", "aes256-cbc-sha2"
]

SigDefaultInterfaceIkeCiphersuiteDef = Literal["aes256-cbc-sha1"]

SigInterfaceIkeGroupDef = Literal["14", "15", "16", "19", "2", "20", "21", "5"]

SigSecuritySigInterfaceIkeGroupDef = Literal["14", "15", "16", "19", "2", "20", "21", "5"]

SigInterfaceIpsecCiphersuiteDef = Literal[
    "aes256-cbc-sha1", "aes256-cbc-sha256", "aes256-cbc-sha384", "aes256-cbc-sha512", "aes256-gcm"
]

SigSecuritySigInterfaceIpsecCiphersuiteDef = Literal[
    "aes256-cbc-sha1", "aes256-cbc-sha256", "aes256-cbc-sha384", "aes256-cbc-sha512", "aes256-gcm"
]

SigInterfacePerfectForwardSecrecyDef = Literal[
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

SigSecuritySigInterfacePerfectForwardSecrecyDef = Literal[
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

SigServiceDisplayTimeUnitDef = Literal["DAY", "HOUR", "MINUTE"]

SigDefaultServiceDisplayTimeUnitDef = Literal["MINUTE"]

SigServiceRefreshTimeUnitDef = Literal["DAY", "HOUR", "MINUTE"]

SigDefaultServiceRefreshTimeUnitDef = Literal["MINUTE"]

SigTrackerTrackerTypeDef = Literal["SIG"]

SigSecuritySigSigProviderDef = Literal["Generic", "Umbrella", "Zscaler"]

SigSecuritySigInterfaceApplicationDef = Literal["sig"]

SigSecuritySigInterfaceTunnelSetDef = Literal[
    "secure-internet-gateway-other",
    "secure-internet-gateway-umbrella",
    "secure-internet-gateway-zscaler",
]

SigSecuritySigInterfaceTunnelDcPreferenceDef = Literal["primary-dc", "secondary-dc"]

SigSecuritySigInterfaceIkeCiphersuiteDef = Literal[
    "aes128-cbc-sha1", "aes128-cbc-sha2", "aes256-cbc-sha1", "aes256-cbc-sha2"
]

SigSecuritySigDefaultInterfaceIkeCiphersuiteDef = Literal["aes256-cbc-sha1"]

SdwanSigSecuritySigInterfaceIkeGroupDef = Literal["14", "15", "16", "19", "2", "20", "21", "5"]

FeatureProfileSdwanSigSecuritySigInterfaceIkeGroupDef = Literal[
    "14", "15", "16", "19", "2", "20", "21", "5"
]

SdwanSigSecuritySigInterfaceIpsecCiphersuiteDef = Literal[
    "aes256-cbc-sha1", "aes256-cbc-sha256", "aes256-cbc-sha384", "aes256-cbc-sha512", "aes256-gcm"
]

FeatureProfileSdwanSigSecuritySigInterfaceIpsecCiphersuiteDef = Literal[
    "aes256-cbc-sha1", "aes256-cbc-sha256", "aes256-cbc-sha384", "aes256-cbc-sha512", "aes256-gcm"
]

SdwanSigSecuritySigInterfacePerfectForwardSecrecyDef = Literal[
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

FeatureProfileSdwanSigSecuritySigInterfacePerfectForwardSecrecyDef = Literal[
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

SigSecuritySigServiceDisplayTimeUnitDef = Literal["DAY", "HOUR", "MINUTE"]

SigSecuritySigDefaultServiceDisplayTimeUnitDef = Literal["MINUTE"]

SigSecuritySigServiceRefreshTimeUnitDef = Literal["DAY", "HOUR", "MINUTE"]

SigSecuritySigDefaultServiceRefreshTimeUnitDef = Literal["MINUTE"]

SigSecuritySigTrackerTrackerTypeDef = Literal["SIG"]


@dataclass
class OneOfSigProviderOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SigProviderDef


@dataclass
class OneOfSrcVpnOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfSrcVpnOptionsDef2:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[bool] = _field(default=None)


@dataclass
class InterfaceMetadataSharing:
    src_vpn: Optional[Union[OneOfSrcVpnOptionsDef1, OneOfSrcVpnOptionsDef2]] = _field(
        default=None, metadata={"alias": "srcVpn"}
    )


@dataclass
class OneOfInterfaceIfNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfInterfaceAutoOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfInterfaceShutdownOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfInterfaceShutdownOptionsDef2:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[bool] = _field(default=None)


@dataclass
class OneOfInterfaceDescriptionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfInterfaceDescriptionOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceDescriptionOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfInterfaceUnnumberedOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfInterfaceAddressOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfInterfaceAddressOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceAddressOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfInterfaceTunnelSourceOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfInterfaceTunnelSourceOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceTunnelSourceInterfaceOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfInterfaceTunnelSourceInterfaceOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceTunnelRouteViaOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfInterfaceTunnelRouteViaOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceTunnelRouteViaOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[str] = _field(default="")


@dataclass
class OneOfInterfaceTunnelDestinationOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfInterfaceTunnelDestinationOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceApplicationOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceApplicationDef


@dataclass
class OneOfInterfaceTunnelSetOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceTunnelSetDef


@dataclass
class OneOfInterfaceTunnelDcPreferenceOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceTunnelDcPreferenceDef


@dataclass
class OneOfInterfaceTcpMssAdjustOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfInterfaceTcpMssAdjustOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceTcpMssAdjustOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfInterfaceMtuOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfInterfaceMtuOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceDpdIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfInterfaceDpdIntervalOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceDpdIntervalOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class OneOfInterfaceDpdRetriesOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfInterfaceDpdRetriesOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceDpdRetriesOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class OneOfInterfaceIkeVersionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfInterfaceIkeVersionOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceIkeVersionOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class OneOfInterfacePreSharedSecretOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfInterfacePreSharedSecretOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfacePreSharedSecretOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfInterfaceIkeRekeyIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfInterfaceIkeRekeyIntervalOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceIkeRekeyIntervalOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class OneOfInterfaceIkeCiphersuiteOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceIkeCiphersuiteDef


@dataclass
class OneOfInterfaceIkeCiphersuiteOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceIkeCiphersuiteOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[DefaultInterfaceIkeCiphersuiteDef] = _field(default=None)


@dataclass
class OneOfInterfaceIkeGroupOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceIkeGroupDef


@dataclass
class OneOfInterfaceIkeGroupOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceIkeGroupOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[InterfaceIkeGroupDef] = _field(default="16")


@dataclass
class OneOfInterfacePreSharedKeyDynamicOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfInterfaceIkeLocalIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfInterfaceIkeLocalIdOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceIkeLocalIdOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfInterfaceIkeRemoteIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfInterfaceIkeRemoteIdOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceIkeRemoteIdOptionsDef3:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfInterfaceIpsecRekeyIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfInterfaceIpsecRekeyIntervalOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceIpsecRekeyIntervalOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class OneOfInterfaceIpsecReplayWindowOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfInterfaceIpsecReplayWindowOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceIpsecReplayWindowOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class OneOfInterfaceIpsecCiphersuiteOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfaceIpsecCiphersuiteDef


@dataclass
class OneOfInterfaceIpsecCiphersuiteOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceIpsecCiphersuiteOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[InterfaceIpsecCiphersuiteDef] = _field(default="aes256-cbc-sha512")


@dataclass
class OneOfInterfacePerfectForwardSecrecyOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InterfacePerfectForwardSecrecyDef


@dataclass
class OneOfInterfacePerfectForwardSecrecyOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfacePerfectForwardSecrecyOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[InterfacePerfectForwardSecrecyDef] = _field(default="none")


@dataclass
class OneOfInterfaceTrackerOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfInterfaceTrackerOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfInterfaceTrackEnableOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfInterfaceTrackEnableOptionsDef2:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[bool] = _field(default=None)


@dataclass
class OneOfInterfaceTunnelPublicIpOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfInterfaceTunnelPublicIpOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfInterfaceTunnelPublicIpOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[str] = _field(default="Auto")


@dataclass
class Interface:
    if_name: OneOfInterfaceIfNameOptionsDef = _field(metadata={"alias": "ifName"})
    tunnel_source_interface: Union[
        OneOfInterfaceTunnelSourceInterfaceOptionsDef1,
        OneOfInterfaceTunnelSourceInterfaceOptionsDef2,
    ] = _field(metadata={"alias": "tunnelSourceInterface"})
    address: Optional[
        Union[
            OneOfInterfaceAddressOptionsDef1,
            OneOfInterfaceAddressOptionsDef2,
            OneOfInterfaceAddressOptionsDef3,
        ]
    ] = _field(default=None)
    application: Optional[OneOfInterfaceApplicationOptionsDef] = _field(default=None)
    auto: Optional[OneOfInterfaceAutoOptionsDef] = _field(default=None)
    description: Optional[
        Union[
            OneOfInterfaceDescriptionOptionsDef1,
            OneOfInterfaceDescriptionOptionsDef2,
            OneOfInterfaceDescriptionOptionsDef3,
        ]
    ] = _field(default=None)
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
    ike_local_id: Optional[
        Union[
            OneOfInterfaceIkeLocalIdOptionsDef1,
            OneOfInterfaceIkeLocalIdOptionsDef2,
            OneOfInterfaceIkeLocalIdOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ikeLocalId"})
    ike_rekey_interval: Optional[
        Union[
            OneOfInterfaceIkeRekeyIntervalOptionsDef1,
            OneOfInterfaceIkeRekeyIntervalOptionsDef2,
            OneOfInterfaceIkeRekeyIntervalOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ikeRekeyInterval"})
    ike_remote_id: Optional[
        Union[
            OneOfInterfaceIkeRemoteIdOptionsDef1,
            OneOfInterfaceIkeRemoteIdOptionsDef2,
            OneOfInterfaceIkeRemoteIdOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ikeRemoteId"})
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
    pre_shared_key_dynamic: Optional[OneOfInterfacePreSharedKeyDynamicOptionsDef] = _field(
        default=None, metadata={"alias": "preSharedKeyDynamic"}
    )
    pre_shared_secret: Optional[
        Union[
            OneOfInterfacePreSharedSecretOptionsDef1,
            OneOfInterfacePreSharedSecretOptionsDef2,
            OneOfInterfacePreSharedSecretOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "preSharedSecret"})
    shutdown: Optional[
        Union[OneOfInterfaceShutdownOptionsDef1, OneOfInterfaceShutdownOptionsDef2]
    ] = _field(default=None)
    tcp_mss_adjust: Optional[
        Union[
            OneOfInterfaceTcpMssAdjustOptionsDef1,
            OneOfInterfaceTcpMssAdjustOptionsDef2,
            OneOfInterfaceTcpMssAdjustOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tcpMssAdjust"})
    track_enable: Optional[
        Union[OneOfInterfaceTrackEnableOptionsDef1, OneOfInterfaceTrackEnableOptionsDef2]
    ] = _field(default=None, metadata={"alias": "trackEnable"})
    tracker: Optional[Union[OneOfInterfaceTrackerOptionsDef1, OneOfInterfaceTrackerOptionsDef2]] = (
        _field(default=None)
    )
    tunnel_dc_preference: Optional[OneOfInterfaceTunnelDcPreferenceOptionsDef] = _field(
        default=None, metadata={"alias": "tunnelDcPreference"}
    )
    tunnel_destination: Optional[
        Union[
            OneOfInterfaceTunnelDestinationOptionsDef1, OneOfInterfaceTunnelDestinationOptionsDef2
        ]
    ] = _field(default=None, metadata={"alias": "tunnelDestination"})
    tunnel_public_ip: Optional[
        Union[
            OneOfInterfaceTunnelPublicIpOptionsDef1,
            OneOfInterfaceTunnelPublicIpOptionsDef2,
            OneOfInterfaceTunnelPublicIpOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tunnelPublicIp"})
    tunnel_route_via: Optional[
        Union[
            OneOfInterfaceTunnelRouteViaOptionsDef1,
            OneOfInterfaceTunnelRouteViaOptionsDef2,
            OneOfInterfaceTunnelRouteViaOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tunnelRouteVia"})
    tunnel_set: Optional[OneOfInterfaceTunnelSetOptionsDef] = _field(
        default=None, metadata={"alias": "tunnelSet"}
    )
    tunnel_source: Optional[
        Union[OneOfInterfaceTunnelSourceOptionsDef1, OneOfInterfaceTunnelSourceOptionsDef2]
    ] = _field(default=None, metadata={"alias": "tunnelSource"})
    unnumbered: Optional[OneOfInterfaceUnnumberedOptionsDef] = _field(default=None)


@dataclass
class OneOfServiceInterfacePairActiveInterfaceOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfServiceInterfacePairActiveInterfaceWeightOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfServiceInterfacePairBackupInterfaceOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfServiceInterfacePairBackupInterfaceWeightOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
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
class OneOfServiceAuthRequiredOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfServiceAuthRequiredOptionsDef2:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[bool] = _field(default=None)


@dataclass
class OneOfServiceXffForwardEnabledOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfServiceXffForwardEnabledOptionsDef2:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[bool] = _field(default=None)


@dataclass
class OneOfServiceOfwEnabledOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfServiceOfwEnabledOptionsDef2:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[bool] = _field(default=None)


@dataclass
class OneOfServiceIpsControlOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfServiceIpsControlOptionsDef2:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[bool] = _field(default=None)


@dataclass
class OneOfServiceCautionEnabledOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfServiceCautionEnabledOptionsDef2:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[bool] = _field(default=None)


@dataclass
class OneOfServicePrimaryDataCenterOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfServicePrimaryDataCenterOptionsDef2:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[str] = _field(default="Auto")


@dataclass
class OneOfServicePrimaryDataCenterOptionsDef3:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfServiceSecondaryDataCenterOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfServiceSecondaryDataCenterOptionsDef2:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[str] = _field(default="Auto")


@dataclass
class OneOfServiceSecondaryDataCenterOptionsDef3:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfServiceIpOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfServiceIpOptionsDef2:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[bool] = _field(default=None)


@dataclass
class OneOfServiceIdleTimeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfServiceIdleTimeOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfServiceDisplayTimeUnitOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ServiceDisplayTimeUnitDef


@dataclass
class OneOfServiceDisplayTimeUnitOptionsDef2:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[DefaultServiceDisplayTimeUnitDef] = _field(default=None)


@dataclass
class OneOfServiceIpEnforcedForKnownBrowsersOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfServiceIpEnforcedForKnownBrowsersOptionsDef2:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[bool] = _field(default=None)


@dataclass
class OneOfServiceRefreshTimeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfServiceRefreshTimeOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfServiceRefreshTimeUnitOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ServiceRefreshTimeUnitDef


@dataclass
class OneOfServiceRefreshTimeUnitOptionsDef2:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[DefaultServiceRefreshTimeUnitDef] = _field(default=None)


@dataclass
class OneOfServiceEnabledOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfServiceEnabledOptionsDef2:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[bool] = _field(default=None)


@dataclass
class OneOfServiceBlockInternetUntilAcceptedOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfServiceBlockInternetUntilAcceptedOptionsDef2:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[bool] = _field(default=None)


@dataclass
class OneOfServiceForceSslInspectionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfServiceForceSslInspectionOptionsDef2:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[bool] = _field(default=None)


@dataclass
class OneOfServiceTimeoutOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfServiceTimeoutOptionsDef2:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=0)


@dataclass
class OneOfServiceLocationNameOptionsDef1:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[str] = _field(default="Auto")


@dataclass
class OneOfServiceLocationNameOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfServiceDataCenterPrimaryOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfServiceDataCenterPrimaryOptionsDef2:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[str] = _field(default="Auto")


@dataclass
class OneOfServiceDataCenterPrimaryOptionsDef3:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfServiceDataCenterSecondaryOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfServiceDataCenterSecondaryOptionsDef2:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[str] = _field(default="Auto")


@dataclass
class OneOfServiceDataCenterSecondaryOptionsDef3:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class Service:
    """
    Configure services
    """

    auth_required: Optional[
        Union[OneOfServiceAuthRequiredOptionsDef1, OneOfServiceAuthRequiredOptionsDef2]
    ] = _field(default=None, metadata={"alias": "authRequired"})
    block_internet_until_accepted: Optional[
        Union[
            OneOfServiceBlockInternetUntilAcceptedOptionsDef1,
            OneOfServiceBlockInternetUntilAcceptedOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "blockInternetUntilAccepted"})
    caution_enabled: Optional[
        Union[OneOfServiceCautionEnabledOptionsDef1, OneOfServiceCautionEnabledOptionsDef2]
    ] = _field(default=None, metadata={"alias": "cautionEnabled"})
    data_center_primary: Optional[
        Union[
            OneOfServiceDataCenterPrimaryOptionsDef1,
            OneOfServiceDataCenterPrimaryOptionsDef2,
            OneOfServiceDataCenterPrimaryOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "dataCenterPrimary"})
    data_center_secondary: Optional[
        Union[
            OneOfServiceDataCenterSecondaryOptionsDef1,
            OneOfServiceDataCenterSecondaryOptionsDef2,
            OneOfServiceDataCenterSecondaryOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "dataCenterSecondary"})
    display_time_unit: Optional[
        Union[OneOfServiceDisplayTimeUnitOptionsDef1, OneOfServiceDisplayTimeUnitOptionsDef2]
    ] = _field(default=None, metadata={"alias": "displayTimeUnit"})
    enabled: Optional[Union[OneOfServiceEnabledOptionsDef1, OneOfServiceEnabledOptionsDef2]] = (
        _field(default=None)
    )
    force_ssl_inspection: Optional[
        Union[OneOfServiceForceSslInspectionOptionsDef1, OneOfServiceForceSslInspectionOptionsDef2]
    ] = _field(default=None, metadata={"alias": "forceSslInspection"})
    idle_time: Optional[Union[OneOfServiceIdleTimeOptionsDef1, OneOfServiceIdleTimeOptionsDef2]] = (
        _field(default=None, metadata={"alias": "idleTime"})
    )
    # Interface Pair for active and backup
    interface_pair: Optional[List[InterfacePair]] = _field(
        default=None, metadata={"alias": "interfacePair"}
    )
    ip: Optional[Union[OneOfServiceIpOptionsDef1, OneOfServiceIpOptionsDef2]] = _field(default=None)
    ip_enforced_for_known_browsers: Optional[
        Union[
            OneOfServiceIpEnforcedForKnownBrowsersOptionsDef1,
            OneOfServiceIpEnforcedForKnownBrowsersOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "ipEnforcedForKnownBrowsers"})
    ips_control: Optional[
        Union[OneOfServiceIpsControlOptionsDef1, OneOfServiceIpsControlOptionsDef2]
    ] = _field(default=None, metadata={"alias": "ipsControl"})
    location_name: Optional[
        Union[OneOfServiceLocationNameOptionsDef1, OneOfServiceLocationNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "locationName"})
    ofw_enabled: Optional[
        Union[OneOfServiceOfwEnabledOptionsDef1, OneOfServiceOfwEnabledOptionsDef2]
    ] = _field(default=None, metadata={"alias": "ofwEnabled"})
    primary_data_center: Optional[
        Union[
            OneOfServicePrimaryDataCenterOptionsDef1,
            OneOfServicePrimaryDataCenterOptionsDef2,
            OneOfServicePrimaryDataCenterOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "primaryDataCenter"})
    refresh_time: Optional[
        Union[OneOfServiceRefreshTimeOptionsDef1, OneOfServiceRefreshTimeOptionsDef2]
    ] = _field(default=None, metadata={"alias": "refreshTime"})
    refresh_time_unit: Optional[
        Union[OneOfServiceRefreshTimeUnitOptionsDef1, OneOfServiceRefreshTimeUnitOptionsDef2]
    ] = _field(default=None, metadata={"alias": "refreshTimeUnit"})
    secondary_data_center: Optional[
        Union[
            OneOfServiceSecondaryDataCenterOptionsDef1,
            OneOfServiceSecondaryDataCenterOptionsDef2,
            OneOfServiceSecondaryDataCenterOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "secondaryDataCenter"})
    timeout: Optional[Union[OneOfServiceTimeoutOptionsDef1, OneOfServiceTimeoutOptionsDef2]] = (
        _field(default=None)
    )
    xff_forward_enabled: Optional[
        Union[OneOfServiceXffForwardEnabledOptionsDef1, OneOfServiceXffForwardEnabledOptionsDef2]
    ] = _field(default=None, metadata={"alias": "xffForwardEnabled"})


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
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfTrackerEndpointApiUrlOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfTrackerEndpointApiUrlOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTrackerThresholdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfTrackerThresholdOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTrackerThresholdOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class OneOfTrackerIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfTrackerIntervalOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTrackerIntervalOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class OneOfTrackerMultiplierOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfTrackerMultiplierOptionsDef2:
    option_type: VariableOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str
    default: Optional[str] = _field(default=None)
    description: Optional[str] = _field(default=None)


@dataclass
class OneOfTrackerMultiplierOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
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
class SigData:
    tracker_src_ip: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2] = _field(
        metadata={"alias": "trackerSrcIp"}
    )
    # Interface name: IPsec when present
    interface: Optional[List[Interface]] = _field(default=None)
    interface_metadata_sharing: Optional[InterfaceMetadataSharing] = _field(
        default=None, metadata={"alias": "interfaceMetadataSharing"}
    )
    # Configure services
    service: Optional[Service] = _field(default=None)
    sig_provider: Optional[OneOfSigProviderOptionsDef] = _field(
        default=None, metadata={"alias": "sigProvider"}
    )
    # Tracker configuration
    tracker: Optional[List[Tracker]] = _field(default=None)


@dataclass
class Payload:
    """
    SIG schema for POST request
    """

    data: SigData
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
    # SIG schema for POST request
    payload: Optional[Payload] = _field(default=None)


@dataclass
class GetListSdwanSigSecuritySigPayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateSigSecurityProfileParcel1PostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SigSecuritySigData:
    tracker_src_ip: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2] = _field(
        metadata={"alias": "trackerSrcIp"}
    )
    # Interface name: IPsec when present
    interface: Optional[List[Interface]] = _field(default=None)
    interface_metadata_sharing: Optional[InterfaceMetadataSharing] = _field(
        default=None, metadata={"alias": "interfaceMetadataSharing"}
    )
    # Configure services
    service: Optional[Service] = _field(default=None)
    sig_provider: Optional[OneOfSigProviderOptionsDef] = _field(
        default=None, metadata={"alias": "sigProvider"}
    )
    # Tracker configuration
    tracker: Optional[List[Tracker]] = _field(default=None)


@dataclass
class CreateSigSecurityProfileParcel1PostRequest:
    """
    SIG schema for POST request
    """

    data: SigSecuritySigData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class SigOneOfSigProviderOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SigSigProviderDef


@dataclass
class SigInterfaceMetadataSharing:
    src_vpn: Optional[Union[OneOfSrcVpnOptionsDef1, OneOfSrcVpnOptionsDef2]] = _field(
        default=None, metadata={"alias": "srcVpn"}
    )


@dataclass
class SigOneOfInterfaceIfNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SigOneOfInterfaceDescriptionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SigOneOfInterfaceAddressOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SigOneOfInterfaceTunnelSourceOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SigOneOfInterfaceTunnelRouteViaOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SigOneOfInterfaceTunnelRouteViaOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[str] = _field(default="")


@dataclass
class SigOneOfInterfaceTunnelDestinationOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SigOneOfInterfaceApplicationOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SigInterfaceApplicationDef


@dataclass
class SigOneOfInterfaceTunnelSetOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SigInterfaceTunnelSetDef


@dataclass
class SigOneOfInterfaceTunnelDcPreferenceOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SigInterfaceTunnelDcPreferenceDef


@dataclass
class SigOneOfInterfaceTcpMssAdjustOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SigOneOfInterfaceMtuOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SigOneOfInterfaceDpdIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SigOneOfInterfaceDpdIntervalOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class SigOneOfInterfaceDpdRetriesOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SigOneOfInterfaceDpdRetriesOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class SigOneOfInterfaceIkeVersionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SigOneOfInterfaceIkeVersionOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class SigOneOfInterfacePreSharedSecretOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SigOneOfInterfaceIkeRekeyIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SigOneOfInterfaceIkeRekeyIntervalOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class SigOneOfInterfaceIkeCiphersuiteOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SigInterfaceIkeCiphersuiteDef


@dataclass
class SigOneOfInterfaceIkeCiphersuiteOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[SigDefaultInterfaceIkeCiphersuiteDef] = _field(default=None)


@dataclass
class SigOneOfInterfaceIkeGroupOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SigInterfaceIkeGroupDef


@dataclass
class SigOneOfInterfaceIkeGroupOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[SigSecuritySigInterfaceIkeGroupDef] = _field(default="16")


@dataclass
class SigOneOfInterfaceIkeLocalIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SigOneOfInterfaceIkeRemoteIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SigOneOfInterfaceIpsecRekeyIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SigOneOfInterfaceIpsecRekeyIntervalOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class SigOneOfInterfaceIpsecReplayWindowOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SigOneOfInterfaceIpsecReplayWindowOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class SigOneOfInterfaceIpsecCiphersuiteOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SigInterfaceIpsecCiphersuiteDef


@dataclass
class SigOneOfInterfaceIpsecCiphersuiteOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[SigSecuritySigInterfaceIpsecCiphersuiteDef] = _field(
        default="aes256-cbc-sha512"
    )


@dataclass
class SigOneOfInterfacePerfectForwardSecrecyOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SigInterfacePerfectForwardSecrecyDef


@dataclass
class SigOneOfInterfacePerfectForwardSecrecyOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[SigSecuritySigInterfacePerfectForwardSecrecyDef] = _field(default="none")


@dataclass
class SigOneOfInterfaceTrackerOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SigOneOfInterfaceTunnelPublicIpOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SigOneOfInterfaceTunnelPublicIpOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[str] = _field(default="Auto")


@dataclass
class SigInterface:
    if_name: SigOneOfInterfaceIfNameOptionsDef = _field(metadata={"alias": "ifName"})
    tunnel_source_interface: Union[
        OneOfInterfaceTunnelSourceInterfaceOptionsDef1,
        OneOfInterfaceTunnelSourceInterfaceOptionsDef2,
    ] = _field(metadata={"alias": "tunnelSourceInterface"})
    address: Optional[
        Union[
            SigOneOfInterfaceAddressOptionsDef1,
            OneOfInterfaceAddressOptionsDef2,
            OneOfInterfaceAddressOptionsDef3,
        ]
    ] = _field(default=None)
    application: Optional[SigOneOfInterfaceApplicationOptionsDef] = _field(default=None)
    auto: Optional[OneOfInterfaceAutoOptionsDef] = _field(default=None)
    description: Optional[
        Union[
            SigOneOfInterfaceDescriptionOptionsDef1,
            OneOfInterfaceDescriptionOptionsDef2,
            OneOfInterfaceDescriptionOptionsDef3,
        ]
    ] = _field(default=None)
    dpd_interval: Optional[
        Union[
            SigOneOfInterfaceDpdIntervalOptionsDef1,
            OneOfInterfaceDpdIntervalOptionsDef2,
            SigOneOfInterfaceDpdIntervalOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "dpdInterval"})
    dpd_retries: Optional[
        Union[
            SigOneOfInterfaceDpdRetriesOptionsDef1,
            OneOfInterfaceDpdRetriesOptionsDef2,
            SigOneOfInterfaceDpdRetriesOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "dpdRetries"})
    ike_ciphersuite: Optional[
        Union[
            SigOneOfInterfaceIkeCiphersuiteOptionsDef1,
            OneOfInterfaceIkeCiphersuiteOptionsDef2,
            SigOneOfInterfaceIkeCiphersuiteOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ikeCiphersuite"})
    ike_group: Optional[
        Union[
            SigOneOfInterfaceIkeGroupOptionsDef1,
            OneOfInterfaceIkeGroupOptionsDef2,
            SigOneOfInterfaceIkeGroupOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ikeGroup"})
    ike_local_id: Optional[
        Union[
            SigOneOfInterfaceIkeLocalIdOptionsDef1,
            OneOfInterfaceIkeLocalIdOptionsDef2,
            OneOfInterfaceIkeLocalIdOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ikeLocalId"})
    ike_rekey_interval: Optional[
        Union[
            SigOneOfInterfaceIkeRekeyIntervalOptionsDef1,
            OneOfInterfaceIkeRekeyIntervalOptionsDef2,
            SigOneOfInterfaceIkeRekeyIntervalOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ikeRekeyInterval"})
    ike_remote_id: Optional[
        Union[
            SigOneOfInterfaceIkeRemoteIdOptionsDef1,
            OneOfInterfaceIkeRemoteIdOptionsDef2,
            OneOfInterfaceIkeRemoteIdOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ikeRemoteId"})
    ike_version: Optional[
        Union[
            SigOneOfInterfaceIkeVersionOptionsDef1,
            OneOfInterfaceIkeVersionOptionsDef2,
            SigOneOfInterfaceIkeVersionOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ikeVersion"})
    ipsec_ciphersuite: Optional[
        Union[
            SigOneOfInterfaceIpsecCiphersuiteOptionsDef1,
            OneOfInterfaceIpsecCiphersuiteOptionsDef2,
            SigOneOfInterfaceIpsecCiphersuiteOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ipsecCiphersuite"})
    ipsec_rekey_interval: Optional[
        Union[
            SigOneOfInterfaceIpsecRekeyIntervalOptionsDef1,
            OneOfInterfaceIpsecRekeyIntervalOptionsDef2,
            SigOneOfInterfaceIpsecRekeyIntervalOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ipsecRekeyInterval"})
    ipsec_replay_window: Optional[
        Union[
            SigOneOfInterfaceIpsecReplayWindowOptionsDef1,
            OneOfInterfaceIpsecReplayWindowOptionsDef2,
            SigOneOfInterfaceIpsecReplayWindowOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ipsecReplayWindow"})
    mtu: Optional[Union[SigOneOfInterfaceMtuOptionsDef1, OneOfInterfaceMtuOptionsDef2]] = _field(
        default=None
    )
    perfect_forward_secrecy: Optional[
        Union[
            SigOneOfInterfacePerfectForwardSecrecyOptionsDef1,
            OneOfInterfacePerfectForwardSecrecyOptionsDef2,
            SigOneOfInterfacePerfectForwardSecrecyOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "perfectForwardSecrecy"})
    pre_shared_key_dynamic: Optional[OneOfInterfacePreSharedKeyDynamicOptionsDef] = _field(
        default=None, metadata={"alias": "preSharedKeyDynamic"}
    )
    pre_shared_secret: Optional[
        Union[
            SigOneOfInterfacePreSharedSecretOptionsDef1,
            OneOfInterfacePreSharedSecretOptionsDef2,
            OneOfInterfacePreSharedSecretOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "preSharedSecret"})
    shutdown: Optional[
        Union[OneOfInterfaceShutdownOptionsDef1, OneOfInterfaceShutdownOptionsDef2]
    ] = _field(default=None)
    tcp_mss_adjust: Optional[
        Union[
            SigOneOfInterfaceTcpMssAdjustOptionsDef1,
            OneOfInterfaceTcpMssAdjustOptionsDef2,
            OneOfInterfaceTcpMssAdjustOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tcpMssAdjust"})
    track_enable: Optional[
        Union[OneOfInterfaceTrackEnableOptionsDef1, OneOfInterfaceTrackEnableOptionsDef2]
    ] = _field(default=None, metadata={"alias": "trackEnable"})
    tracker: Optional[
        Union[SigOneOfInterfaceTrackerOptionsDef1, OneOfInterfaceTrackerOptionsDef2]
    ] = _field(default=None)
    tunnel_dc_preference: Optional[SigOneOfInterfaceTunnelDcPreferenceOptionsDef] = _field(
        default=None, metadata={"alias": "tunnelDcPreference"}
    )
    tunnel_destination: Optional[
        Union[
            SigOneOfInterfaceTunnelDestinationOptionsDef1,
            OneOfInterfaceTunnelDestinationOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "tunnelDestination"})
    tunnel_public_ip: Optional[
        Union[
            SigOneOfInterfaceTunnelPublicIpOptionsDef1,
            OneOfInterfaceTunnelPublicIpOptionsDef2,
            SigOneOfInterfaceTunnelPublicIpOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tunnelPublicIp"})
    tunnel_route_via: Optional[
        Union[
            SigOneOfInterfaceTunnelRouteViaOptionsDef1,
            OneOfInterfaceTunnelRouteViaOptionsDef2,
            SigOneOfInterfaceTunnelRouteViaOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tunnelRouteVia"})
    tunnel_set: Optional[SigOneOfInterfaceTunnelSetOptionsDef] = _field(
        default=None, metadata={"alias": "tunnelSet"}
    )
    tunnel_source: Optional[
        Union[SigOneOfInterfaceTunnelSourceOptionsDef1, OneOfInterfaceTunnelSourceOptionsDef2]
    ] = _field(default=None, metadata={"alias": "tunnelSource"})
    unnumbered: Optional[OneOfInterfaceUnnumberedOptionsDef] = _field(default=None)


@dataclass
class SigOneOfServiceInterfacePairActiveInterfaceOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SigOneOfServiceInterfacePairActiveInterfaceWeightOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SigOneOfServiceInterfacePairBackupInterfaceOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SigOneOfServiceInterfacePairBackupInterfaceWeightOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SigInterfacePair:
    active_interface: SigOneOfServiceInterfacePairActiveInterfaceOptionsDef = _field(
        metadata={"alias": "activeInterface"}
    )
    backup_interface: SigOneOfServiceInterfacePairBackupInterfaceOptionsDef = _field(
        metadata={"alias": "backupInterface"}
    )
    active_interface_weight: Optional[
        SigOneOfServiceInterfacePairActiveInterfaceWeightOptionsDef
    ] = _field(default=None, metadata={"alias": "activeInterfaceWeight"})
    backup_interface_weight: Optional[
        SigOneOfServiceInterfacePairBackupInterfaceWeightOptionsDef
    ] = _field(default=None, metadata={"alias": "backupInterfaceWeight"})


@dataclass
class SigOneOfServicePrimaryDataCenterOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SigOneOfServicePrimaryDataCenterOptionsDef2:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[str] = _field(default="Auto")


@dataclass
class SigOneOfServiceSecondaryDataCenterOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SigOneOfServiceSecondaryDataCenterOptionsDef2:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[str] = _field(default="Auto")


@dataclass
class SigOneOfServiceIdleTimeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SigOneOfServiceIdleTimeOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SigOneOfServiceDisplayTimeUnitOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SigServiceDisplayTimeUnitDef


@dataclass
class SigOneOfServiceDisplayTimeUnitOptionsDef2:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[SigDefaultServiceDisplayTimeUnitDef] = _field(default=None)


@dataclass
class SigOneOfServiceRefreshTimeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SigOneOfServiceRefreshTimeOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SigOneOfServiceRefreshTimeUnitOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SigServiceRefreshTimeUnitDef


@dataclass
class SigOneOfServiceRefreshTimeUnitOptionsDef2:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[SigDefaultServiceRefreshTimeUnitDef] = _field(default=None)


@dataclass
class SigOneOfServiceTimeoutOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SigOneOfServiceTimeoutOptionsDef2:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=0)


@dataclass
class SigOneOfServiceLocationNameOptionsDef1:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[str] = _field(default="Auto")


@dataclass
class SigOneOfServiceDataCenterPrimaryOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SigOneOfServiceDataCenterPrimaryOptionsDef2:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[str] = _field(default="Auto")


@dataclass
class SigOneOfServiceDataCenterSecondaryOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SigOneOfServiceDataCenterSecondaryOptionsDef2:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[str] = _field(default="Auto")


@dataclass
class SigService:
    """
    Configure services
    """

    auth_required: Optional[
        Union[OneOfServiceAuthRequiredOptionsDef1, OneOfServiceAuthRequiredOptionsDef2]
    ] = _field(default=None, metadata={"alias": "authRequired"})
    block_internet_until_accepted: Optional[
        Union[
            OneOfServiceBlockInternetUntilAcceptedOptionsDef1,
            OneOfServiceBlockInternetUntilAcceptedOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "blockInternetUntilAccepted"})
    caution_enabled: Optional[
        Union[OneOfServiceCautionEnabledOptionsDef1, OneOfServiceCautionEnabledOptionsDef2]
    ] = _field(default=None, metadata={"alias": "cautionEnabled"})
    data_center_primary: Optional[
        Union[
            SigOneOfServiceDataCenterPrimaryOptionsDef1,
            SigOneOfServiceDataCenterPrimaryOptionsDef2,
            OneOfServiceDataCenterPrimaryOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "dataCenterPrimary"})
    data_center_secondary: Optional[
        Union[
            SigOneOfServiceDataCenterSecondaryOptionsDef1,
            SigOneOfServiceDataCenterSecondaryOptionsDef2,
            OneOfServiceDataCenterSecondaryOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "dataCenterSecondary"})
    display_time_unit: Optional[
        Union[SigOneOfServiceDisplayTimeUnitOptionsDef1, SigOneOfServiceDisplayTimeUnitOptionsDef2]
    ] = _field(default=None, metadata={"alias": "displayTimeUnit"})
    enabled: Optional[Union[OneOfServiceEnabledOptionsDef1, OneOfServiceEnabledOptionsDef2]] = (
        _field(default=None)
    )
    force_ssl_inspection: Optional[
        Union[OneOfServiceForceSslInspectionOptionsDef1, OneOfServiceForceSslInspectionOptionsDef2]
    ] = _field(default=None, metadata={"alias": "forceSslInspection"})
    idle_time: Optional[
        Union[SigOneOfServiceIdleTimeOptionsDef1, SigOneOfServiceIdleTimeOptionsDef2]
    ] = _field(default=None, metadata={"alias": "idleTime"})
    # Interface Pair for active and backup
    interface_pair: Optional[List[SigInterfacePair]] = _field(
        default=None, metadata={"alias": "interfacePair"}
    )
    ip: Optional[Union[OneOfServiceIpOptionsDef1, OneOfServiceIpOptionsDef2]] = _field(default=None)
    ip_enforced_for_known_browsers: Optional[
        Union[
            OneOfServiceIpEnforcedForKnownBrowsersOptionsDef1,
            OneOfServiceIpEnforcedForKnownBrowsersOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "ipEnforcedForKnownBrowsers"})
    ips_control: Optional[
        Union[OneOfServiceIpsControlOptionsDef1, OneOfServiceIpsControlOptionsDef2]
    ] = _field(default=None, metadata={"alias": "ipsControl"})
    location_name: Optional[
        Union[SigOneOfServiceLocationNameOptionsDef1, OneOfServiceLocationNameOptionsDef2]
    ] = _field(default=None, metadata={"alias": "locationName"})
    ofw_enabled: Optional[
        Union[OneOfServiceOfwEnabledOptionsDef1, OneOfServiceOfwEnabledOptionsDef2]
    ] = _field(default=None, metadata={"alias": "ofwEnabled"})
    primary_data_center: Optional[
        Union[
            SigOneOfServicePrimaryDataCenterOptionsDef1,
            SigOneOfServicePrimaryDataCenterOptionsDef2,
            OneOfServicePrimaryDataCenterOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "primaryDataCenter"})
    refresh_time: Optional[
        Union[SigOneOfServiceRefreshTimeOptionsDef1, SigOneOfServiceRefreshTimeOptionsDef2]
    ] = _field(default=None, metadata={"alias": "refreshTime"})
    refresh_time_unit: Optional[
        Union[SigOneOfServiceRefreshTimeUnitOptionsDef1, SigOneOfServiceRefreshTimeUnitOptionsDef2]
    ] = _field(default=None, metadata={"alias": "refreshTimeUnit"})
    secondary_data_center: Optional[
        Union[
            SigOneOfServiceSecondaryDataCenterOptionsDef1,
            SigOneOfServiceSecondaryDataCenterOptionsDef2,
            OneOfServiceSecondaryDataCenterOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "secondaryDataCenter"})
    timeout: Optional[
        Union[SigOneOfServiceTimeoutOptionsDef1, SigOneOfServiceTimeoutOptionsDef2]
    ] = _field(default=None)
    xff_forward_enabled: Optional[
        Union[OneOfServiceXffForwardEnabledOptionsDef1, OneOfServiceXffForwardEnabledOptionsDef2]
    ] = _field(default=None, metadata={"alias": "xffForwardEnabled"})


@dataclass
class SigOneOfTrackerNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SigOneOfTrackerEndpointApiUrlOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SigOneOfTrackerThresholdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SigOneOfTrackerThresholdOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class SigOneOfTrackerIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SigOneOfTrackerIntervalOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class SigOneOfTrackerMultiplierOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SigOneOfTrackerMultiplierOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class SigOneOfTrackerTrackerTypeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SigTrackerTrackerTypeDef


@dataclass
class SigTracker:
    endpoint_api_url: Union[
        SigOneOfTrackerEndpointApiUrlOptionsDef1, OneOfTrackerEndpointApiUrlOptionsDef2
    ] = _field(metadata={"alias": "endpointApiUrl"})
    name: SigOneOfTrackerNameOptionsDef
    tracker_type: SigOneOfTrackerTrackerTypeOptionsDef = _field(metadata={"alias": "trackerType"})
    interval: Optional[
        Union[
            SigOneOfTrackerIntervalOptionsDef1,
            OneOfTrackerIntervalOptionsDef2,
            SigOneOfTrackerIntervalOptionsDef3,
        ]
    ] = _field(default=None)
    multiplier: Optional[
        Union[
            SigOneOfTrackerMultiplierOptionsDef1,
            OneOfTrackerMultiplierOptionsDef2,
            SigOneOfTrackerMultiplierOptionsDef3,
        ]
    ] = _field(default=None)
    threshold: Optional[
        Union[
            SigOneOfTrackerThresholdOptionsDef1,
            OneOfTrackerThresholdOptionsDef2,
            SigOneOfTrackerThresholdOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class SdwanSigSecuritySigData:
    tracker_src_ip: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2] = _field(
        metadata={"alias": "trackerSrcIp"}
    )
    # Interface name: IPsec when present
    interface: Optional[List[SigInterface]] = _field(default=None)
    interface_metadata_sharing: Optional[SigInterfaceMetadataSharing] = _field(
        default=None, metadata={"alias": "interfaceMetadataSharing"}
    )
    # Configure services
    service: Optional[SigService] = _field(default=None)
    sig_provider: Optional[SigOneOfSigProviderOptionsDef] = _field(
        default=None, metadata={"alias": "sigProvider"}
    )
    # Tracker configuration
    tracker: Optional[List[SigTracker]] = _field(default=None)


@dataclass
class SigPayload:
    """
    SIG schema for PUT request
    """

    data: SdwanSigSecuritySigData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)


@dataclass
class GetSingleSdwanSigSecuritySigPayload:
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
    # SIG schema for PUT request
    payload: Optional[SigPayload] = _field(default=None)


@dataclass
class EditSigSecurityProfileParcel1PutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class SigSecuritySigOneOfSigProviderOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SigSecuritySigSigProviderDef


@dataclass
class SigSecuritySigInterfaceMetadataSharing:
    src_vpn: Optional[Union[OneOfSrcVpnOptionsDef1, OneOfSrcVpnOptionsDef2]] = _field(
        default=None, metadata={"alias": "srcVpn"}
    )


@dataclass
class SigSecuritySigOneOfInterfaceIfNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SigSecuritySigOneOfInterfaceDescriptionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SigSecuritySigOneOfInterfaceAddressOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SigSecuritySigOneOfInterfaceTunnelSourceOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SigSecuritySigOneOfInterfaceTunnelRouteViaOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SigSecuritySigOneOfInterfaceTunnelRouteViaOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[str] = _field(default="")


@dataclass
class SigSecuritySigOneOfInterfaceTunnelDestinationOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SigSecuritySigOneOfInterfaceApplicationOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SigSecuritySigInterfaceApplicationDef


@dataclass
class SigSecuritySigOneOfInterfaceTunnelSetOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SigSecuritySigInterfaceTunnelSetDef


@dataclass
class SigSecuritySigOneOfInterfaceTunnelDcPreferenceOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SigSecuritySigInterfaceTunnelDcPreferenceDef


@dataclass
class SigSecuritySigOneOfInterfaceTcpMssAdjustOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SigSecuritySigOneOfInterfaceMtuOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SigSecuritySigOneOfInterfaceDpdIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SigSecuritySigOneOfInterfaceDpdIntervalOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class SigSecuritySigOneOfInterfaceDpdRetriesOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SigSecuritySigOneOfInterfaceDpdRetriesOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class SigSecuritySigOneOfInterfaceIkeVersionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SigSecuritySigOneOfInterfaceIkeVersionOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class SigSecuritySigOneOfInterfacePreSharedSecretOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SigSecuritySigOneOfInterfaceIkeRekeyIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SigSecuritySigOneOfInterfaceIkeRekeyIntervalOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class SigSecuritySigOneOfInterfaceIkeCiphersuiteOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SigSecuritySigInterfaceIkeCiphersuiteDef


@dataclass
class SigSecuritySigOneOfInterfaceIkeCiphersuiteOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[SigSecuritySigDefaultInterfaceIkeCiphersuiteDef] = _field(default=None)


@dataclass
class SigSecuritySigOneOfInterfaceIkeGroupOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SdwanSigSecuritySigInterfaceIkeGroupDef


@dataclass
class SigSecuritySigOneOfInterfaceIkeGroupOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[FeatureProfileSdwanSigSecuritySigInterfaceIkeGroupDef] = _field(default="16")


@dataclass
class SigSecuritySigOneOfInterfaceIkeLocalIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SigSecuritySigOneOfInterfaceIkeRemoteIdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SigSecuritySigOneOfInterfaceIpsecRekeyIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SigSecuritySigOneOfInterfaceIpsecRekeyIntervalOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class SigSecuritySigOneOfInterfaceIpsecReplayWindowOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SigSecuritySigOneOfInterfaceIpsecReplayWindowOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class SigSecuritySigOneOfInterfaceIpsecCiphersuiteOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SdwanSigSecuritySigInterfaceIpsecCiphersuiteDef


@dataclass
class SigSecuritySigOneOfInterfaceIpsecCiphersuiteOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[FeatureProfileSdwanSigSecuritySigInterfaceIpsecCiphersuiteDef] = _field(
        default="aes256-cbc-sha512"
    )


@dataclass
class SigSecuritySigOneOfInterfacePerfectForwardSecrecyOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SdwanSigSecuritySigInterfacePerfectForwardSecrecyDef


@dataclass
class SigSecuritySigOneOfInterfacePerfectForwardSecrecyOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[FeatureProfileSdwanSigSecuritySigInterfacePerfectForwardSecrecyDef] = _field(
        default="none"
    )


@dataclass
class SigSecuritySigOneOfInterfaceTrackerOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SigSecuritySigOneOfInterfaceTunnelPublicIpOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SigSecuritySigOneOfInterfaceTunnelPublicIpOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[str] = _field(default="Auto")


@dataclass
class SigSecuritySigInterface:
    if_name: SigSecuritySigOneOfInterfaceIfNameOptionsDef = _field(metadata={"alias": "ifName"})
    tunnel_source_interface: Union[
        OneOfInterfaceTunnelSourceInterfaceOptionsDef1,
        OneOfInterfaceTunnelSourceInterfaceOptionsDef2,
    ] = _field(metadata={"alias": "tunnelSourceInterface"})
    address: Optional[
        Union[
            SigSecuritySigOneOfInterfaceAddressOptionsDef1,
            OneOfInterfaceAddressOptionsDef2,
            OneOfInterfaceAddressOptionsDef3,
        ]
    ] = _field(default=None)
    application: Optional[SigSecuritySigOneOfInterfaceApplicationOptionsDef] = _field(default=None)
    auto: Optional[OneOfInterfaceAutoOptionsDef] = _field(default=None)
    description: Optional[
        Union[
            SigSecuritySigOneOfInterfaceDescriptionOptionsDef1,
            OneOfInterfaceDescriptionOptionsDef2,
            OneOfInterfaceDescriptionOptionsDef3,
        ]
    ] = _field(default=None)
    dpd_interval: Optional[
        Union[
            SigSecuritySigOneOfInterfaceDpdIntervalOptionsDef1,
            OneOfInterfaceDpdIntervalOptionsDef2,
            SigSecuritySigOneOfInterfaceDpdIntervalOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "dpdInterval"})
    dpd_retries: Optional[
        Union[
            SigSecuritySigOneOfInterfaceDpdRetriesOptionsDef1,
            OneOfInterfaceDpdRetriesOptionsDef2,
            SigSecuritySigOneOfInterfaceDpdRetriesOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "dpdRetries"})
    ike_ciphersuite: Optional[
        Union[
            SigSecuritySigOneOfInterfaceIkeCiphersuiteOptionsDef1,
            OneOfInterfaceIkeCiphersuiteOptionsDef2,
            SigSecuritySigOneOfInterfaceIkeCiphersuiteOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ikeCiphersuite"})
    ike_group: Optional[
        Union[
            SigSecuritySigOneOfInterfaceIkeGroupOptionsDef1,
            OneOfInterfaceIkeGroupOptionsDef2,
            SigSecuritySigOneOfInterfaceIkeGroupOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ikeGroup"})
    ike_local_id: Optional[
        Union[
            SigSecuritySigOneOfInterfaceIkeLocalIdOptionsDef1,
            OneOfInterfaceIkeLocalIdOptionsDef2,
            OneOfInterfaceIkeLocalIdOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ikeLocalId"})
    ike_rekey_interval: Optional[
        Union[
            SigSecuritySigOneOfInterfaceIkeRekeyIntervalOptionsDef1,
            OneOfInterfaceIkeRekeyIntervalOptionsDef2,
            SigSecuritySigOneOfInterfaceIkeRekeyIntervalOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ikeRekeyInterval"})
    ike_remote_id: Optional[
        Union[
            SigSecuritySigOneOfInterfaceIkeRemoteIdOptionsDef1,
            OneOfInterfaceIkeRemoteIdOptionsDef2,
            OneOfInterfaceIkeRemoteIdOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ikeRemoteId"})
    ike_version: Optional[
        Union[
            SigSecuritySigOneOfInterfaceIkeVersionOptionsDef1,
            OneOfInterfaceIkeVersionOptionsDef2,
            SigSecuritySigOneOfInterfaceIkeVersionOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ikeVersion"})
    ipsec_ciphersuite: Optional[
        Union[
            SigSecuritySigOneOfInterfaceIpsecCiphersuiteOptionsDef1,
            OneOfInterfaceIpsecCiphersuiteOptionsDef2,
            SigSecuritySigOneOfInterfaceIpsecCiphersuiteOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ipsecCiphersuite"})
    ipsec_rekey_interval: Optional[
        Union[
            SigSecuritySigOneOfInterfaceIpsecRekeyIntervalOptionsDef1,
            OneOfInterfaceIpsecRekeyIntervalOptionsDef2,
            SigSecuritySigOneOfInterfaceIpsecRekeyIntervalOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ipsecRekeyInterval"})
    ipsec_replay_window: Optional[
        Union[
            SigSecuritySigOneOfInterfaceIpsecReplayWindowOptionsDef1,
            OneOfInterfaceIpsecReplayWindowOptionsDef2,
            SigSecuritySigOneOfInterfaceIpsecReplayWindowOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "ipsecReplayWindow"})
    mtu: Optional[
        Union[SigSecuritySigOneOfInterfaceMtuOptionsDef1, OneOfInterfaceMtuOptionsDef2]
    ] = _field(default=None)
    perfect_forward_secrecy: Optional[
        Union[
            SigSecuritySigOneOfInterfacePerfectForwardSecrecyOptionsDef1,
            OneOfInterfacePerfectForwardSecrecyOptionsDef2,
            SigSecuritySigOneOfInterfacePerfectForwardSecrecyOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "perfectForwardSecrecy"})
    pre_shared_key_dynamic: Optional[OneOfInterfacePreSharedKeyDynamicOptionsDef] = _field(
        default=None, metadata={"alias": "preSharedKeyDynamic"}
    )
    pre_shared_secret: Optional[
        Union[
            SigSecuritySigOneOfInterfacePreSharedSecretOptionsDef1,
            OneOfInterfacePreSharedSecretOptionsDef2,
            OneOfInterfacePreSharedSecretOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "preSharedSecret"})
    shutdown: Optional[
        Union[OneOfInterfaceShutdownOptionsDef1, OneOfInterfaceShutdownOptionsDef2]
    ] = _field(default=None)
    tcp_mss_adjust: Optional[
        Union[
            SigSecuritySigOneOfInterfaceTcpMssAdjustOptionsDef1,
            OneOfInterfaceTcpMssAdjustOptionsDef2,
            OneOfInterfaceTcpMssAdjustOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tcpMssAdjust"})
    track_enable: Optional[
        Union[OneOfInterfaceTrackEnableOptionsDef1, OneOfInterfaceTrackEnableOptionsDef2]
    ] = _field(default=None, metadata={"alias": "trackEnable"})
    tracker: Optional[
        Union[SigSecuritySigOneOfInterfaceTrackerOptionsDef1, OneOfInterfaceTrackerOptionsDef2]
    ] = _field(default=None)
    tunnel_dc_preference: Optional[SigSecuritySigOneOfInterfaceTunnelDcPreferenceOptionsDef] = (
        _field(default=None, metadata={"alias": "tunnelDcPreference"})
    )
    tunnel_destination: Optional[
        Union[
            SigSecuritySigOneOfInterfaceTunnelDestinationOptionsDef1,
            OneOfInterfaceTunnelDestinationOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "tunnelDestination"})
    tunnel_public_ip: Optional[
        Union[
            SigSecuritySigOneOfInterfaceTunnelPublicIpOptionsDef1,
            OneOfInterfaceTunnelPublicIpOptionsDef2,
            SigSecuritySigOneOfInterfaceTunnelPublicIpOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tunnelPublicIp"})
    tunnel_route_via: Optional[
        Union[
            SigSecuritySigOneOfInterfaceTunnelRouteViaOptionsDef1,
            OneOfInterfaceTunnelRouteViaOptionsDef2,
            SigSecuritySigOneOfInterfaceTunnelRouteViaOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "tunnelRouteVia"})
    tunnel_set: Optional[SigSecuritySigOneOfInterfaceTunnelSetOptionsDef] = _field(
        default=None, metadata={"alias": "tunnelSet"}
    )
    tunnel_source: Optional[
        Union[
            SigSecuritySigOneOfInterfaceTunnelSourceOptionsDef1,
            OneOfInterfaceTunnelSourceOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "tunnelSource"})
    unnumbered: Optional[OneOfInterfaceUnnumberedOptionsDef] = _field(default=None)


@dataclass
class SigSecuritySigOneOfServiceInterfacePairActiveInterfaceOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SigSecuritySigOneOfServiceInterfacePairActiveInterfaceWeightOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SigSecuritySigOneOfServiceInterfacePairBackupInterfaceOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SigSecuritySigOneOfServiceInterfacePairBackupInterfaceWeightOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SigSecuritySigInterfacePair:
    active_interface: SigSecuritySigOneOfServiceInterfacePairActiveInterfaceOptionsDef = _field(
        metadata={"alias": "activeInterface"}
    )
    backup_interface: SigSecuritySigOneOfServiceInterfacePairBackupInterfaceOptionsDef = _field(
        metadata={"alias": "backupInterface"}
    )
    active_interface_weight: Optional[
        SigSecuritySigOneOfServiceInterfacePairActiveInterfaceWeightOptionsDef
    ] = _field(default=None, metadata={"alias": "activeInterfaceWeight"})
    backup_interface_weight: Optional[
        SigSecuritySigOneOfServiceInterfacePairBackupInterfaceWeightOptionsDef
    ] = _field(default=None, metadata={"alias": "backupInterfaceWeight"})


@dataclass
class SigSecuritySigOneOfServicePrimaryDataCenterOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SigSecuritySigOneOfServicePrimaryDataCenterOptionsDef2:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[str] = _field(default="Auto")


@dataclass
class SigSecuritySigOneOfServiceSecondaryDataCenterOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SigSecuritySigOneOfServiceSecondaryDataCenterOptionsDef2:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[str] = _field(default="Auto")


@dataclass
class SigSecuritySigOneOfServiceIdleTimeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SigSecuritySigOneOfServiceIdleTimeOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SigSecuritySigOneOfServiceDisplayTimeUnitOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SigSecuritySigServiceDisplayTimeUnitDef


@dataclass
class SigSecuritySigOneOfServiceDisplayTimeUnitOptionsDef2:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[SigSecuritySigDefaultServiceDisplayTimeUnitDef] = _field(default=None)


@dataclass
class SigSecuritySigOneOfServiceRefreshTimeOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SigSecuritySigOneOfServiceRefreshTimeOptionsDef2:
    option_type: DefaultOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SigSecuritySigOneOfServiceRefreshTimeUnitOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SigSecuritySigServiceRefreshTimeUnitDef


@dataclass
class SigSecuritySigOneOfServiceRefreshTimeUnitOptionsDef2:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[SigSecuritySigDefaultServiceRefreshTimeUnitDef] = _field(default=None)


@dataclass
class SigSecuritySigOneOfServiceTimeoutOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SigSecuritySigOneOfServiceTimeoutOptionsDef2:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=0)


@dataclass
class SigSecuritySigOneOfServiceLocationNameOptionsDef1:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[str] = _field(default="Auto")


@dataclass
class SigSecuritySigOneOfServiceDataCenterPrimaryOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SigSecuritySigOneOfServiceDataCenterPrimaryOptionsDef2:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[str] = _field(default="Auto")


@dataclass
class SigSecuritySigOneOfServiceDataCenterSecondaryOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SigSecuritySigOneOfServiceDataCenterSecondaryOptionsDef2:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[str] = _field(default="Auto")


@dataclass
class SigSecuritySigService:
    """
    Configure services
    """

    auth_required: Optional[
        Union[OneOfServiceAuthRequiredOptionsDef1, OneOfServiceAuthRequiredOptionsDef2]
    ] = _field(default=None, metadata={"alias": "authRequired"})
    block_internet_until_accepted: Optional[
        Union[
            OneOfServiceBlockInternetUntilAcceptedOptionsDef1,
            OneOfServiceBlockInternetUntilAcceptedOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "blockInternetUntilAccepted"})
    caution_enabled: Optional[
        Union[OneOfServiceCautionEnabledOptionsDef1, OneOfServiceCautionEnabledOptionsDef2]
    ] = _field(default=None, metadata={"alias": "cautionEnabled"})
    data_center_primary: Optional[
        Union[
            SigSecuritySigOneOfServiceDataCenterPrimaryOptionsDef1,
            SigSecuritySigOneOfServiceDataCenterPrimaryOptionsDef2,
            OneOfServiceDataCenterPrimaryOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "dataCenterPrimary"})
    data_center_secondary: Optional[
        Union[
            SigSecuritySigOneOfServiceDataCenterSecondaryOptionsDef1,
            SigSecuritySigOneOfServiceDataCenterSecondaryOptionsDef2,
            OneOfServiceDataCenterSecondaryOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "dataCenterSecondary"})
    display_time_unit: Optional[
        Union[
            SigSecuritySigOneOfServiceDisplayTimeUnitOptionsDef1,
            SigSecuritySigOneOfServiceDisplayTimeUnitOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "displayTimeUnit"})
    enabled: Optional[Union[OneOfServiceEnabledOptionsDef1, OneOfServiceEnabledOptionsDef2]] = (
        _field(default=None)
    )
    force_ssl_inspection: Optional[
        Union[OneOfServiceForceSslInspectionOptionsDef1, OneOfServiceForceSslInspectionOptionsDef2]
    ] = _field(default=None, metadata={"alias": "forceSslInspection"})
    idle_time: Optional[
        Union[
            SigSecuritySigOneOfServiceIdleTimeOptionsDef1,
            SigSecuritySigOneOfServiceIdleTimeOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "idleTime"})
    # Interface Pair for active and backup
    interface_pair: Optional[List[SigSecuritySigInterfacePair]] = _field(
        default=None, metadata={"alias": "interfacePair"}
    )
    ip: Optional[Union[OneOfServiceIpOptionsDef1, OneOfServiceIpOptionsDef2]] = _field(default=None)
    ip_enforced_for_known_browsers: Optional[
        Union[
            OneOfServiceIpEnforcedForKnownBrowsersOptionsDef1,
            OneOfServiceIpEnforcedForKnownBrowsersOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "ipEnforcedForKnownBrowsers"})
    ips_control: Optional[
        Union[OneOfServiceIpsControlOptionsDef1, OneOfServiceIpsControlOptionsDef2]
    ] = _field(default=None, metadata={"alias": "ipsControl"})
    location_name: Optional[
        Union[
            SigSecuritySigOneOfServiceLocationNameOptionsDef1, OneOfServiceLocationNameOptionsDef2
        ]
    ] = _field(default=None, metadata={"alias": "locationName"})
    ofw_enabled: Optional[
        Union[OneOfServiceOfwEnabledOptionsDef1, OneOfServiceOfwEnabledOptionsDef2]
    ] = _field(default=None, metadata={"alias": "ofwEnabled"})
    primary_data_center: Optional[
        Union[
            SigSecuritySigOneOfServicePrimaryDataCenterOptionsDef1,
            SigSecuritySigOneOfServicePrimaryDataCenterOptionsDef2,
            OneOfServicePrimaryDataCenterOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "primaryDataCenter"})
    refresh_time: Optional[
        Union[
            SigSecuritySigOneOfServiceRefreshTimeOptionsDef1,
            SigSecuritySigOneOfServiceRefreshTimeOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "refreshTime"})
    refresh_time_unit: Optional[
        Union[
            SigSecuritySigOneOfServiceRefreshTimeUnitOptionsDef1,
            SigSecuritySigOneOfServiceRefreshTimeUnitOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "refreshTimeUnit"})
    secondary_data_center: Optional[
        Union[
            SigSecuritySigOneOfServiceSecondaryDataCenterOptionsDef1,
            SigSecuritySigOneOfServiceSecondaryDataCenterOptionsDef2,
            OneOfServiceSecondaryDataCenterOptionsDef3,
        ]
    ] = _field(default=None, metadata={"alias": "secondaryDataCenter"})
    timeout: Optional[
        Union[
            SigSecuritySigOneOfServiceTimeoutOptionsDef1,
            SigSecuritySigOneOfServiceTimeoutOptionsDef2,
        ]
    ] = _field(default=None)
    xff_forward_enabled: Optional[
        Union[OneOfServiceXffForwardEnabledOptionsDef1, OneOfServiceXffForwardEnabledOptionsDef2]
    ] = _field(default=None, metadata={"alias": "xffForwardEnabled"})


@dataclass
class SigSecuritySigOneOfTrackerNameOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SigSecuritySigOneOfTrackerEndpointApiUrlOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SigSecuritySigOneOfTrackerThresholdOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SigSecuritySigOneOfTrackerThresholdOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class SigSecuritySigOneOfTrackerIntervalOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SigSecuritySigOneOfTrackerIntervalOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class SigSecuritySigOneOfTrackerMultiplierOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class SigSecuritySigOneOfTrackerMultiplierOptionsDef3:
    option_type: Optional[DefaultOptionTypeDef] = _field(
        default=None, metadata={"alias": "optionType"}
    )
    value: Optional[int] = _field(default=None)


@dataclass
class SigSecuritySigOneOfTrackerTrackerTypeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SigSecuritySigTrackerTrackerTypeDef


@dataclass
class SigSecuritySigTracker:
    endpoint_api_url: Union[
        SigSecuritySigOneOfTrackerEndpointApiUrlOptionsDef1, OneOfTrackerEndpointApiUrlOptionsDef2
    ] = _field(metadata={"alias": "endpointApiUrl"})
    name: SigSecuritySigOneOfTrackerNameOptionsDef
    tracker_type: SigSecuritySigOneOfTrackerTrackerTypeOptionsDef = _field(
        metadata={"alias": "trackerType"}
    )
    interval: Optional[
        Union[
            SigSecuritySigOneOfTrackerIntervalOptionsDef1,
            OneOfTrackerIntervalOptionsDef2,
            SigSecuritySigOneOfTrackerIntervalOptionsDef3,
        ]
    ] = _field(default=None)
    multiplier: Optional[
        Union[
            SigSecuritySigOneOfTrackerMultiplierOptionsDef1,
            OneOfTrackerMultiplierOptionsDef2,
            SigSecuritySigOneOfTrackerMultiplierOptionsDef3,
        ]
    ] = _field(default=None)
    threshold: Optional[
        Union[
            SigSecuritySigOneOfTrackerThresholdOptionsDef1,
            OneOfTrackerThresholdOptionsDef2,
            SigSecuritySigOneOfTrackerThresholdOptionsDef3,
        ]
    ] = _field(default=None)


@dataclass
class FeatureProfileSdwanSigSecuritySigData:
    tracker_src_ip: Union[OneOfIpV4AddressOptionsDef1, OneOfIpV4AddressOptionsDef2] = _field(
        metadata={"alias": "trackerSrcIp"}
    )
    # Interface name: IPsec when present
    interface: Optional[List[SigSecuritySigInterface]] = _field(default=None)
    interface_metadata_sharing: Optional[SigSecuritySigInterfaceMetadataSharing] = _field(
        default=None, metadata={"alias": "interfaceMetadataSharing"}
    )
    # Configure services
    service: Optional[SigSecuritySigService] = _field(default=None)
    sig_provider: Optional[SigSecuritySigOneOfSigProviderOptionsDef] = _field(
        default=None, metadata={"alias": "sigProvider"}
    )
    # Tracker configuration
    tracker: Optional[List[SigSecuritySigTracker]] = _field(default=None)


@dataclass
class EditSigSecurityProfileParcel1PutRequest:
    """
    SIG schema for PUT request
    """

    data: FeatureProfileSdwanSigSecuritySigData
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)
    name: Optional[str] = _field(default=None)
