# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

TlsDecryptionActionDef = Literal["decrypt", "neverDecrypt", "skipDecrypt"]

SignatureSetDef = Literal["balanced", "connectivity", "security"]

InspectionModeDef = Literal["detection", "protection"]

LogLevelDef = Literal[
    "alert", "critical", "debug", "emergency", "error", "info", "notice", "warning"
]

WebCategoriesActionDef = Literal["allow", "block"]

WebCategoriesDef = Literal[
    "abortion",
    "abused-drugs",
    "adult-and-pornography",
    "alcohol-and-tobacco",
    "auctions",
    "bot-nets",
    "business-and-economy",
    "cdns",
    "cheating",
    "computer-and-internet-info",
    "computer-and-internet-security",
    "confirmed-spam-sources",
    "cult-and-occult",
    "dating",
    "dead-sites",
    "dns-over-https",
    "dynamic-content",
    "educational-institutions",
    "entertainment-and-arts",
    "fashion-and-beauty",
    "financial-services",
    "gambling",
    "games",
    "generative-ai",
    "government",
    "gross",
    "hacking",
    "hate-and-racism",
    "health-and-medicine",
    "home",
    "hunting-and-fishing",
    "illegal",
    "image-and-video-search",
    "individual-stock-advice-and-tools",
    "internet-communications",
    "internet-portals",
    "job-search",
    "keyloggers-and-monitoring",
    "kids",
    "legal",
    "local-information",
    "low-thc-cannabis-products",
    "malware-sites",
    "marijuana",
    "military",
    "motor-vehicles",
    "music",
    "news-and-media",
    "nudity",
    "online-greeting-cards",
    "online-personal-storage",
    "open-http-proxies",
    "p2p",
    "parked-sites",
    "pay-to-surf",
    "personal-sites-and-blogs",
    "philosophy-and-political-advocacy",
    "phishing-and-other-frauds",
    "private-ip-addresses",
    "proxy-avoid-and-anonymizers",
    "questionable",
    "real-estate",
    "recreation-and-hobbies",
    "reference-and-research",
    "religion",
    "search-engines",
    "self-harm",
    "sex-education",
    "shareware-and-freeware",
    "shopping",
    "social-network",
    "society",
    "spam-urls",
    "sports",
    "spyware-and-adware",
    "streaming-media",
    "swimsuits-and-intimate-apparel",
    "training-and-tools",
    "translation",
    "travel",
    "uncategorized",
    "unconfirmed-spam-sources",
    "unused-food-and-dining",
    "unused-reputation",
    "violence",
    "weapons",
    "web-advertisements",
    "web-based-email",
    "web-hosting",
]

WebReputationDef = Literal["high-risk", "low-risk", "moderate-risk", "suspicious", "trustworthy"]

BlockPageActionDef = Literal["redirect-url", "text"]

AlertsDef = Literal["blacklist", "categories-reputation", "whitelist"]

ServerDef = Literal["apjc", "eur", "nam"]

AlertDef = Literal["critical", "info", "warning"]

FileAnalysisCloudServerDef = Literal["eur", "nam"]

CategoriesDef = Literal[
    "abortion",
    "abused-drugs",
    "adult-and-pornography",
    "alcohol-and-tobacco",
    "auctions",
    "bot-nets",
    "business-and-economy",
    "cdns",
    "cheating",
    "computer-and-internet-info",
    "computer-and-internet-security",
    "confirmed-spam-sources",
    "cult-and-occult",
    "dating",
    "dead-sites",
    "dns-over-https",
    "dynamic-content",
    "educational-institutions",
    "entertainment-and-arts",
    "fashion-and-beauty",
    "financial-services",
    "gambling",
    "games",
    "generative-ai",
    "government",
    "gross",
    "hacking",
    "hate-and-racism",
    "health-and-medicine",
    "home",
    "hunting-and-fishing",
    "illegal",
    "image-and-video-search",
    "individual-stock-advice-and-tools",
    "internet-communications",
    "internet-portals",
    "job-search",
    "keyloggers-and-monitoring",
    "kids",
    "legal",
    "local-information",
    "low-thc-cannabis-products",
    "malware-sites",
    "marijuana",
    "military",
    "motor-vehicles",
    "music",
    "news-and-media",
    "nudity",
    "online-greeting-cards",
    "online-personal-storage",
    "open-http-proxies",
    "p2p",
    "parked-sites",
    "pay-to-surf",
    "personal-sites-and-blogs",
    "philosophy-and-political-advocacy",
    "phishing-and-other-frauds",
    "private-ip-addresses",
    "proxy-avoid-and-anonymizers",
    "questionable",
    "real-estate",
    "recreation-and-hobbies",
    "reference-and-research",
    "religion",
    "search-engines",
    "self-harm",
    "sex-education",
    "shareware-and-freeware",
    "shopping",
    "social-network",
    "society",
    "spam-urls",
    "sports",
    "spyware-and-adware",
    "streaming-media",
    "swimsuits-and-intimate-apparel",
    "training-and-tools",
    "translation",
    "travel",
    "uncategorized",
    "unconfirmed-spam-sources",
    "unused-food-and-dining",
    "unused-reputation",
    "violence",
    "weapons",
    "web-advertisements",
    "web-based-email",
    "web-hosting",
]

ThresholdDef = Literal["high-risk", "low-risk", "moderate-risk", "suspicious", "trustworthy"]

DecryptAndDropStringDef = Literal["decrypt", "drop"]

CertificateRevocationStatusDef = Literal["none", "ocsp"]

NoDecryptAndDropStringDef = Literal["drop", "no-decrypt"]

FailureModeDef = Literal["close", "open"]

KeyModulusDef = Literal["1024", "2048", "4096"]

EckeyTypeDef = Literal["P256", "P384", "P521"]

MinTlsVerDef = Literal["TLSv1", "TLSv1.1", "TLSv1.2"]

CaTpLabelDef = Literal["PROXY-SIGNING-CA"]

SecurityProfileParcelTypeParam = Literal[
    "advanced-inspection-profile",
    "advanced-malware-protection",
    "intrusion-prevention",
    "ssl-decryption",
    "ssl-decryption-profile",
    "url-filtering",
]

UnifiedTlsDecryptionActionDef = Literal["decrypt", "neverDecrypt", "skipDecrypt"]

PolicyObjectUnifiedTlsDecryptionActionDef = Literal["decrypt", "neverDecrypt", "skipDecrypt"]

SdwanPolicyObjectUnifiedTlsDecryptionActionDef = Literal["decrypt", "neverDecrypt", "skipDecrypt"]

UnifiedSignatureSetDef = Literal["balanced", "connectivity", "security"]

UnifiedInspectionModeDef = Literal["detection", "protection"]

UnifiedLogLevelDef = Literal[
    "alert", "critical", "debug", "emergency", "error", "info", "notice", "warning"
]

UnifiedWebCategoriesActionDef = Literal["allow", "block"]

UnifiedWebReputationDef = Literal[
    "high-risk", "low-risk", "moderate-risk", "suspicious", "trustworthy"
]

UnifiedBlockPageActionDef = Literal["redirect-url", "text"]

UnifiedServerDef = Literal["apjc", "eur", "nam"]

PolicyObjectUnifiedServerDef = Literal["apjc", "eur", "nam"]

UnifiedAlertDef = Literal["critical", "info", "warning"]

UnifiedFileAnalysisCloudServerDef = Literal["eur", "nam"]

PolicyObjectUnifiedAlertDef = Literal["critical", "info", "warning"]

UnifiedThresholdDef = Literal["high-risk", "low-risk", "moderate-risk", "suspicious", "trustworthy"]

PolicyObjectUnifiedThresholdDef = Literal[
    "high-risk", "low-risk", "moderate-risk", "suspicious", "trustworthy"
]

UnifiedDecryptAndDropStringDef = Literal["decrypt", "drop"]

PolicyObjectUnifiedDecryptAndDropStringDef = Literal["decrypt", "drop"]

UnifiedCertificateRevocationStatusDef = Literal["none", "ocsp"]

SdwanPolicyObjectUnifiedDecryptAndDropStringDef = Literal["decrypt", "drop"]

UnifiedNoDecryptAndDropStringDef = Literal["drop", "no-decrypt"]

PolicyObjectUnifiedNoDecryptAndDropStringDef = Literal["drop", "no-decrypt"]

UnifiedFailureModeDef = Literal["close", "open"]

UnifiedKeyModulusDef = Literal["1024", "2048", "4096"]

UnifiedEckeyTypeDef = Literal["P256", "P384", "P521"]

UnifiedMinTlsVerDef = Literal["TLSv1", "TLSv1.1", "TLSv1.2"]

UnifiedCaTpLabelDef = Literal["PROXY-SIGNING-CA"]

FeatureProfileSdwanPolicyObjectUnifiedTlsDecryptionActionDef = Literal[
    "decrypt", "neverDecrypt", "skipDecrypt"
]

V1FeatureProfileSdwanPolicyObjectUnifiedTlsDecryptionActionDef = Literal[
    "decrypt", "neverDecrypt", "skipDecrypt"
]

TlsDecryptionActionDef1 = Literal["decrypt", "neverDecrypt", "skipDecrypt"]

PolicyObjectUnifiedSignatureSetDef = Literal["balanced", "connectivity", "security"]

PolicyObjectUnifiedInspectionModeDef = Literal["detection", "protection"]

