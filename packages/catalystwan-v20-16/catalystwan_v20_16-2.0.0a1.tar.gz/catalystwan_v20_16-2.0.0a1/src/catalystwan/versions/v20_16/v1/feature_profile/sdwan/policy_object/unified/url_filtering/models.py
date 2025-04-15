# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

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


@dataclass
class CreateSdwanSecurityFeaturePostResponse:
    parcel_id: Optional[str] = _field(default=None, metadata={"alias": "parcelId"})


@dataclass
class CreateSdwanSecurityFeaturePostRequest11:
    data: Any
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
class RefIdOptionDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


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
class Data:
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
class CreateSdwanSecurityFeaturePostRequest12:
    data: Data
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class CreateSdwanSecurityFeaturePostRequest21:
    data: Any
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class CreateSdwanSecurityFeaturePostRequest22:
    data: Data
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class CreateSdwanSecurityFeaturePostRequest31:
    data: Any
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class CreateSdwanSecurityFeaturePostRequest32:
    data: Data
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class CreateSdwanSecurityFeaturePostRequest41:
    data: Any
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class CreateSdwanSecurityFeaturePostRequest42:
    data: Data
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class CreateSdwanSecurityFeaturePostRequest51:
    data: Any
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class CreateSdwanSecurityFeaturePostRequest52:
    data: Data
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class CreateSdwanSecurityFeaturePostRequest61:
    data: Any
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class CreateSdwanSecurityFeaturePostRequest62:
    data: Data
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class CreateSdwanSecurityFeaturePostRequest71:
    data: Any
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class CreateSdwanSecurityFeaturePostRequest72:
    data: Data
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Payload11:
    data: Any
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Payload12:
    data: Data
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Payload21:
    data: Any
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Payload22:
    data: Data
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Payload31:
    data: Any
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Payload32:
    data: Data
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Payload41:
    data: Any
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Payload42:
    data: Data
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Payload51:
    data: Any
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Payload52:
    data: Data
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Payload61:
    data: Any
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Payload62:
    data: Data
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Payload71:
    data: Any
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Payload72:
    data: Data
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetSdwanSecurityFeatureGetResponse:
    created_by: Optional[str] = _field(default=None, metadata={"alias": "createdBy"})
    created_on: Optional[int] = _field(default=None, metadata={"alias": "createdOn"})
    last_updated_by: Optional[str] = _field(default=None, metadata={"alias": "lastUpdatedBy"})
    last_updated_on: Optional[int] = _field(default=None, metadata={"alias": "lastUpdatedOn"})
    parcel_id: Optional[str] = _field(default=None, metadata={"alias": "parcelId"})
    parcel_type: Optional[str] = _field(default=None, metadata={"alias": "parcelType"})
    # url-filtering profile parcel schema for POST request
    payload: Optional[
        Union[
            Union[Payload11, Payload12],
            Union[Payload21, Payload22],
            Union[Payload31, Payload32],
            Union[Payload41, Payload42],
            Union[Payload51, Payload52],
            Union[Payload61, Payload62],
            Union[Payload71, Payload72],
        ]
    ] = _field(default=None)
