# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional

GlobalOptionTypeDef = Literal["global"]


@dataclass
class CreateDataPrefixProfileParcelForSecurityPolicyObjectPostResponse:
    parcel_id: Optional[str] = _field(default=None, metadata={"alias": "parcelId"})


@dataclass
class OneOfEntriesGeneratorIdOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class OneOfEntriesSignatureIdOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class Entries:
    generator_id: OneOfEntriesGeneratorIdOptionsDef = _field(metadata={"alias": "generatorId"})
    signature_id: OneOfEntriesSignatureIdOptionsDef = _field(metadata={"alias": "signatureId"})


@dataclass
class Data:
    # Ips Signature
    entries: List[Entries]


@dataclass
class CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest:
    """
    security-ipssignature profile parcel schema for POST request
    """

    data: Data
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Payload:
    """
    security-ipssignature profile parcel schema for POST request
    """

    data: Data
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class GetDataPrefixProfileParcelForPolicyObjectGetResponse:
    created_by: Optional[str] = _field(default=None, metadata={"alias": "createdBy"})
    created_on: Optional[int] = _field(default=None, metadata={"alias": "createdOn"})
    last_updated_by: Optional[str] = _field(default=None, metadata={"alias": "lastUpdatedBy"})
    last_updated_on: Optional[int] = _field(default=None, metadata={"alias": "lastUpdatedOn"})
    parcel_id: Optional[str] = _field(default=None, metadata={"alias": "parcelId"})
    parcel_type: Optional[str] = _field(default=None, metadata={"alias": "parcelType"})
    # security-ipssignature profile parcel schema for POST request
    payload: Optional[Payload] = _field(default=None)