PolicyObjectUnifiedLogLevelDef = Literal[
    "alert", "critical", "debug", "emergency", "error", "info", "notice", "warning"
]

PolicyObjectUnifiedWebCategoriesActionDef = Literal["allow", "block"]

PolicyObjectUnifiedWebReputationDef = Literal[
    "high-risk", "low-risk", "moderate-risk", "suspicious", "trustworthy"
]

PolicyObjectUnifiedBlockPageActionDef = Literal["redirect-url", "text"]

SdwanPolicyObjectUnifiedServerDef = Literal["apjc", "eur", "nam"]

FeatureProfileSdwanPolicyObjectUnifiedServerDef = Literal["apjc", "eur", "nam"]

SdwanPolicyObjectUnifiedAlertDef = Literal["critical", "info", "warning"]

PolicyObjectUnifiedFileAnalysisCloudServerDef = Literal["eur", "nam"]

FeatureProfileSdwanPolicyObjectUnifiedAlertDef = Literal["critical", "info", "warning"]

SdwanPolicyObjectUnifiedThresholdDef = Literal[
    "high-risk", "low-risk", "moderate-risk", "suspicious", "trustworthy"
]

FeatureProfileSdwanPolicyObjectUnifiedThresholdDef = Literal[
    "high-risk", "low-risk", "moderate-risk", "suspicious", "trustworthy"
]

FeatureProfileSdwanPolicyObjectUnifiedDecryptAndDropStringDef = Literal["decrypt", "drop"]

V1FeatureProfileSdwanPolicyObjectUnifiedDecryptAndDropStringDef = Literal["decrypt", "drop"]

PolicyObjectUnifiedCertificateRevocationStatusDef = Literal["none", "ocsp"]

DecryptAndDropStringDef1 = Literal["decrypt", "drop"]

SdwanPolicyObjectUnifiedNoDecryptAndDropStringDef = Literal["drop", "no-decrypt"]

FeatureProfileSdwanPolicyObjectUnifiedNoDecryptAndDropStringDef = Literal["drop", "no-decrypt"]

PolicyObjectUnifiedFailureModeDef = Literal["close", "open"]

PolicyObjectUnifiedKeyModulusDef = Literal["1024", "2048", "4096"]

PolicyObjectUnifiedEckeyTypeDef = Literal["P256", "P384", "P521"]

PolicyObjectUnifiedMinTlsVerDef = Literal["TLSv1", "TLSv1.1", "TLSv1.2"]

PolicyObjectUnifiedCaTpLabelDef = Literal["PROXY-SIGNING-CA"]


@dataclass
class OneOfTlsDecryptionActionOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: TlsDecryptionActionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class RefIdDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ReferenceDef:
    ref_id: RefIdDef = _field(metadata={"alias": "refId"})


@dataclass
class Data1:
    intrusion_prevention: ReferenceDef = _field(metadata={"alias": "intrusionPrevention"})
    tls_decryption_action: OneOfTlsDecryptionActionOptionsDef = _field(
        metadata={"alias": "tlsDecryptionAction"}
    )
    advanced_malware_protection: Optional[ReferenceDef] = _field(
        default=None, metadata={"alias": "advancedMalwareProtection"}
    )
    ssl_decryption_profile: Optional[ReferenceDef] = _field(
        default=None, metadata={"alias": "sslDecryptionProfile"}
    )
    url_filtering: Optional[ReferenceDef] = _field(default=None, metadata={"alias": "urlFiltering"})


@dataclass
class Data2:
    tls_decryption_action: OneOfTlsDecryptionActionOptionsDef = _field(
        metadata={"alias": "tlsDecryptionAction"}
    )
    url_filtering: ReferenceDef = _field(metadata={"alias": "urlFiltering"})
    advanced_malware_protection: Optional[ReferenceDef] = _field(
        default=None, metadata={"alias": "advancedMalwareProtection"}
    )
    intrusion_prevention: Optional[ReferenceDef] = _field(
        default=None, metadata={"alias": "intrusionPrevention"}
    )
    ssl_decryption_profile: Optional[ReferenceDef] = _field(
        default=None, metadata={"alias": "sslDecryptionProfile"}
    )


@dataclass
class Data3:
    advanced_malware_protection: ReferenceDef = _field(
        metadata={"alias": "advancedMalwareProtection"}
    )
    tls_decryption_action: OneOfTlsDecryptionActionOptionsDef = _field(
        metadata={"alias": "tlsDecryptionAction"}
    )
    intrusion_prevention: Optional[ReferenceDef] = _field(
        default=None, metadata={"alias": "intrusionPrevention"}
    )
    ssl_decryption_profile: Optional[ReferenceDef] = _field(
        default=None, metadata={"alias": "sslDecryptionProfile"}
    )
    url_filtering: Optional[ReferenceDef] = _field(default=None, metadata={"alias": "urlFiltering"})


@dataclass
class Schema2HubGeneratedSecurityprofileparceltypePost1:
    """
    advanced-malware-protection profile parcel schema for POST request
    """

    # requires tlsDecryptionAction and at least one of Intrusion Prevention or URL Filtering or Advanced Malware Protection policies
    data: Union[Data1, Data2, Data3]
    description: str
    name: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class OneOfSignatureSetOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SignatureSetDef


@dataclass
class OneOfInspectionModeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: InspectionModeDef


@dataclass
class RefIdOptionDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SignatureAllowedList:
    """
    Valid UUID
    """

    ref_id: Optional[RefIdOptionDef] = _field(default=None, metadata={"alias": "refId"})


@dataclass
class OneOfLogLevelOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: LogLevelDef


@dataclass
class OneOfCustomSignatureOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class UnifiedData:
    inspection_mode: OneOfInspectionModeOptionsDef = _field(metadata={"alias": "inspectionMode"})
    log_level: OneOfLogLevelOptionsDef = _field(metadata={"alias": "logLevel"})
    signature_set: OneOfSignatureSetOptionsDef = _field(metadata={"alias": "signatureSet"})
    custom_signature: Optional[OneOfCustomSignatureOptionsDef] = _field(
        default=None, metadata={"alias": "customSignature"}
    )
    # Valid UUID
    signature_allowed_list: Optional[SignatureAllowedList] = _field(
        default=None, metadata={"alias": "signatureAllowedList"}
    )


@dataclass
class Schema2HubGeneratedSecurityprofileparceltypePost2:
    """
    Intrusion Prevention profile parcel schema for POST request
    """

    data: UnifiedData
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class OneOfWebCategoriesActionOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: WebCategoriesActionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfWebCategoriesOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[WebCategoriesDef]  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfWebReputationOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: WebReputationDef  # pytype: disable=annotation-type-mismatch


@dataclass
class UrlAllowedList:
    ref_id: Optional[RefIdOptionDef] = _field(default=None, metadata={"alias": "refId"})


@dataclass
class UrlBlockedList:
    ref_id: Optional[RefIdOptionDef] = _field(default=None, metadata={"alias": "refId"})


@dataclass
class OneOfBlockPageActionOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: BlockPageActionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfBlockPageContentsOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfRedirectUrlOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfEnableAlertsOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfAlertsOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[AlertsDef]  # pytype: disable=annotation-type-mismatch


@dataclass
class PolicyObjectUnifiedData:
    block_page_action: OneOfBlockPageActionOptionsDef = _field(
        metadata={"alias": "blockPageAction"}
    )
    enable_alerts: OneOfEnableAlertsOptionsDef = _field(metadata={"alias": "enableAlerts"})
    web_categories_action: OneOfWebCategoriesActionOptionsDef = _field(
        metadata={"alias": "webCategoriesAction"}
    )
    web_reputation: OneOfWebReputationOptionsDef = _field(metadata={"alias": "webReputation"})
    alerts: Optional[OneOfAlertsOptionsDef] = _field(default=None)
    block_page_contents: Optional[OneOfBlockPageContentsOptionsDef] = _field(
        default=None, metadata={"alias": "blockPageContents"}
    )
    redirect_url: Optional[OneOfRedirectUrlOptionsDef] = _field(
        default=None, metadata={"alias": "redirectUrl"}
    )
    url_allowed_list: Optional[UrlAllowedList] = _field(
        default=None, metadata={"alias": "urlAllowedList"}
    )
    url_blocked_list: Optional[UrlBlockedList] = _field(
        default=None, metadata={"alias": "urlBlockedList"}
    )
    web_categories: Optional[OneOfWebCategoriesOptionsDef] = _field(
        default=None, metadata={"alias": "webCategories"}
    )


@dataclass
class Schema2HubGeneratedSecurityprofileparceltypePost3:
    """
    url-filtering profile parcel schema for POST request
    """

    data: PolicyObjectUnifiedData
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class OneOfMatchAllVpnOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: Any


