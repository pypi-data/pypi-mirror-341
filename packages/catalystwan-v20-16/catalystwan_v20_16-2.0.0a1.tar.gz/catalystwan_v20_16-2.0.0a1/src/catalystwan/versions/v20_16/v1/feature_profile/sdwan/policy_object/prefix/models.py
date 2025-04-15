# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional

GlobalOptionTypeDef = Literal["global"]


@dataclass
class CreateDataPrefixProfileParcelForSecurityPolicyObjectPostResponse:
    parcel_id: Optional[str] = _field(default=None, metadata={"alias": "parcelId"})


@dataclass
class EntriesIpv4AddressOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class EntriesIpv4PrefixLengthOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class EntriesLeRangePrefixLengthOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class EntriesGeRangePrefixLengthOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class Entries:
    ipv4_address: EntriesIpv4AddressOptionsDef = _field(metadata={"alias": "ipv4Address"})
    ipv4_prefix_length: EntriesIpv4PrefixLengthOptionsDef = _field(
        metadata={"alias": "ipv4PrefixLength"}
    )
    ge_range_prefix_length: Optional[EntriesGeRangePrefixLengthOptionsDef] = _field(
        default=None, metadata={"alias": "geRangePrefixLength"}
    )
    le_range_prefix_length: Optional[EntriesLeRangePrefixLengthOptionsDef] = _field(
        default=None, metadata={"alias": "leRangePrefixLength"}
    )


@dataclass
class Data:
    # IPv4 Prefix List
    entries: List[Entries]


@dataclass
class CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest:
    """
    Ipv4 prefix profile parcel schema
    """

    data: Data
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Payload:
    """
    Ipv4 prefix profile parcel schema
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
    # Ipv4 prefix profile parcel schema
    payload: Optional[Payload] = _field(default=None)
