# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, Literal, Optional

GlobalOptionTypeDef = Literal["global"]

SignatureSetDef = Literal["balanced", "connectivity", "security"]

InspectionModeDef = Literal["detection", "protection"]

LogLevelDef = Literal[
    "alert", "critical", "debug", "emergency", "error", "info", "notice", "warning"
]


@dataclass
class CreateSdwanSecurityFeaturePostResponse:
    parcel_id: Optional[str] = _field(default=None, metadata={"alias": "parcelId"})


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
class Data:
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
class CreateSdwanSecurityFeaturePostRequest:
    """
    Intrusion Prevention profile parcel schema for POST request
    """

    data: Data
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Payload:
    """
    Intrusion Prevention profile parcel schema for POST request
    """

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
    # Intrusion Prevention profile parcel schema for POST request
    payload: Optional[Payload] = _field(default=None)