@dataclass
class OneOfFileReputationCloudServerOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ServerDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfFileReputationEstServerOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ServerDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfFileReputationAlertOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: AlertDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfFileAnalysisEnabledOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfFileAnalysisCloudServerOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: FileAnalysisCloudServerDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfFileAnalysisFileTypesOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class OneOfFileAnalysisAlertOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: AlertDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SdwanPolicyObjectUnifiedData:
    file_analysis_enabled: OneOfFileAnalysisEnabledOptionsDef = _field(
        metadata={"alias": "fileAnalysisEnabled"}
    )
    file_reputation_alert: OneOfFileReputationAlertOptionsDef = _field(
        metadata={"alias": "fileReputationAlert"}
    )
    file_reputation_cloud_server: OneOfFileReputationCloudServerOptionsDef = _field(
        metadata={"alias": "fileReputationCloudServer"}
    )
    file_reputation_est_server: OneOfFileReputationEstServerOptionsDef = _field(
        metadata={"alias": "fileReputationEstServer"}
    )
    match_all_vpn: OneOfMatchAllVpnOptionsDef = _field(metadata={"alias": "matchAllVpn"})
    file_analysis_alert: Optional[OneOfFileAnalysisAlertOptionsDef] = _field(
        default=None, metadata={"alias": "fileAnalysisAlert"}
    )
    file_analysis_cloud_server: Optional[OneOfFileAnalysisCloudServerOptionsDef] = _field(
        default=None, metadata={"alias": "fileAnalysisCloudServer"}
    )
    file_analysis_file_types: Optional[OneOfFileAnalysisFileTypesOptionsDef] = _field(
        default=None, metadata={"alias": "fileAnalysisFileTypes"}
    )


@dataclass
class Schema2HubGeneratedSecurityprofileparceltypePost4:
    """
    advanced-malware-protection profile parcel schema for POST request
    """

    data: SdwanPolicyObjectUnifiedData
    description: str
    name: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class OneOfDecryptCategoriesOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[CategoriesDef]  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfNeverDecryptCategoriesOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[CategoriesDef]  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfSkipDecryptCategoriesOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[CategoriesDef]  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfReputationOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfDecryptThresholdOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ThresholdDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfSkipDecryptThresholdOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: ThresholdDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfFailDecryptOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class FeatureProfileSdwanPolicyObjectUnifiedData:
    decrypt_categories: OneOfDecryptCategoriesOptionsDef = _field(
        metadata={"alias": "decryptCategories"}
    )
    fail_decrypt: OneOfFailDecryptOptionsDef = _field(metadata={"alias": "failDecrypt"})
    never_decrypt_categories: OneOfNeverDecryptCategoriesOptionsDef = _field(
        metadata={"alias": "neverDecryptCategories"}
    )
    reputation: OneOfReputationOptionsDef
    decrypt_threshold: Optional[OneOfDecryptThresholdOptionsDef] = _field(
        default=None, metadata={"alias": "decryptThreshold"}
    )
    skip_decrypt_categories: Optional[OneOfSkipDecryptCategoriesOptionsDef] = _field(
        default=None, metadata={"alias": "skipDecryptCategories"}
    )
    skip_decrypt_threshold: Optional[OneOfSkipDecryptThresholdOptionsDef] = _field(
        default=None, metadata={"alias": "skipDecryptThreshold"}
    )
    url_allowed_list: Optional[UrlAllowedList] = _field(
        default=None, metadata={"alias": "urlAllowedList"}
    )
    url_blocked_list: Optional[UrlBlockedList] = _field(
        default=None, metadata={"alias": "urlBlockedList"}
    )


@dataclass
class Schema2HubGeneratedSecurityprofileparceltypePost5:
    """
    ssl-decryption-profile profile parcel schema for POST request
    """

    data: FeatureProfileSdwanPolicyObjectUnifiedData
    description: str
    name: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class V1FeatureProfileSdwanPolicyObjectUnifiedData:
    ca_cert_bundle: Optional[Any] = _field(default=None, metadata={"alias": "caCertBundle"})


@dataclass
class Schema2HubGeneratedSecurityprofileparceltypePost61:
    data: V1FeatureProfileSdwanPolicyObjectUnifiedData
    # Will be auto generated
    description: str
    name: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class OneOfSslEnableOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfExpiredCertificateOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DecryptAndDropStringDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfUntrustedCertificateOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DecryptAndDropStringDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfCertificateRevocationStatusOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: CertificateRevocationStatusDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfUnknownStatusOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DecryptAndDropStringDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfUnsupportedProtocolVersionsOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: NoDecryptAndDropStringDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfUnsupportedCipherSuitesOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: NoDecryptAndDropStringDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfFailureModeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: FailureModeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class DefaultDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class OneOfCaCertBundleOptionsDef1:
    default: DefaultDef


@dataclass
class FileNameDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class BundleStringDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfCaCertBundleOptionsDef2:
    bundle_string: BundleStringDef = _field(metadata={"alias": "bundleString"})
    default: DefaultDef
    file_name: FileNameDef = _field(metadata={"alias": "fileName"})


@dataclass
class OneOfKeyModulusOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: KeyModulusDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfEckeyTypeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EckeyTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfCertificateLifetimeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfMinTlsVerOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: MinTlsVerDef  # pytype: disable=annotation-type-mismatch


@dataclass
class OneOfCaTpLabelOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: CaTpLabelDef  # pytype: disable=annotation-type-mismatch


@dataclass
class Data11:
    ssl_enable: OneOfSslEnableOptionsDef = _field(metadata={"alias": "sslEnable"})
    ca_cert_bundle: Optional[Union[OneOfCaCertBundleOptionsDef1, OneOfCaCertBundleOptionsDef2]] = (
        _field(default=None, metadata={"alias": "caCertBundle"})
    )
    ca_tp_label: Optional[OneOfCaTpLabelOptionsDef] = _field(
        default=None, metadata={"alias": "caTpLabel"}
    )
    certificate_lifetime: Optional[OneOfCertificateLifetimeOptionsDef] = _field(
        default=None, metadata={"alias": "certificateLifetime"}
    )
    certificate_revocation_status: Optional[OneOfCertificateRevocationStatusOptionsDef] = _field(
        default=None, metadata={"alias": "certificateRevocationStatus"}
    )
    eckey_type: Optional[OneOfEckeyTypeOptionsDef] = _field(
        default=None, metadata={"alias": "eckeyType"}
    )
    expired_certificate: Optional[OneOfExpiredCertificateOptionsDef] = _field(
        default=None, metadata={"alias": "expiredCertificate"}
    )
    failure_mode: Optional[OneOfFailureModeOptionsDef] = _field(
        default=None, metadata={"alias": "failureMode"}
    )
    key_modulus: Optional[OneOfKeyModulusOptionsDef] = _field(
        default=None, metadata={"alias": "keyModulus"}
    )
    min_tls_ver: Optional[OneOfMinTlsVerOptionsDef] = _field(
        default=None, metadata={"alias": "minTlsVer"}
    )
    unknown_status: Optional[OneOfUnknownStatusOptionsDef] = _field(
        default=None, metadata={"alias": "unknownStatus"}
    )
    unsupported_cipher_suites: Optional[OneOfUnsupportedCipherSuitesOptionsDef] = _field(
        default=None, metadata={"alias": "unsupportedCipherSuites"}
    )
    unsupported_protocol_versions: Optional[OneOfUnsupportedProtocolVersionsOptionsDef] = _field(
        default=None, metadata={"alias": "unsupportedProtocolVersions"}
    )
    untrusted_certificate: Optional[OneOfUntrustedCertificateOptionsDef] = _field(
        default=None, metadata={"alias": "untrustedCertificate"}
    )


@dataclass
class Schema2HubGeneratedSecurityprofileparceltypePost62:
    data: Data11
    # Will be auto generated
    description: str
    name: str
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
    payload: Optional[
        Union[
            Schema2HubGeneratedSecurityprofileparceltypePost1,
            Schema2HubGeneratedSecurityprofileparceltypePost2,
            Schema2HubGeneratedSecurityprofileparceltypePost3,
            Schema2HubGeneratedSecurityprofileparceltypePost4,
            Schema2HubGeneratedSecurityprofileparceltypePost5,
            Union[
                Schema2HubGeneratedSecurityprofileparceltypePost61,
                Schema2HubGeneratedSecurityprofileparceltypePost62,
            ],
        ]
    ] = _field(default=None)


@dataclass
class GetListSdwanPolicyObjectUnifiedAdvancedInspectionProfilePayload:
    data: Optional[List[Data]] = _field(default=None)


@dataclass
class CreateSdwanSecurityFeaturePostResponse:
    """
    Profile Parcel POST Response schema
    """

    parcel_id: str = _field(metadata={"alias": "parcelId"})
    metadata: Optional[Any] = _field(default=None)


@dataclass
class CreateSdwanSecurityFeaturePostRequest1:
    """
    advanced-malware-protection profile parcel schema for POST request
    """

    # requires tlsDecryptionAction and at least one of Intrusion Prevention or URL Filtering or Advanced Malware Protection policies
    data: Union[Data1, Data2, Data3]
    description: str
    name: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Data21:
    inspection_mode: OneOfInspectionModeOptionsDef = _field(metadata={"alias": "inspectionMode"})
    log_level: OneOfLogLevelOptionsDef = _field(metadata={"alias": "logLevel"})
    signature_set: OneOfSignatureSetOptionsDef = _field(metadata={"alias": "signatureSet"})
    custom_signature: Optional[OneOfCustomSignatureOptionsDef] = _field(
        default=None, metadata={"alias": "customSignature"}
    )
    # Valid UUID
    signature_allowed_list: Optional[SignatureAllowedList] = _field(
        default=None, metadata={"alias": "signatureAllowedList"}
    )


