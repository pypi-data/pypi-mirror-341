# Copyright 2024 Cisco Systems, Inc. and its affiliates
from dataclasses import dataclass
from dataclasses import field as _field
from typing import Any, List, Literal, Optional, Union

GlobalOptionTypeDef = Literal["global"]

EntriesCriteriaDef = Literal[
    "jitter",
    "jitter-latency",
    "jitter-latency-loss",
    "jitter-loss",
    "jitter-loss-latency",
    "latency",
    "latency-jitter",
    "latency-jitter-loss",
    "latency-loss",
    "latency-loss-jitter",
    "loss",
    "loss-jitter",
    "loss-jitter-latency",
    "loss-latency",
    "loss-latency-jitter",
]


@dataclass
class CreateDataPrefixProfileParcelForSecurityPolicyObjectPostResponse:
    parcel_id: Optional[str] = _field(default=None, metadata={"alias": "parcelId"})


@dataclass
class OneOfEntriesLatencyOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfEntriesLossOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class OneOfEntriesJitterOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: int


@dataclass
class RefId:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: str


@dataclass
class ParcelReferenceDef:
    ref_id: RefId = _field(metadata={"alias": "refId"})


@dataclass
class OneOfEntriesCriteriaOptionsDef:
    option_type: GlobalOptionTypeDef = _field(
        metadata={"alias": "optionType"}
    )  # pytype: disable=annotation-type-mismatch
    value: EntriesCriteriaDef


@dataclass
class FallbackBestTunnel:
    """
    Object with a criteria and variance
    """

    criteria: Optional[OneOfEntriesCriteriaOptionsDef] = _field(default=None)
    jitter_variance: Optional[OneOfEntriesJitterOptionsDef] = _field(
        default=None, metadata={"alias": "jitterVariance"}
    )
    latency_variance: Optional[OneOfEntriesLatencyOptionsDef] = _field(
        default=None, metadata={"alias": "latencyVariance"}
    )
    loss_variance: Optional[OneOfEntriesLossOptionsDef] = _field(
        default=None, metadata={"alias": "lossVariance"}
    )


@dataclass
class Entries1:
    latency: OneOfEntriesLatencyOptionsDef
    app_probe_class: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "appProbeClass"}
    )
    # Object with a criteria and variance
    fallback_best_tunnel: Optional[FallbackBestTunnel] = _field(
        default=None, metadata={"alias": "fallbackBestTunnel"}
    )
    jitter: Optional[OneOfEntriesJitterOptionsDef] = _field(default=None)
    loss: Optional[OneOfEntriesLossOptionsDef] = _field(default=None)


@dataclass
class Entries2:
    loss: OneOfEntriesLossOptionsDef
    app_probe_class: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "appProbeClass"}
    )
    # Object with a criteria and variance
    fallback_best_tunnel: Optional[FallbackBestTunnel] = _field(
        default=None, metadata={"alias": "fallbackBestTunnel"}
    )
    jitter: Optional[OneOfEntriesJitterOptionsDef] = _field(default=None)
    latency: Optional[OneOfEntriesLatencyOptionsDef] = _field(default=None)


@dataclass
class Entries3:
    jitter: OneOfEntriesJitterOptionsDef
    app_probe_class: Optional[ParcelReferenceDef] = _field(
        default=None, metadata={"alias": "appProbeClass"}
    )
    # Object with a criteria and variance
    fallback_best_tunnel: Optional[FallbackBestTunnel] = _field(
        default=None, metadata={"alias": "fallbackBestTunnel"}
    )
    latency: Optional[OneOfEntriesLatencyOptionsDef] = _field(default=None)
    loss: Optional[OneOfEntriesLossOptionsDef] = _field(default=None)


@dataclass
class Data:
    # Sla class List
    entries: List[Union[Entries1, Entries2, Entries3]]


@dataclass
class CreateDataPrefixProfileParcelForSecurityPolicyObjectPostRequest:
    """
    Sla class profile parcel schema for POST request
    """

    data: Data
    name: str
    description: Optional[str] = _field(default=None)
    metadata: Optional[Any] = _field(default=None)


@dataclass
class Payload:
    """
    Sla class profile parcel schema for POST request
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
    # Sla class profile parcel schema for POST request
    payload: Optional[Payload] = _field(default=None)
