# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

TlsDecryptionActionDef = Literal["decrypt", "neverDecrypt", "skipDecrypt"]


@dataclass
class CreateSdwanSecurityFeaturePostResponse:
    parcel_id: Optional[str] = _field(default=None, metadata={"alias": "parcelId"})


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
class CreateSdwanSecurityFeaturePostRequest:
    """
    advanced-malware-protection profile parcel schema for POST request
    """

    # requires tlsDecryptionAction and at least one of Intrusion Prevention or URL Filtering or Advanced Malware Protection policies
    data: Union[Data1, Data2, Data3]
    description: str
    name: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Payload:
    """
    advanced-malware-protection profile parcel schema for POST request
    """

    # requires tlsDecryptionAction and at least one of Intrusion Prevention or URL Filtering or Advanced Malware Protection policies
    data: Union[Data1, Data2, Data3]
    description: str
    name: str
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetSdwanSecurityFeatureGetResponse:
    created_by: Optional[str] = _field(default=None, metadata={"alias": "createdBy"})
    created_on: Optional[int] = _field(default=None, metadata={"alias": "createdOn"})
    last_updated_by: Optional[str] = _field(default=None, metadata={"alias": "lastUpdatedBy"})
    last_updated_on: Optional[int] = _field(default=None, metadata={"alias": "lastUpdatedOn"})
    parcel_id: Optional[str] = _field(default=None, metadata={"alias": "parcelId"})
    parcel_type: Optional[str] = _field(default=None, metadata={"alias": "parcelType"})
    # advanced-malware-protection profile parcel schema for POST request
    payload: Optional[Payload] = _field(default=None)