@dataclass
class CreateSdwanSecurityFeaturePostRequest2:
    """
    Intrusion Prevention profile parcel schema for POST request
    """

    data: Data21
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Data31:
    block_page_action: OneOfBlockPageActionOptionsDef = _field(
        metadata={"alias": "blockPageAction"}
    )
    enable_alerts: OneOfEnableAlertsOptionsDef = _field(metadata={"alias": "enableAlerts"})
    web_categories_action: OneOfWebCategoriesActionOptionsDef = _field(
        metadata={"alias": "webCategoriesAction"}
    )
    web_reputation: OneOfWebReputationOptionsDef = _field(metadata={"alias": "webReputation"})
    alerts: Optional[OneOfAlertsOptionsDef] = _field(default=None)
    block_page_contents: Optional[OneOfBlockPageContentsOptionsDef] = _field(
        default=None, metadata={"alias": "blockPageContents"}
    )
    redirect_url: Optional[OneOfRedirectUrlOptionsDef] = _field(
        default=None, metadata={"alias": "redirectUrl"}
    )
    url_allowed_list: Optional[UrlAllowedList] = _field(
        default=None, metadata={"alias": "urlAllowedList"}
    )
    url_blocked_list: Optional[UrlBlockedList] = _field(
        default=None, metadata={"alias": "urlBlockedList"}
    )
    web_categories: Optional[OneOfWebCategoriesOptionsDef] = _field(
        default=None, metadata={"alias": "webCategories"}
    )


@dataclass
class CreateSdwanSecurityFeaturePostRequest3:
    """
    url-filtering profile parcel schema for POST request
    """

    data: Data31
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Data4:
    file_analysis_enabled: OneOfFileAnalysisEnabledOptionsDef = _field(
        metadata={"alias": "fileAnalysisEnabled"}
    )
    file_reputation_alert: OneOfFileReputationAlertOptionsDef = _field(
        metadata={"alias": "fileReputationAlert"}
    )
    file_reputation_cloud_server: OneOfFileReputationCloudServerOptionsDef = _field(
        metadata={"alias": "fileReputationCloudServer"}
    )
    file_reputation_est_server: OneOfFileReputationEstServerOptionsDef = _field(
        metadata={"alias": "fileReputationEstServer"}
    )
    match_all_vpn: OneOfMatchAllVpnOptionsDef = _field(metadata={"alias": "matchAllVpn"})
    file_analysis_alert: Optional[OneOfFileAnalysisAlertOptionsDef] = _field(
        default=None, metadata={"alias": "fileAnalysisAlert"}
    )
    file_analysis_cloud_server: Optional[OneOfFileAnalysisCloudServerOptionsDef] = _field(
        default=None, metadata={"alias": "fileAnalysisCloudServer"}
    )
    file_analysis_file_types: Optional[OneOfFileAnalysisFileTypesOptionsDef] = _field(
        default=None, metadata={"alias": "fileAnalysisFileTypes"}
    )


@dataclass
class CreateSdwanSecurityFeaturePostRequest4:
    """
    advanced-malware-protection profile parcel schema for POST request
    """

    data: Data4
    description: str
    name: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Data5:
    decrypt_categories: OneOfDecryptCategoriesOptionsDef = _field(
        metadata={"alias": "decryptCategories"}
    )
    fail_decrypt: OneOfFailDecryptOptionsDef = _field(metadata={"alias": "failDecrypt"})
    never_decrypt_categories: OneOfNeverDecryptCategoriesOptionsDef = _field(
        metadata={"alias": "neverDecryptCategories"}
    )
    reputation: OneOfReputationOptionsDef
    decrypt_threshold: Optional[OneOfDecryptThresholdOptionsDef] = _field(
        default=None, metadata={"alias": "decryptThreshold"}
    )
    skip_decrypt_categories: Optional[OneOfSkipDecryptCategoriesOptionsDef] = _field(
        default=None, metadata={"alias": "skipDecryptCategories"}
    )
    skip_decrypt_threshold: Optional[OneOfSkipDecryptThresholdOptionsDef] = _field(
        default=None, metadata={"alias": "skipDecryptThreshold"}
    )
    url_allowed_list: Optional[UrlAllowedList] = _field(
        default=None, metadata={"alias": "urlAllowedList"}
    )
    url_blocked_list: Optional[UrlBlockedList] = _field(
        default=None, metadata={"alias": "urlBlockedList"}
    )


@dataclass
class CreateSdwanSecurityFeaturePostRequest5:
    """
    ssl-decryption-profile profile parcel schema for POST request
    """

    data: Data5
    description: str
    name: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Data6:
    ca_cert_bundle: Optional[Any] = _field(default=None, metadata={"alias": "caCertBundle"})


@dataclass
class CreateSdwanSecurityFeaturePostRequest61:
    data: Data6
    # Will be auto generated
    description: str
    name: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Data7:
    ssl_enable: OneOfSslEnableOptionsDef = _field(metadata={"alias": "sslEnable"})
    ca_cert_bundle: Optional[Union[OneOfCaCertBundleOptionsDef1, OneOfCaCertBundleOptionsDef2]] = (
        _field(default=None, metadata={"alias": "caCertBundle"})
    )
    ca_tp_label: Optional[OneOfCaTpLabelOptionsDef] = _field(
        default=None, metadata={"alias": "caTpLabel"}
    )
    certificate_lifetime: Optional[OneOfCertificateLifetimeOptionsDef] = _field(
        default=None, metadata={"alias": "certificateLifetime"}
    )
    certificate_revocation_status: Optional[OneOfCertificateRevocationStatusOptionsDef] = _field(
        default=None, metadata={"alias": "certificateRevocationStatus"}
    )
    eckey_type: Optional[OneOfEckeyTypeOptionsDef] = _field(
        default=None, metadata={"alias": "eckeyType"}
    )
    expired_certificate: Optional[OneOfExpiredCertificateOptionsDef] = _field(
        default=None, metadata={"alias": "expiredCertificate"}
    )
    failure_mode: Optional[OneOfFailureModeOptionsDef] = _field(
        default=None, metadata={"alias": "failureMode"}
    )
    key_modulus: Optional[OneOfKeyModulusOptionsDef] = _field(
        default=None, metadata={"alias": "keyModulus"}
    )
    min_tls_ver: Optional[OneOfMinTlsVerOptionsDef] = _field(
        default=None, metadata={"alias": "minTlsVer"}
    )
    unknown_status: Optional[OneOfUnknownStatusOptionsDef] = _field(
        default=None, metadata={"alias": "unknownStatus"}
    )
    unsupported_cipher_suites: Optional[OneOfUnsupportedCipherSuitesOptionsDef] = _field(
        default=None, metadata={"alias": "unsupportedCipherSuites"}
    )
    unsupported_protocol_versions: Optional[OneOfUnsupportedProtocolVersionsOptionsDef] = _field(
        default=None, metadata={"alias": "unsupportedProtocolVersions"}
    )
    untrusted_certificate: Optional[OneOfUntrustedCertificateOptionsDef] = _field(
        default=None, metadata={"alias": "untrustedCertificate"}
    )


@dataclass
class CreateSdwanSecurityFeaturePostRequest62:
    data: Data7
    # Will be auto generated
    description: str
    name: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class UnifiedOneOfTlsDecryptionActionOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: UnifiedTlsDecryptionActionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class UnifiedRefIdDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class UnifiedReferenceDef:
    ref_id: UnifiedRefIdDef = _field(metadata={"alias": "refId"})


@dataclass
class PolicyObjectUnifiedRefIdDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class PolicyObjectUnifiedReferenceDef:
    ref_id: PolicyObjectUnifiedRefIdDef = _field(metadata={"alias": "refId"})


@dataclass
class SdwanPolicyObjectUnifiedRefIdDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class SdwanPolicyObjectUnifiedReferenceDef:
    ref_id: SdwanPolicyObjectUnifiedRefIdDef = _field(metadata={"alias": "refId"})


@dataclass
class FeatureProfileSdwanPolicyObjectUnifiedRefIdDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class FeatureProfileSdwanPolicyObjectUnifiedReferenceDef:
    ref_id: FeatureProfileSdwanPolicyObjectUnifiedRefIdDef = _field(metadata={"alias": "refId"})


@dataclass
class UnifiedData1:
    intrusion_prevention: UnifiedReferenceDef = _field(metadata={"alias": "intrusionPrevention"})
    tls_decryption_action: UnifiedOneOfTlsDecryptionActionOptionsDef = _field(
        metadata={"alias": "tlsDecryptionAction"}
    )
    advanced_malware_protection: Optional[SdwanPolicyObjectUnifiedReferenceDef] = _field(
        default=None, metadata={"alias": "advancedMalwareProtection"}
    )
    ssl_decryption_profile: Optional[FeatureProfileSdwanPolicyObjectUnifiedReferenceDef] = _field(
        default=None, metadata={"alias": "sslDecryptionProfile"}
    )
    url_filtering: Optional[PolicyObjectUnifiedReferenceDef] = _field(
        default=None, metadata={"alias": "urlFiltering"}
    )


@dataclass
class PolicyObjectUnifiedOneOfTlsDecryptionActionOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: PolicyObjectUnifiedTlsDecryptionActionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class V1FeatureProfileSdwanPolicyObjectUnifiedRefIdDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class V1FeatureProfileSdwanPolicyObjectUnifiedReferenceDef:
    ref_id: V1FeatureProfileSdwanPolicyObjectUnifiedRefIdDef = _field(metadata={"alias": "refId"})


@dataclass
class RefIdDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ReferenceDef1:
    ref_id: RefIdDef1 = _field(metadata={"alias": "refId"})


