# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional

GlobalOptionTypeDef = Literal["global"]


@dataclass
class CreateDataPrefixProfileParcelForSecurityPolicyObjectPostResponse:
    parcel_id: Optional[str] = _field(default=None, metadata={"alias": "parcelId"})


@dataclass
class EntriesIpv6AddressOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class EntriesIpv6PrefixLengthOptionsDef:
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
    ipv6_address: EntriesIpv6AddressOptionsDef = _field(metadata={"alias": "ipv6Address"})
    ipv6_prefix_length: EntriesIpv6PrefixLengthOptionsDef = _field(
        metadata={"alias": "ipv6PrefixLength"}
    )
    ge_range_prefix_length: Optional[EntriesGeRangePrefixLengthOptionsDef] = _field(
        default=None, metadata={"alias": "geRangePrefixLength"}
    )
    le_range_prefix_length: Optional[EntriesLeRangePrefixLengthOptionsDef] = _field(
        default=None, metadata={"alias": "leRangePrefixLength"}
    )


@dataclass
class Data:
    # IPv6 Prefix List
    entries: List[Entries]


@dataclass
class CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest:
    """
    Ipv6 prefix profile parcel schema
    """

    data: Data
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Payload:
    """
    Ipv6 prefix profile parcel schema
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
    # Ipv6 prefix profile parcel schema
    payload: Optional[Payload] = _field(default=None)