@dataclass
class RefIdDef2:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ReferenceDef2:
    ref_id: RefIdDef2 = _field(metadata={"alias": "refId"})


@dataclass
class RefIdDef3:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ReferenceDef3:
    ref_id: RefIdDef3 = _field(metadata={"alias": "refId"})


@dataclass
class UnifiedData2:
    tls_decryption_action: PolicyObjectUnifiedOneOfTlsDecryptionActionOptionsDef = _field(
        metadata={"alias": "tlsDecryptionAction"}
    )
    url_filtering: ReferenceDef1 = _field(metadata={"alias": "urlFiltering"})
    advanced_malware_protection: Optional[ReferenceDef2] = _field(
        default=None, metadata={"alias": "advancedMalwareProtection"}
    )
    intrusion_prevention: Optional[V1FeatureProfileSdwanPolicyObjectUnifiedReferenceDef] = _field(
        default=None, metadata={"alias": "intrusionPrevention"}
    )
    ssl_decryption_profile: Optional[ReferenceDef3] = _field(
        default=None, metadata={"alias": "sslDecryptionProfile"}
    )


@dataclass
class SdwanPolicyObjectUnifiedOneOfTlsDecryptionActionOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: (
        SdwanPolicyObjectUnifiedTlsDecryptionActionDef  # pytype: disable=annotation-type-mismatch
    )


@dataclass
class RefIdDef4:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ReferenceDef4:
    ref_id: RefIdDef4 = _field(metadata={"alias": "refId"})


@dataclass
class RefIdDef5:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ReferenceDef5:
    ref_id: RefIdDef5 = _field(metadata={"alias": "refId"})


@dataclass
class RefIdDef6:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ReferenceDef6:
    ref_id: RefIdDef6 = _field(metadata={"alias": "refId"})


@dataclass
class RefIdDef7:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ReferenceDef7:
    ref_id: RefIdDef7 = _field(metadata={"alias": "refId"})


@dataclass
class UnifiedData3:
    advanced_malware_protection: ReferenceDef6 = _field(
        metadata={"alias": "advancedMalwareProtection"}
    )
    tls_decryption_action: SdwanPolicyObjectUnifiedOneOfTlsDecryptionActionOptionsDef = _field(
        metadata={"alias": "tlsDecryptionAction"}
    )
    intrusion_prevention: Optional[ReferenceDef4] = _field(
        default=None, metadata={"alias": "intrusionPrevention"}
    )
    ssl_decryption_profile: Optional[ReferenceDef7] = _field(
        default=None, metadata={"alias": "sslDecryptionProfile"}
    )
    url_filtering: Optional[ReferenceDef5] = _field(
        default=None, metadata={"alias": "urlFiltering"}
    )


@dataclass
class Schema2HubGeneratedSecurityprofileparceltypePut1:
    """
    advanced-malware-protection profile parcel schema for PUT request
    """

    # requires tlsDecryptionAction and at least one of Intrusion Prevention or URL Filtering or Advanced Malware Protection policies
    data: Union[UnifiedData1, UnifiedData2, UnifiedData3]
    description: str
    name: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class UnifiedOneOfSignatureSetOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: UnifiedSignatureSetDef


@dataclass
class UnifiedOneOfInspectionModeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: UnifiedInspectionModeDef


@dataclass
class UnifiedOneOfLogLevelOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: UnifiedLogLevelDef


@dataclass
class UnifiedOneOfCustomSignatureOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class Data8:
    inspection_mode: UnifiedOneOfInspectionModeOptionsDef = _field(
        metadata={"alias": "inspectionMode"}
    )
    log_level: UnifiedOneOfLogLevelOptionsDef = _field(metadata={"alias": "logLevel"})
    signature_set: UnifiedOneOfSignatureSetOptionsDef = _field(metadata={"alias": "signatureSet"})
    custom_signature: Optional[UnifiedOneOfCustomSignatureOptionsDef] = _field(
        default=None, metadata={"alias": "customSignature"}
    )
    # Valid UUID
    signature_allowed_list: Optional[SignatureAllowedList] = _field(
        default=None, metadata={"alias": "signatureAllowedList"}
    )


@dataclass
class Schema2HubGeneratedSecurityprofileparceltypePut2:
    """
    Intrusion Prevention profile parcel schema for PUT request
    """

    data: Data8
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class UnifiedOneOfWebCategoriesActionOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: UnifiedWebCategoriesActionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class UnifiedOneOfWebCategoriesOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[WebCategoriesDef]  # pytype: disable=annotation-type-mismatch


@dataclass
class UnifiedOneOfWebReputationOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: UnifiedWebReputationDef  # pytype: disable=annotation-type-mismatch


@dataclass
class UnifiedOneOfBlockPageActionOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: UnifiedBlockPageActionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class UnifiedOneOfBlockPageContentsOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class UnifiedOneOfRedirectUrlOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class UnifiedOneOfAlertsOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[AlertsDef]  # pytype: disable=annotation-type-mismatch


@dataclass
class Data9:
    block_page_action: UnifiedOneOfBlockPageActionOptionsDef = _field(
        metadata={"alias": "blockPageAction"}
    )
    enable_alerts: OneOfEnableAlertsOptionsDef = _field(metadata={"alias": "enableAlerts"})
    web_categories_action: UnifiedOneOfWebCategoriesActionOptionsDef = _field(
        metadata={"alias": "webCategoriesAction"}
    )
    web_reputation: UnifiedOneOfWebReputationOptionsDef = _field(
        metadata={"alias": "webReputation"}
    )
    alerts: Optional[UnifiedOneOfAlertsOptionsDef] = _field(default=None)
    block_page_contents: Optional[UnifiedOneOfBlockPageContentsOptionsDef] = _field(
        default=None, metadata={"alias": "blockPageContents"}
    )
    redirect_url: Optional[UnifiedOneOfRedirectUrlOptionsDef] = _field(
        default=None, metadata={"alias": "redirectUrl"}
    )
    url_allowed_list: Optional[UrlAllowedList] = _field(
        default=None, metadata={"alias": "urlAllowedList"}
    )
    url_blocked_list: Optional[UrlBlockedList] = _field(
        default=None, metadata={"alias": "urlBlockedList"}
    )
    web_categories: Optional[UnifiedOneOfWebCategoriesOptionsDef] = _field(
        default=None, metadata={"alias": "webCategories"}
    )


@dataclass
class Schema2HubGeneratedSecurityprofileparceltypePut3:
    """
    url-filtering profile parcel schema for put request
    """

    data: Data9
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class UnifiedOneOfFileReputationCloudServerOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: UnifiedServerDef  # pytype: disable=annotation-type-mismatch


@dataclass
class UnifiedOneOfFileReputationEstServerOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: PolicyObjectUnifiedServerDef  # pytype: disable=annotation-type-mismatch


@dataclass
class UnifiedOneOfFileReputationAlertOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: UnifiedAlertDef  # pytype: disable=annotation-type-mismatch


@dataclass
class UnifiedOneOfFileAnalysisCloudServerOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: UnifiedFileAnalysisCloudServerDef  # pytype: disable=annotation-type-mismatch


@dataclass
class UnifiedOneOfFileAnalysisFileTypesOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class UnifiedOneOfFileAnalysisAlertOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: PolicyObjectUnifiedAlertDef  # pytype: disable=annotation-type-mismatch


@dataclass
class Data10:
    file_analysis_enabled: OneOfFileAnalysisEnabledOptionsDef = _field(
        metadata={"alias": "fileAnalysisEnabled"}
    )
    file_reputation_alert: UnifiedOneOfFileReputationAlertOptionsDef = _field(
        metadata={"alias": "fileReputationAlert"}
    )
    file_reputation_cloud_server: UnifiedOneOfFileReputationCloudServerOptionsDef = _field(
        metadata={"alias": "fileReputationCloudServer"}
    )
    file_reputation_est_server: UnifiedOneOfFileReputationEstServerOptionsDef = _field(
        metadata={"alias": "fileReputationEstServer"}
    )
    match_all_vpn: OneOfMatchAllVpnOptionsDef = _field(metadata={"alias": "matchAllVpn"})
    file_analysis_alert: Optional[UnifiedOneOfFileAnalysisAlertOptionsDef] = _field(
        default=None, metadata={"alias": "fileAnalysisAlert"}
    )
    file_analysis_cloud_server: Optional[UnifiedOneOfFileAnalysisCloudServerOptionsDef] = _field(
        default=None, metadata={"alias": "fileAnalysisCloudServer"}
    )
    file_analysis_file_types: Optional[UnifiedOneOfFileAnalysisFileTypesOptionsDef] = _field(
        default=None, metadata={"alias": "fileAnalysisFileTypes"}
    )


@dataclass
class Schema2HubGeneratedSecurityprofileparceltypePut4:
    """
    advanced-malware-protection profile parcel schema for PUT request
    """

    data: Data10
    description: str
    name: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class UnifiedOneOfDecryptCategoriesOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[CategoriesDef]  # pytype: disable=annotation-type-mismatch


@dataclass
class UnifiedOneOfNeverDecryptCategoriesOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[CategoriesDef]  # pytype: disable=annotation-type-mismatch


@dataclass
class UnifiedOneOfSkipDecryptCategoriesOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[CategoriesDef]  # pytype: disable=annotation-type-mismatch


@dataclass
class UnifiedOneOfDecryptThresholdOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: UnifiedThresholdDef  # pytype: disable=annotation-type-mismatch


@dataclass
class UnifiedOneOfSkipDecryptThresholdOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: PolicyObjectUnifiedThresholdDef  # pytype: disable=annotation-type-mismatch


@dataclass
class Data11_1:
    decrypt_categories: UnifiedOneOfDecryptCategoriesOptionsDef = _field(
        metadata={"alias": "decryptCategories"}
    )
    fail_decrypt: OneOfFailDecryptOptionsDef = _field(metadata={"alias": "failDecrypt"})
    never_decrypt_categories: UnifiedOneOfNeverDecryptCategoriesOptionsDef = _field(
        metadata={"alias": "neverDecryptCategories"}
    )
    reputation: OneOfReputationOptionsDef
    decrypt_threshold: Optional[UnifiedOneOfDecryptThresholdOptionsDef] = _field(
        default=None, metadata={"alias": "decryptThreshold"}
    )
    skip_decrypt_categories: Optional[UnifiedOneOfSkipDecryptCategoriesOptionsDef] = _field(
        default=None, metadata={"alias": "skipDecryptCategories"}
    )
    skip_decrypt_threshold: Optional[UnifiedOneOfSkipDecryptThresholdOptionsDef] = _field(
        default=None, metadata={"alias": "skipDecryptThreshold"}
    )
    url_allowed_list: Optional[UrlAllowedList] = _field(
        default=None, metadata={"alias": "urlAllowedList"}
    )
    url_blocked_list: Optional[UrlBlockedList] = _field(
        default=None, metadata={"alias": "urlBlockedList"}
    )


@dataclass
class Schema2HubGeneratedSecurityprofileparceltypePut5:
    """
    ssl-decryption-profile profile parcel schema for put request
    """

    data: Data11_1
    description: str
    name: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Data12:
    ca_cert_bundle: Optional[Any] = _field(default=None, metadata={"alias": "caCertBundle"})


@dataclass
class Schema2HubGeneratedSecurityprofileparceltypePut61:
    data: Data12
    # Will be auto generated
    description: str
    name: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class UnifiedOneOfExpiredCertificateOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: UnifiedDecryptAndDropStringDef  # pytype: disable=annotation-type-mismatch


@dataclass
class UnifiedOneOfUntrustedCertificateOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: PolicyObjectUnifiedDecryptAndDropStringDef  # pytype: disable=annotation-type-mismatch


@dataclass
class UnifiedOneOfCertificateRevocationStatusOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: UnifiedCertificateRevocationStatusDef  # pytype: disable=annotation-type-mismatch


@dataclass
class UnifiedOneOfUnknownStatusOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: (
        SdwanPolicyObjectUnifiedDecryptAndDropStringDef  # pytype: disable=annotation-type-mismatch
    )


@dataclass
class UnifiedOneOfUnsupportedProtocolVersionsOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: UnifiedNoDecryptAndDropStringDef  # pytype: disable=annotation-type-mismatch


@dataclass
class UnifiedOneOfUnsupportedCipherSuitesOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: PolicyObjectUnifiedNoDecryptAndDropStringDef  # pytype: disable=annotation-type-mismatch


@dataclass
class UnifiedOneOfFailureModeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: UnifiedFailureModeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class UnifiedDefaultDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class UnifiedOneOfCaCertBundleOptionsDef1:
    default: UnifiedDefaultDef


@dataclass
class PolicyObjectUnifiedDefaultDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class UnifiedFileNameDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class UnifiedBundleStringDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class UnifiedOneOfCaCertBundleOptionsDef2:
    bundle_string: UnifiedBundleStringDef = _field(metadata={"alias": "bundleString"})
    default: PolicyObjectUnifiedDefaultDef
    file_name: UnifiedFileNameDef = _field(metadata={"alias": "fileName"})


@dataclass
class UnifiedOneOfKeyModulusOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: UnifiedKeyModulusDef  # pytype: disable=annotation-type-mismatch


@dataclass
class UnifiedOneOfEckeyTypeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: UnifiedEckeyTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class UnifiedOneOfCertificateLifetimeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class UnifiedOneOfMinTlsVerOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: UnifiedMinTlsVerDef  # pytype: disable=annotation-type-mismatch


@dataclass
class UnifiedOneOfCaTpLabelOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: UnifiedCaTpLabelDef  # pytype: disable=annotation-type-mismatch


@dataclass
class Data13:
    ssl_enable: OneOfSslEnableOptionsDef = _field(metadata={"alias": "sslEnable"})
    ca_cert_bundle: Optional[
        Union[UnifiedOneOfCaCertBundleOptionsDef1, UnifiedOneOfCaCertBundleOptionsDef2]
    ] = _field(default=None, metadata={"alias": "caCertBundle"})
    ca_tp_label: Optional[UnifiedOneOfCaTpLabelOptionsDef] = _field(
        default=None, metadata={"alias": "caTpLabel"}
    )
    certificate_lifetime: Optional[UnifiedOneOfCertificateLifetimeOptionsDef] = _field(
        default=None, metadata={"alias": "certificateLifetime"}
    )
    certificate_revocation_status: Optional[UnifiedOneOfCertificateRevocationStatusOptionsDef] = (
        _field(default=None, metadata={"alias": "certificateRevocationStatus"})
    )
    eckey_type: Optional[UnifiedOneOfEckeyTypeOptionsDef] = _field(
        default=None, metadata={"alias": "eckeyType"}
    )
    expired_certificate: Optional[UnifiedOneOfExpiredCertificateOptionsDef] = _field(
        default=None, metadata={"alias": "expiredCertificate"}
    )
    failure_mode: Optional[UnifiedOneOfFailureModeOptionsDef] = _field(
        default=None, metadata={"alias": "failureMode"}
    )
    key_modulus: Optional[UnifiedOneOfKeyModulusOptionsDef] = _field(
        default=None, metadata={"alias": "keyModulus"}
    )
    min_tls_ver: Optional[UnifiedOneOfMinTlsVerOptionsDef] = _field(
        default=None, metadata={"alias": "minTlsVer"}
    )
    unknown_status: Optional[UnifiedOneOfUnknownStatusOptionsDef] = _field(
        default=None, metadata={"alias": "unknownStatus"}
    )
    unsupported_cipher_suites: Optional[UnifiedOneOfUnsupportedCipherSuitesOptionsDef] = _field(
        default=None, metadata={"alias": "unsupportedCipherSuites"}
    )
    unsupported_protocol_versions: Optional[UnifiedOneOfUnsupportedProtocolVersionsOptionsDef] = (
        _field(default=None, metadata={"alias": "unsupportedProtocolVersions"})
    )
    untrusted_certificate: Optional[UnifiedOneOfUntrustedCertificateOptionsDef] = _field(
        default=None, metadata={"alias": "untrustedCertificate"}
    )


@dataclass
class Schema2HubGeneratedSecurityprofileparceltypePut62:
    data: Data13
    # Will be auto generated
    description: str
    name: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetSingleSdwanPolicyObjectUnifiedAdvancedInspectionProfilePayload:
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
    payload: Optional[
        Union[
            Schema2HubGeneratedSecurityprofileparceltypePut1,
            Schema2HubGeneratedSecurityprofileparceltypePut2,
            Schema2HubGeneratedSecurityprofileparceltypePut3,
            Schema2HubGeneratedSecurityprofileparceltypePut4,
            Schema2HubGeneratedSecurityprofileparceltypePut5,
            Union[
                Schema2HubGeneratedSecurityprofileparceltypePut61,
                Schema2HubGeneratedSecurityprofileparceltypePut62,
            ],
        ]
    ] = _field(default=None)


@dataclass
class EditSdwanSecurityFeature1PutResponse:
    """
    Profile Parcel PUT Response schema
    """

    id: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class FeatureProfileSdwanPolicyObjectUnifiedOneOfTlsDecryptionActionOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: FeatureProfileSdwanPolicyObjectUnifiedTlsDecryptionActionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class RefIdDef8:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ReferenceDef8:
    ref_id: RefIdDef8 = _field(metadata={"alias": "refId"})


@dataclass
class RefIdDef9:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ReferenceDef9:
    ref_id: RefIdDef9 = _field(metadata={"alias": "refId"})


@dataclass
class RefIdDef10:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ReferenceDef10:
    ref_id: RefIdDef10 = _field(metadata={"alias": "refId"})


@dataclass
class RefIdDef11:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ReferenceDef11:
    ref_id: RefIdDef11 = _field(metadata={"alias": "refId"})


@dataclass
class PolicyObjectUnifiedData1:
    intrusion_prevention: ReferenceDef8 = _field(metadata={"alias": "intrusionPrevention"})
    tls_decryption_action: FeatureProfileSdwanPolicyObjectUnifiedOneOfTlsDecryptionActionOptionsDef = _field(
        metadata={"alias": "tlsDecryptionAction"}
    )
    advanced_malware_protection: Optional[ReferenceDef10] = _field(
        default=None, metadata={"alias": "advancedMalwareProtection"}
    )
    ssl_decryption_profile: Optional[ReferenceDef11] = _field(
        default=None, metadata={"alias": "sslDecryptionProfile"}
    )
    url_filtering: Optional[ReferenceDef9] = _field(
        default=None, metadata={"alias": "urlFiltering"}
    )


@dataclass
class V1FeatureProfileSdwanPolicyObjectUnifiedOneOfTlsDecryptionActionOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: V1FeatureProfileSdwanPolicyObjectUnifiedTlsDecryptionActionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class RefIdDef12:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ReferenceDef12:
    ref_id: RefIdDef12 = _field(metadata={"alias": "refId"})


@dataclass
class RefIdDef13:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ReferenceDef13:
    ref_id: RefIdDef13 = _field(metadata={"alias": "refId"})


@dataclass
class RefIdDef14:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ReferenceDef14:
    ref_id: RefIdDef14 = _field(metadata={"alias": "refId"})


@dataclass
class RefIdDef15:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ReferenceDef15:
    ref_id: RefIdDef15 = _field(metadata={"alias": "refId"})


@dataclass
class PolicyObjectUnifiedData2:
    tls_decryption_action: V1FeatureProfileSdwanPolicyObjectUnifiedOneOfTlsDecryptionActionOptionsDef = _field(
        metadata={"alias": "tlsDecryptionAction"}
    )
    url_filtering: ReferenceDef13 = _field(metadata={"alias": "urlFiltering"})
    advanced_malware_protection: Optional[ReferenceDef14] = _field(
        default=None, metadata={"alias": "advancedMalwareProtection"}
    )
    intrusion_prevention: Optional[ReferenceDef12] = _field(
        default=None, metadata={"alias": "intrusionPrevention"}
    )
    ssl_decryption_profile: Optional[ReferenceDef15] = _field(
        default=None, metadata={"alias": "sslDecryptionProfile"}
    )


@dataclass
class OneOfTlsDecryptionActionOptionsDef1:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: TlsDecryptionActionDef1  # pytype: disable=annotation-type-mismatch


@dataclass
class RefIdDef16:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ReferenceDef16:
    ref_id: RefIdDef16 = _field(metadata={"alias": "refId"})


@dataclass
class RefIdDef17:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ReferenceDef17:
    ref_id: RefIdDef17 = _field(metadata={"alias": "refId"})


@dataclass
class RefIdDef18:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ReferenceDef18:
    ref_id: RefIdDef18 = _field(metadata={"alias": "refId"})


@dataclass
class RefIdDef19:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ReferenceDef19:
    ref_id: RefIdDef19 = _field(metadata={"alias": "refId"})


@dataclass
class PolicyObjectUnifiedData3:
    advanced_malware_protection: ReferenceDef18 = _field(
        metadata={"alias": "advancedMalwareProtection"}
    )
    tls_decryption_action: OneOfTlsDecryptionActionOptionsDef1 = _field(
        metadata={"alias": "tlsDecryptionAction"}
    )
    intrusion_prevention: Optional[ReferenceDef16] = _field(
        default=None, metadata={"alias": "intrusionPrevention"}
    )
    ssl_decryption_profile: Optional[ReferenceDef19] = _field(
        default=None, metadata={"alias": "sslDecryptionProfile"}
    )
    url_filtering: Optional[ReferenceDef17] = _field(
        default=None, metadata={"alias": "urlFiltering"}
    )


@dataclass
class EditSdwanSecurityFeature1PutRequest1:
    """
    advanced-malware-protection profile parcel schema for PUT request
    """

    # requires tlsDecryptionAction and at least one of Intrusion Prevention or URL Filtering or Advanced Malware Protection policies
    data: Union[PolicyObjectUnifiedData1, PolicyObjectUnifiedData2, PolicyObjectUnifiedData3]
    description: str
    name: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class PolicyObjectUnifiedOneOfSignatureSetOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: PolicyObjectUnifiedSignatureSetDef


@dataclass
class PolicyObjectUnifiedOneOfInspectionModeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: PolicyObjectUnifiedInspectionModeDef


@dataclass
class PolicyObjectUnifiedOneOfLogLevelOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: PolicyObjectUnifiedLogLevelDef


@dataclass
class PolicyObjectUnifiedOneOfCustomSignatureOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class Data14:
    inspection_mode: PolicyObjectUnifiedOneOfInspectionModeOptionsDef = _field(
        metadata={"alias": "inspectionMode"}
    )
    log_level: PolicyObjectUnifiedOneOfLogLevelOptionsDef = _field(metadata={"alias": "logLevel"})
    signature_set: PolicyObjectUnifiedOneOfSignatureSetOptionsDef = _field(
        metadata={"alias": "signatureSet"}
    )
    custom_signature: Optional[PolicyObjectUnifiedOneOfCustomSignatureOptionsDef] = _field(
        default=None, metadata={"alias": "customSignature"}
    )
    # Valid UUID
    signature_allowed_list: Optional[SignatureAllowedList] = _field(
        default=None, metadata={"alias": "signatureAllowedList"}
    )


@dataclass
class EditSdwanSecurityFeature1PutRequest2:
    """
    Intrusion Prevention profile parcel schema for PUT request
    """

    data: Data14
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class PolicyObjectUnifiedOneOfWebCategoriesActionOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: PolicyObjectUnifiedWebCategoriesActionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class PolicyObjectUnifiedOneOfWebCategoriesOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[WebCategoriesDef]  # pytype: disable=annotation-type-mismatch


@dataclass
class PolicyObjectUnifiedOneOfWebReputationOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: PolicyObjectUnifiedWebReputationDef  # pytype: disable=annotation-type-mismatch


@dataclass
class PolicyObjectUnifiedOneOfBlockPageActionOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: PolicyObjectUnifiedBlockPageActionDef  # pytype: disable=annotation-type-mismatch


@dataclass
class PolicyObjectUnifiedOneOfBlockPageContentsOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class PolicyObjectUnifiedOneOfRedirectUrlOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class PolicyObjectUnifiedOneOfAlertsOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[AlertsDef]  # pytype: disable=annotation-type-mismatch


@dataclass
class Data15:
    block_page_action: PolicyObjectUnifiedOneOfBlockPageActionOptionsDef = _field(
        metadata={"alias": "blockPageAction"}
    )
    enable_alerts: OneOfEnableAlertsOptionsDef = _field(metadata={"alias": "enableAlerts"})
    web_categories_action: PolicyObjectUnifiedOneOfWebCategoriesActionOptionsDef = _field(
        metadata={"alias": "webCategoriesAction"}
    )
    web_reputation: PolicyObjectUnifiedOneOfWebReputationOptionsDef = _field(
        metadata={"alias": "webReputation"}
    )
    alerts: Optional[PolicyObjectUnifiedOneOfAlertsOptionsDef] = _field(default=None)
    block_page_contents: Optional[PolicyObjectUnifiedOneOfBlockPageContentsOptionsDef] = _field(
        default=None, metadata={"alias": "blockPageContents"}
    )
    redirect_url: Optional[PolicyObjectUnifiedOneOfRedirectUrlOptionsDef] = _field(
        default=None, metadata={"alias": "redirectUrl"}
    )
    url_allowed_list: Optional[UrlAllowedList] = _field(
        default=None, metadata={"alias": "urlAllowedList"}
    )
    url_blocked_list: Optional[UrlBlockedList] = _field(
        default=None, metadata={"alias": "urlBlockedList"}
    )
    web_categories: Optional[PolicyObjectUnifiedOneOfWebCategoriesOptionsDef] = _field(
        default=None, metadata={"alias": "webCategories"}
    )


@dataclass
class EditSdwanSecurityFeature1PutRequest3:
    """
    url-filtering profile parcel schema for put request
    """

    data: Data15
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class PolicyObjectUnifiedOneOfFileReputationCloudServerOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SdwanPolicyObjectUnifiedServerDef  # pytype: disable=annotation-type-mismatch


@dataclass
class PolicyObjectUnifiedOneOfFileReputationEstServerOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: (
        FeatureProfileSdwanPolicyObjectUnifiedServerDef  # pytype: disable=annotation-type-mismatch
    )


@dataclass
class PolicyObjectUnifiedOneOfFileReputationAlertOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SdwanPolicyObjectUnifiedAlertDef  # pytype: disable=annotation-type-mismatch


@dataclass
class PolicyObjectUnifiedOneOfFileAnalysisCloudServerOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: PolicyObjectUnifiedFileAnalysisCloudServerDef  # pytype: disable=annotation-type-mismatch


@dataclass
class PolicyObjectUnifiedOneOfFileAnalysisFileTypesOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[str]


@dataclass
class PolicyObjectUnifiedOneOfFileAnalysisAlertOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: (
        FeatureProfileSdwanPolicyObjectUnifiedAlertDef  # pytype: disable=annotation-type-mismatch
    )


@dataclass
class Data16:
    file_analysis_enabled: OneOfFileAnalysisEnabledOptionsDef = _field(
        metadata={"alias": "fileAnalysisEnabled"}
    )
    file_reputation_alert: PolicyObjectUnifiedOneOfFileReputationAlertOptionsDef = _field(
        metadata={"alias": "fileReputationAlert"}
    )
    file_reputation_cloud_server: PolicyObjectUnifiedOneOfFileReputationCloudServerOptionsDef = (
        _field(metadata={"alias": "fileReputationCloudServer"})
    )
    file_reputation_est_server: PolicyObjectUnifiedOneOfFileReputationEstServerOptionsDef = _field(
        metadata={"alias": "fileReputationEstServer"}
    )
    match_all_vpn: OneOfMatchAllVpnOptionsDef = _field(metadata={"alias": "matchAllVpn"})
    file_analysis_alert: Optional[PolicyObjectUnifiedOneOfFileAnalysisAlertOptionsDef] = _field(
        default=None, metadata={"alias": "fileAnalysisAlert"}
    )
    file_analysis_cloud_server: Optional[
        PolicyObjectUnifiedOneOfFileAnalysisCloudServerOptionsDef
    ] = _field(default=None, metadata={"alias": "fileAnalysisCloudServer"})
    file_analysis_file_types: Optional[PolicyObjectUnifiedOneOfFileAnalysisFileTypesOptionsDef] = (
        _field(default=None, metadata={"alias": "fileAnalysisFileTypes"})
    )


@dataclass
class EditSdwanSecurityFeature1PutRequest4:
    """
    advanced-malware-protection profile parcel schema for PUT request
    """

    data: Data16
    description: str
    name: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class PolicyObjectUnifiedOneOfDecryptCategoriesOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[CategoriesDef]  # pytype: disable=annotation-type-mismatch


@dataclass
class PolicyObjectUnifiedOneOfNeverDecryptCategoriesOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[CategoriesDef]  # pytype: disable=annotation-type-mismatch


@dataclass
class PolicyObjectUnifiedOneOfSkipDecryptCategoriesOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: List[CategoriesDef]  # pytype: disable=annotation-type-mismatch


@dataclass
class PolicyObjectUnifiedOneOfDecryptThresholdOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SdwanPolicyObjectUnifiedThresholdDef  # pytype: disable=annotation-type-mismatch


@dataclass
class PolicyObjectUnifiedOneOfSkipDecryptThresholdOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: FeatureProfileSdwanPolicyObjectUnifiedThresholdDef  # pytype: disable=annotation-type-mismatch


@dataclass
class Data17:
    decrypt_categories: PolicyObjectUnifiedOneOfDecryptCategoriesOptionsDef = _field(
        metadata={"alias": "decryptCategories"}
    )
    fail_decrypt: OneOfFailDecryptOptionsDef = _field(metadata={"alias": "failDecrypt"})
    never_decrypt_categories: PolicyObjectUnifiedOneOfNeverDecryptCategoriesOptionsDef = _field(
        metadata={"alias": "neverDecryptCategories"}
    )
    reputation: OneOfReputationOptionsDef
    decrypt_threshold: Optional[PolicyObjectUnifiedOneOfDecryptThresholdOptionsDef] = _field(
        default=None, metadata={"alias": "decryptThreshold"}
    )
    skip_decrypt_categories: Optional[PolicyObjectUnifiedOneOfSkipDecryptCategoriesOptionsDef] = (
        _field(default=None, metadata={"alias": "skipDecryptCategories"})
    )
    skip_decrypt_threshold: Optional[PolicyObjectUnifiedOneOfSkipDecryptThresholdOptionsDef] = (
        _field(default=None, metadata={"alias": "skipDecryptThreshold"})
    )
    url_allowed_list: Optional[UrlAllowedList] = _field(
        default=None, metadata={"alias": "urlAllowedList"}
    )
    url_blocked_list: Optional[UrlBlockedList] = _field(
        default=None, metadata={"alias": "urlBlockedList"}
    )


@dataclass
class EditSdwanSecurityFeature1PutRequest5:
    """
    ssl-decryption-profile profile parcel schema for put request
    """

    data: Data17
    description: str
    name: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Data18:
    ca_cert_bundle: Optional[Any] = _field(default=None, metadata={"alias": "caCertBundle"})


@dataclass
class EditSdwanSecurityFeature1PutRequest61:
    data: Data18
    # Will be auto generated
    description: str
    name: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class PolicyObjectUnifiedOneOfExpiredCertificateOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: FeatureProfileSdwanPolicyObjectUnifiedDecryptAndDropStringDef  # pytype: disable=annotation-type-mismatch


@dataclass
class PolicyObjectUnifiedOneOfUntrustedCertificateOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: V1FeatureProfileSdwanPolicyObjectUnifiedDecryptAndDropStringDef  # pytype: disable=annotation-type-mismatch


@dataclass
class PolicyObjectUnifiedOneOfCertificateRevocationStatusOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: PolicyObjectUnifiedCertificateRevocationStatusDef  # pytype: disable=annotation-type-mismatch


@dataclass
class PolicyObjectUnifiedOneOfUnknownStatusOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: DecryptAndDropStringDef1  # pytype: disable=annotation-type-mismatch


@dataclass
class PolicyObjectUnifiedOneOfUnsupportedProtocolVersionsOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: SdwanPolicyObjectUnifiedNoDecryptAndDropStringDef  # pytype: disable=annotation-type-mismatch


@dataclass
class PolicyObjectUnifiedOneOfUnsupportedCipherSuitesOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: FeatureProfileSdwanPolicyObjectUnifiedNoDecryptAndDropStringDef  # pytype: disable=annotation-type-mismatch


@dataclass
class PolicyObjectUnifiedOneOfFailureModeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: PolicyObjectUnifiedFailureModeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class SdwanPolicyObjectUnifiedDefaultDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class PolicyObjectUnifiedOneOfCaCertBundleOptionsDef1:
    default: SdwanPolicyObjectUnifiedDefaultDef


@dataclass
class FeatureProfileSdwanPolicyObjectUnifiedDefaultDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: bool


@dataclass
class PolicyObjectUnifiedFileNameDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class PolicyObjectUnifiedBundleStringDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class PolicyObjectUnifiedOneOfCaCertBundleOptionsDef2:
    bundle_string: PolicyObjectUnifiedBundleStringDef = _field(metadata={"alias": "bundleString"})
    default: FeatureProfileSdwanPolicyObjectUnifiedDefaultDef
    file_name: PolicyObjectUnifiedFileNameDef = _field(metadata={"alias": "fileName"})


@dataclass
class PolicyObjectUnifiedOneOfKeyModulusOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: PolicyObjectUnifiedKeyModulusDef  # pytype: disable=annotation-type-mismatch


@dataclass
class PolicyObjectUnifiedOneOfEckeyTypeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: PolicyObjectUnifiedEckeyTypeDef  # pytype: disable=annotation-type-mismatch


@dataclass
class PolicyObjectUnifiedOneOfCertificateLifetimeOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class PolicyObjectUnifiedOneOfMinTlsVerOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: PolicyObjectUnifiedMinTlsVerDef  # pytype: disable=annotation-type-mismatch


@dataclass
class PolicyObjectUnifiedOneOfCaTpLabelOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: PolicyObjectUnifiedCaTpLabelDef  # pytype: disable=annotation-type-mismatch


@dataclass
class Data19:
    ssl_enable: OneOfSslEnableOptionsDef = _field(metadata={"alias": "sslEnable"})
    ca_cert_bundle: Optional[
        Union[
            PolicyObjectUnifiedOneOfCaCertBundleOptionsDef1,
            PolicyObjectUnifiedOneOfCaCertBundleOptionsDef2,
        ]
    ] = _field(default=None, metadata={"alias": "caCertBundle"})
    ca_tp_label: Optional[PolicyObjectUnifiedOneOfCaTpLabelOptionsDef] = _field(
        default=None, metadata={"alias": "caTpLabel"}
    )
    certificate_lifetime: Optional[PolicyObjectUnifiedOneOfCertificateLifetimeOptionsDef] = _field(
        default=None, metadata={"alias": "certificateLifetime"}
    )
    certificate_revocation_status: Optional[
        PolicyObjectUnifiedOneOfCertificateRevocationStatusOptionsDef
    ] = _field(default=None, metadata={"alias": "certificateRevocationStatus"})
    eckey_type: Optional[PolicyObjectUnifiedOneOfEckeyTypeOptionsDef] = _field(
        default=None, metadata={"alias": "eckeyType"}
    )
    expired_certificate: Optional[PolicyObjectUnifiedOneOfExpiredCertificateOptionsDef] = _field(
        default=None, metadata={"alias": "expiredCertificate"}
    )
    failure_mode: Optional[PolicyObjectUnifiedOneOfFailureModeOptionsDef] = _field(
        default=None, metadata={"alias": "failureMode"}
    )
    key_modulus: Optional[PolicyObjectUnifiedOneOfKeyModulusOptionsDef] = _field(
        default=None, metadata={"alias": "keyModulus"}
    )
    min_tls_ver: Optional[PolicyObjectUnifiedOneOfMinTlsVerOptionsDef] = _field(
        default=None, metadata={"alias": "minTlsVer"}
    )
    unknown_status: Optional[PolicyObjectUnifiedOneOfUnknownStatusOptionsDef] = _field(
        default=None, metadata={"alias": "unknownStatus"}
    )
    unsupported_cipher_suites: Optional[
        PolicyObjectUnifiedOneOfUnsupportedCipherSuitesOptionsDef
    ] = _field(default=None, metadata={"alias": "unsupportedCipherSuites"})
    unsupported_protocol_versions: Optional[
        PolicyObjectUnifiedOneOfUnsupportedProtocolVersionsOptionsDef
    ] = _field(default=None, metadata={"alias": "unsupportedProtocolVersions"})
    untrusted_certificate: Optional[PolicyObjectUnifiedOneOfUntrustedCertificateOptionsDef] = (
        _field(default=None, metadata={"alias": "untrustedCertificate"})
    )


@dataclass
class EditSdwanSecurityFeature1PutRequest62:
    data: Data19
    # Will be auto generated
    description: str
    name: str
    metadata: Optional[Any] = _field(default=None)
